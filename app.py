import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from scipy import linalg
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
import pytz
from io import BytesIO
import base64
import json
import os
from pathlib import Path
import warnings
import logging
from typing import Dict, List, Optional, Tuple, Any
import hashlib

# Suppress warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
class Config:
    """Application configuration"""
    APP_TITLE = "🏥 Agentic AI & RAG for Healthcare Quality Management"
    APP_ICON = "🏥"
    LAYOUT = "wide"
    SIDEBAR_STATE = "expanded"
    
    # File upload settings
    MAX_FILE_SIZE = 200  # MB
    ALLOWED_EXTENSIONS = ['csv', 'xlsx', 'xls']
    
    # Default simulation parameters
    DEFAULT_SIMULATIONS = 100
    MAX_SIMULATIONS = 1000

# Enhanced CSS for better UI
def load_css():
    """Load custom CSS for enhanced UI"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .sidebar .stRadio > label {
        background: rgba(255, 255, 255, 0.1);
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.2rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

class DataValidator:
    """Data validation utilities"""
    
    @staticmethod
    def validate_file(file) -> Tuple[bool, str]:
        """Validate uploaded file"""
        if file is None:
            return False, "No file uploaded"
        
        # Check file size
        if file.size > Config.MAX_FILE_SIZE * 1024 * 1024:
            return False, f"File size exceeds {Config.MAX_FILE_SIZE}MB limit"
        
        # Check file extension
        file_extension = file.name.split('.')[-1].lower()
        if file_extension not in Config.ALLOWED_EXTENSIONS:
            return False, f"File type not supported. Allowed: {', '.join(Config.ALLOWED_EXTENSIONS)}"
        
        return True, "File is valid"
    
    @staticmethod
    def validate_matrix(matrix: np.ndarray) -> Tuple[bool, str]:
        """Validate comparison matrix for AHP/ANP"""
        if matrix.shape[0] != matrix.shape[1]:
            return False, "Matrix must be square"
        
        # Check for zeros on diagonal
        if np.any(np.diag(matrix) == 0):
            return False, "Diagonal elements cannot be zero"
        
        # Check for negative values
        if np.any(matrix < 0):
            return False, "Matrix cannot contain negative values"
        
        return True, "Matrix is valid"

class RAGSystem:
    """Retrieval-Augmented Generation System for Healthcare Knowledge"""
    
    def __init__(self):
        self.knowledge_base = self._initialize_knowledge_base()
        self.embeddings_cache = {}
    
    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        """Initialize healthcare quality management knowledge base"""
        return {
            "quality_indicators": {
                "patient_safety": ["Medication errors", "Hospital-acquired infections", "Patient falls"],
                "clinical_effectiveness": ["Mortality rates", "Readmission rates", "Treatment outcomes"],
                "patient_experience": ["Patient satisfaction", "Waiting times", "Communication quality"],
                "operational_efficiency": ["Bed occupancy", "Staff productivity", "Resource utilization"]
            },
            "best_practices": {
                "infection_control": "Implement hand hygiene protocols, use personal protective equipment",
                "medication_safety": "Double-check prescriptions, use barcode scanning systems",
                "patient_communication": "Active listening, clear explanations, empathy"
            },
            "compliance_standards": {
                "Joint Commission": ["Patient safety goals", "Performance improvement"],
                "ISO 9001": ["Quality management system", "Continuous improvement"],
                "HIPAA": ["Privacy protection", "Security measures"]
            }
        }
    
    def query_knowledge(self, query: str) -> List[str]:
        """Query the knowledge base for relevant information"""
        query_lower = query.lower()
        relevant_info = []
        
        for category, items in self.knowledge_base.items():
            if isinstance(items, dict):
                for key, value in items.items():
                    if any(term in key.lower() or term in str(value).lower() for term in query_lower.split()):
                        relevant_info.append(f"{category} - {key}: {value}")
            elif isinstance(items, list):
                for item in items:
                    if any(term in item.lower() for term in query_lower.split()):
                        relevant_info.append(f"{category}: {item}")
        
        return relevant_info[:5]  # Return top 5 relevant items

class AgenticAI:
    """Main Agentic AI system with enhanced capabilities"""
    
    def __init__(self):
        self.data = None
        self.processed_data = None
        self.anp_results = None
        self.ahp_results = None
        self.news_data = []
        self.rag_system = RAGSystem()
        self.analysis_history = []
        self.session_state = {}
    
    def load_data(self, file) -> Tuple[bool, str]:
        """Load and validate data from uploaded file"""
        try:
            # Validate file first
            is_valid, message = DataValidator.validate_file(file)
            if not is_valid:
                return False, message
            
            # Load data based on file type
            file_extension = file.name.split('.')[-1].lower()
            
            if file_extension == 'csv':
                self.data = pd.read_csv(file, encoding='utf-8')
            elif file_extension in ['xlsx', 'xls']:
                self.data = pd.read_excel(file)
            
            # Basic data validation
            if self.data.empty:
                return False, "The file contains no data"
            
            # Clean data
            self.data = self._clean_data(self.data)
            
            # Store file metadata
            self.session_state['file_info'] = {
                'name': file.name,
                'size': file.size,
                'shape': self.data.shape,
                'columns': list(self.data.columns),
                'loaded_at': datetime.now().isoformat()
            }
            
            logger.info(f"Data loaded successfully: {self.data.shape}")
            return True, f"Data loaded successfully! Shape: {self.data.shape}"
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return False, f"Error loading data: {str(e)}"
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess data"""
        # Remove duplicate columns
        df = df.loc[:, ~df.columns.duplicated()]
        
        # Handle missing values
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        categorical_columns = df.select_dtypes(include=['object']).columns
        
        # Fill numeric columns with median
        for col in numeric_columns:
            df[col].fillna(df[col].median(), inplace=True)
        
        # Fill categorical columns with mode
        for col in categorical_columns:
            mode_value = df[col].mode().iloc[0] if not df[col].mode().empty else 'Unknown'
            df[col].fillna(mode_value, inplace=True)
        
        return df
    
    def analyze_data(self) -> Optional[Dict[str, Any]]:
        """Comprehensive data analysis with RAG integration"""
        if self.data is None:
            return None
        
        try:
            analysis = {
                "basic_info": {
                    "shape": self.data.shape,
                    "columns": list(self.data.columns),
                    "data_types": self.data.dtypes.to_dict(),
                    "missing_values": self.data.isnull().sum().to_dict(),
                    "duplicate_rows": int(self.data.duplicated().sum())
                },
                "descriptive_stats": self.data.describe().to_dict(),
                "correlation_matrix": self.data.corr().to_dict(),
                "categorical_analysis": self._analyze_categorical_columns(),
                "insights": self._generate_insights(),
                "rag_recommendations": self._get_rag_recommendations()
            }
            
            # Store analysis in history
            self.analysis_history.append({
                "timestamp": datetime.now().isoformat(),
                "analysis": analysis
            })
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in data analysis: {str(e)}")
            st.error(f"Error in data analysis: {str(e)}")
            return None
    
    def _analyze_categorical_columns(self) -> Dict[str, Any]:
        """Analyze categorical columns"""
        categorical_analysis = {}
        categorical_columns = self.data.select_dtypes(include=['object']).columns
        
        for col in categorical_columns:
            categorical_analysis[col] = {
                "unique_values": int(self.data[col].nunique()),
                "value_counts": self.data[col].value_counts().to_dict(),
                "top_values": self.data[col].value_counts().head(5).to_dict()
            }
        
        return categorical_analysis
    
    def _generate_insights(self) -> List[str]:
        """Generate automated insights from data"""
        insights = []
        
        try:
            # Check for high correlation
            numeric_data = self.data.select_dtypes(include=[np.number])
            if len(numeric_data.columns) > 1:
                corr_matrix = numeric_data.corr()
                high_corr = np.where(np.abs(corr_matrix) > 0.8)
                for i, j in zip(high_corr[0], high_corr[1]):
                    if i != j:
                        col1, col2 = corr_matrix.index[i], corr_matrix.columns[j]
                        corr_value = corr_matrix.iloc[i, j]
                        insights.append(f"High correlation ({corr_value:.2f}) between {col1} and {col2}")
            
            # Check for outliers
            numeric_columns = self.data.select_dtypes(include=[np.number]).columns
            for col in numeric_columns:
                Q1 = self.data[col].quantile(0.25)
                Q3 = self.data[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers = self.data[(self.data[col] < (Q1 - 1.5 * IQR)) | (self.data[col] > (Q3 + 1.5 * IQR))]
                if len(outliers) > 0:
                    insights.append(f"Found {len(outliers)} outliers in {col}")
            
            # Check data distribution
            for col in numeric_columns:
                skewness = self.data[col].skew()
                if abs(skewness) > 1:
                    insights.append(f"{col} shows {'right' if skewness > 0 else 'left'} skewness ({skewness:.2f})")
        
        except Exception as e:
            logger.error(f"Error generating insights: {str(e)}")
            insights.append("Unable to generate insights due to data structure")
        
        return insights[:10]  # Return top 10 insights
    
    def _get_rag_recommendations(self) -> List[str]:
        """Get RAG-based recommendations"""
        if not hasattr(self, 'data') or self.data is None:
            return []
        
        recommendations = []
        
        try:
            # Analyze column names for healthcare relevance
            column_names = ' '.join(self.data.columns).lower()
            rag_results = self.rag_system.query_knowledge(column_names)
            
            for result in rag_results:
                recommendations.append(f"Healthcare Insight: {result}")
        except Exception as e:
            logger.error(f"Error getting RAG recommendations: {str(e)}")
            recommendations.append("Unable to generate recommendations")
        
        return recommendations
    
    def anp_analysis(self, comparison_matrix: np.ndarray) -> Optional[Dict[str, Any]]:
        """Enhanced ANP analysis with validation"""
        try:
            # Validate matrix
            is_valid, message = DataValidator.validate_matrix(comparison_matrix)
            if not is_valid:
                st.error(f"Matrix validation failed: {message}")
                return None
            
            # Normalize matrix
            column_sums = comparison_matrix.sum(axis=0)
            norm_matrix = comparison_matrix / column_sums
            
            # Calculate priority vector
            priority_vector = norm_matrix.mean(axis=1)
            
            # Calculate consistency
            weighted_sum = comparison_matrix @ priority_vector
            consistency_vector = weighted_sum / priority_vector
            lambda_max = consistency_vector.mean()
            
            n = comparison_matrix.shape[0]
            consistency_index = (lambda_max - n) / (n - 1) if n > 1 else 0
            
            # Random Index values for different matrix sizes
            random_indices = {2: 0, 3: 0.58, 4: 0.9, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
            random_index = random_indices.get(n, 1.49)
            
            consistency_ratio = consistency_index / random_index if random_index != 0 else 0
            
            result = {
                "priority_vector": priority_vector.tolist(),
                "consistency_ratio": float(consistency_ratio),
                "consistency_index": float(consistency_index),
                "lambda_max": float(lambda_max),
                "is_consistent": consistency_ratio < 0.1,
                "matrix_size": int(n)
            }
            
            self.anp_results = result
            return result
            
        except Exception as e:
            logger.error(f"Error in ANP analysis: {str(e)}")
            st.error(f"Error in ANP analysis: {str(e)}")
            return None
    
    def scenario_planning(self, parameters: Dict[str, float], simulations: int = 100) -> Optional[pd.DataFrame]:
        """Enhanced scenario planning with validation"""
        try:
            if not parameters:
                st.error("No parameters provided for scenario planning")
                return None
            
            # Validate parameters
            for param, value in parameters.items():
                if not isinstance(value, (int, float)) or np.isnan(value):
                    st.error(f"Invalid value for parameter {param}: {value}")
                    return None
            
            # Generate scenarios
            results = []
            np.random.seed(42)  # For reproducibility
            
            for _ in range(simulations):
                scenario = {}
                for param, base_value in parameters.items():
                    # Add some randomness (±20% of base value)
                    std_dev = abs(base_value * 0.2)
                    scenario[param] = np.random.normal(base_value, std_dev)
                results.append(scenario)
            
            scenario_df = pd.DataFrame(results)
            
            # Add scenario metadata
            scenario_df['scenario_id'] = range(1, len(scenario_df) + 1)
            scenario_df['created_at'] = datetime.now()
            
            return scenario_df
            
        except Exception as e:
            logger.error(f"Error in scenario planning: {str(e)}")
            st.error(f"Error in scenario planning: {str(e)}")
            return None
    
    def fetch_news(self, query: str, engine: str = "demo", count: int = 5) -> List[Dict[str, str]]:
        """Demo news fetching (placeholder for real implementation)"""
        try:
            # Demo news data for demonstration
            demo_news = [
                {
                    "title": f"Healthcare Quality Management: {query} - Latest Developments",
                    "link": "https://example.com/news1",
                    "source": "Healthcare Today",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "summary": "Recent advances in healthcare quality management using AI and automation."
                },
                {
                    "title": f"AI in Healthcare: Transforming {query} Operations",
                    "link": "https://example.com/news2",
                    "source": "Medical AI Journal",
                    "timestamp": (datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
                    "summary": "How artificial intelligence is revolutionizing healthcare quality processes."
                },
                {
                    "title": f"Quality Metrics in Healthcare: {query} Best Practices",
                    "link": "https://example.com/news3",
                    "source": "Healthcare Management Review",
                    "timestamp": (datetime.now() - timedelta(hours=4)).strftime("%Y-%m-%d %H:%M:%S"),
                    "summary": "Evidence-based approaches to improving healthcare quality management."
                }
            ]
            
            self.news_data = demo_news[:count]
            return self.news_data
            
        except Exception as e:
            logger.error(f"Error fetching news: {str(e)}")
            st.error(f"Error fetching news: {str(e)}")
            return []

def create_ui():
    """Create the main UI"""
    st.set_page_config(
        page_title=Config.APP_TITLE,
        page_icon=Config.APP_ICON,
        layout=Config.LAYOUT,
        initial_sidebar_state=Config.SIDEBAR_STATE
    )
    
    # Load custom CSS
    load_css()
    
    # Initialize session state
    if 'ai_agent' not in st.session_state:
        st.session_state.ai_agent = AgenticAI()
    
    ai_agent = st.session_state.ai_agent
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏥 Agentic AI & RAG for Healthcare Quality Management</h1>
        <p>Advanced AI-powered analytics for modern healthcare systems</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.title("🚀 Navigation")
        navigation = st.radio(
            "Choose a section:",
            ["🏠 Home", "📊 Data Analysis", "⚖️ Decision Methods", "📈 Visualization", "🎯 Scenario Planning", "📰 News & Updates", "🤖 AI Assistant"]
        )
        
        st.markdown("---")
        st.markdown("### 📊 System Status")
        if ai_agent.data is not None:
            st.success(f"✅ Data loaded: {ai_agent.data.shape[0]} rows")
        else:
            st.info("ℹ️ No data loaded")
    
    # Main content area
    if navigation == "🏠 Home":
        show_home_page()
    elif navigation == "📊 Data Analysis":
        show_data_analysis_page(ai_agent)
    elif navigation == "⚖️ Decision Methods":
        show_decision_methods_page(ai_agent)
    elif navigation == "📈 Visualization":
        show_visualization_page(ai_agent)
    elif navigation == "🎯 Scenario Planning":
        show_scenario_planning_page(ai_agent)
    elif navigation == "📰 News & Updates":
        show_news_page(ai_agent)
    elif navigation == "🤖 AI Assistant":
        show_ai_assistant_page(ai_agent)

def show_home_page():
    """Home page content"""
    st.markdown("""
    <div class="feature-card">
        <h2>🚀 Welcome to Advanced Healthcare Quality Management</h2>
        <p>This application leverages <strong>Agentic AI</strong> and <strong>Retrieval-Augmented Generation (RAG)</strong> to revolutionize healthcare quality management processes.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Data Analysis</h3>
            <ul>
                <li>Multimodal data processing</li>
                <li>Automated insights generation</li>
                <li>Statistical analysis with RAG</li>
                <li>Quality metrics tracking</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>⚖️ Decision Support</h3>
            <ul>
                <li>AHP/ANP analysis</li>
                <li>Consistency validation</li>
                <li>Priority ranking</li>
                <li>Decision visualization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 AI Automation</h3>
            <ul>
                <li>Workflow automation</li>
                <li>Predictive analytics</li>
                <li>Scenario planning</li>
                <li>Real-time monitoring</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def show_data_analysis_page(ai_agent):
    """Data analysis page"""
    st.subheader("📊 Advanced Data Analysis")
    
    uploaded_file = st.file_uploader(
        "Upload your healthcare data file",
        type=Config.ALLOWED_EXTENSIONS,
        help=f"Supported formats: {', '.join(Config.ALLOWED_EXTENSIONS)}"
    )
    
    if uploaded_file:
        success, message = ai_agent.load_data(uploaded_file)
        if success:
            st.success(message)
            
            # Display data overview
            st.markdown("### 📋 Data Overview")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Rows</h4>
                    <h2>{ai_agent.data.shape[0]:,}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Columns</h4>
                    <h2>{ai_agent.data.shape[1]}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Missing Values</h4>
                    <h2>{ai_agent.data.isnull().sum().sum()}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>Duplicates</h4>
                    <h2>{ai_agent.data.duplicated().sum()}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            # Show sample data
            if st.checkbox("Show sample data"):
                st.dataframe(ai_agent.data.head(10))
            
            # Perform analysis
            if st.button("🔍 Perform Comprehensive Analysis", type="primary"):
                with st.spinner("Analyzing data with AI..."):
                    analysis = ai_agent.analyze_data()
                    
                    if analysis:
                        st.success("Analysis completed successfully!")
                        
                        # Display analysis results
                        tab1, tab2, tab3, tab4 = st.tabs(["📈 Statistics", "🔗 Correlations", "🧠 AI Insights", "🎯 Recommendations"])
                        
                        with tab1:
                            st.subheader("📊 Descriptive Statistics")
                            desc_stats = pd.DataFrame(analysis["descriptive_stats"])
                            st.dataframe(desc_stats)
                        
                        with tab2:
                            st.subheader("🔗 Correlation Analysis")
                            corr_data = pd.DataFrame(analysis["correlation_matrix"])
                            if not corr_data.empty:
                                fig = px.imshow(
                                    corr_data,
                                    color_continuous_scale='RdBu_r',
                                    aspect="auto",
                                    title="Correlation Heatmap"
                                )
                                st.plotly_chart(fig, use_container_width=True)
                        
                        with tab3:
                            st.subheader("🧠 AI-Generated Insights")
                            for i, insight in enumerate(analysis["insights"], 1):
                                st.info(f"💡 **Insight #{i}:** {insight}")
                        
                        with tab4:
                            st.subheader("🎯 Healthcare Quality Recommendations")
                            for i, rec in enumerate(analysis["rag_recommendations"], 1):
                                st.success(f"🏥 **Recommendation #{i}:** {rec}")
        else:
            st.error(message)

def show_decision_methods_page(ai_agent):
    """Decision methods page"""
    st.subheader("⚖️ Decision Support Methods")
    
    method = st.selectbox("Select Decision Analysis Method", ["ANP - Analytic Network Process", "AHP - Analytic Hierarchy Process"])
    
    if method == "ANP - Analytic Network Process":
        st.markdown("### 🔄 ANP Analysis")
        st.info("Configure pairwise comparison matrix for network analysis")
        
        size = st.slider("Matrix size", min_value=2, max_value=6, value=3)
        
        st.markdown("#### Pairwise Comparison Matrix")
        comparison_matrix = np.ones((size, size))
        
        # Create matrix input
        cols = st.columns(size + 1)
        with cols[0]:
            st.write("**Element**")
        for j in range(size):
            with cols[j + 1]:
                st.write(f"**Alt {j+1}**")
        
        for i in range(size):
            cols = st.columns(size + 1)
            with cols[0]:
                st.write(f"**Alt {i+1}**")
            for j in range(size):
                with cols[j + 1]:
                    if i == j:
                        st.write("1.00")
                    elif i < j:
                        value = st.number_input(
                            f"",
                            min_value=0.1,
                            max_value=9.0,
                            value=1.0,
                            step=0.1,
                            key=f"anp_{i}_{j}",
                            label_visibility="collapsed"
                        )
                        comparison_matrix[i, j] = value
                        comparison_matrix[j, i] = 1 / value if value != 0 else 1
                    else:
                        st.write(f"{comparison_matrix[i, j]:.2f}")
        
        if st.button("🔍 Calculate ANP Results"):
            result = ai_agent.anp_analysis(comparison_matrix)
            if result:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Priority Vector")
                    priority_df = pd.DataFrame({
                        'Alternative': [f'Alt {i+1}' for i in range(len(result['priority_vector']))],
                        'Priority': result['priority_vector']
                    })
                    fig = px.bar(priority_df, x='Alternative', y='Priority', title="Priority Rankings")
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.subheader("Consistency Analysis")
                    st.metric("Consistency Ratio", f"{result['consistency_ratio']:.4f}")
                    st.metric("Lambda Max", f"{result['lambda_max']:.4f}")
                    
                    if result['is_consistent']:
                        st.success("✅ Matrix is consistent (CR < 0.1)")
                    else:
                        st.warning("⚠️ Matrix is not consistent (CR ≥ 0.1)")

def show_visualization_page(ai_agent):
    """Data visualization page"""
    st.subheader("📈 Interactive Data Visualization")
    
    if ai_agent.data is None:
        st.warning("Please load data first in the Data Analysis section")
        return
    
    viz_type = st.selectbox(
        "Select Visualization Type",
        ["Histogram", "Boxplot", "Scatter Plot", "Correlation Heatmap", "Bar Chart"]
    )
    
    if viz_type == "Histogram":
        numeric_cols = ai_agent.data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            st.error("No numeric columns available for histogram")
            return
            
        col = st.selectbox("Select column", numeric_cols)
        bins = st.slider("Number of bins", 5, 50, 20)
        
        fig = px.histogram(ai_agent.data, x=col, nbins=bins, title=f"Histogram of {col}")
        st.plotly_chart(fig, use_container_width=True)
        
    elif viz_type == "Scatter Plot":
        numeric_cols = ai_agent.data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) < 2:
            st.error("Need at least 2 numeric columns for scatter plot")
            return
            
        x_col = st.selectbox("X-axis", numeric_cols)
        y_col = st.selectbox("Y-axis", numeric_cols)
        
        categorical_cols = ai_agent.data.select_dtypes(include=['object']).columns
        color_col = st.selectbox("Color by (optional)", ["None"] + list(categorical_cols))
        
        if color_col != "None":
            fig = px.scatter(ai_agent.data, x=x_col, y=y_col, color=color_col, title=f"{x_col} vs {y_col}")
        else:
            fig = px.scatter(ai_agent.data, x=x_col, y=y_col, title=f"{x_col} vs {y_col}")
        
        st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "Correlation Heatmap":
        numeric_data = ai_agent.data.select_dtypes(include=[np.number])
        if len(numeric_data.columns) < 2:
            st.error("Need at least 2 numeric columns for correlation heatmap")
            return
            
        corr_matrix = numeric_data.corr()
        fig = px.imshow(
            corr_matrix,
            color_continuous_scale='RdBu_r',
            aspect="auto",
            title="Correlation Heatmap"
        )
        st.plotly_chart(fig, use_container_width=True)

def show_scenario_planning_page(ai_agent):
    """Scenario planning page"""
    st.subheader("🎯 AI-Powered Scenario Planning")
    
    if ai_agent.data is None:
        st.warning("Please load data first in the Data Analysis section")
        return
    
    st.markdown("### Configure Scenario Parameters")
    
    numeric_cols = ai_agent.data.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) == 0:
        st.error("No numeric columns available for scenario planning")
        return
    
    parameters = {}
    
    for col in numeric_cols:
        avg_val = float(ai_agent.data[col].mean())
        parameters[col] = st.number_input(
            f"Base value for {col}",
            value=avg_val,
            key=f"scenario_{col}"
        )
    
    simulations = st.slider("Number of simulations", 10, 1000, 100)
    
    if st.button("🚀 Run Scenario Analysis"):
        with st.spinner("Running scenario simulations..."):
            scenario_df = ai_agent.scenario_planning(parameters, simulations)
            
            if scenario_df is not None:
                st.success("Scenario analysis completed!")
                
                # Display scenario results
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Scenario Statistics")
                    st.dataframe(scenario_df.describe())
                
                with col2:
                    st.subheader("📈 Scenario Distribution")
                    selected_param = st.selectbox("Select parameter to visualize", list(parameters.keys()))
                    fig = px.histogram(scenario_df, x=selected_param, title=f"Distribution of {selected_param}")
                    st.plotly_chart(fig, use_container_width=True)

def show_news_page(ai_agent):
    """News and updates page"""
    st.subheader("📰 Healthcare News & Updates")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_query = st.text_input(
            "Search healthcare news",
            value="healthcare quality management AI",
            help="Enter keywords to search for relevant healthcare news"
        )
    
    with col2:
        count = st.selectbox("Number of articles", [5, 10, 15, 20], index=0)
    
    if st.button("🔍 Search News"):
        with st.spinner("Fetching latest healthcare news..."):
            news_data = ai_agent.fetch_news(search_query, count=count)
            
            if news_data:
                st.success(f"Found {len(news_data)} relevant articles")
                
                for i, article in enumerate(news_data, 1):
                    st.markdown(f"### {i}. [{article['title']}]({article['link']})")
                    st.markdown(f"**Source:** {article['source']}")
                    st.markdown(f"**Summary:** {article.get('summary', 'No summary available')}")
                    st.markdown(f"**Published:** {article['timestamp']}")
                    st.markdown("---")
            else:
                st.warning("No news articles found. Please try different keywords.")

def show_ai_assistant_page(ai_agent):
    """AI Assistant page with RAG capabilities"""
    st.subheader("🤖 AI Healthcare Assistant")
    
    st.markdown("""
    Ask questions about healthcare quality management, and get AI-powered insights
    combined with knowledge from our specialized healthcare database.
    """)
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f"**You:** {chat['content']}")
        else:
            st.markdown(f"**🤖 AI Assistant:** {chat['content']}")
        st.markdown("---")
    
    # User input
    user_question = st.text_input("Ask me about healthcare quality management...")
    
    if st.button("Send") and user_question:
        # Add user message to chat
        st.session_state.chat_history.append({"role": "user", "content": user_question})
        
        # Generate AI response
        with st.spinner("AI is thinking..."):
            rag_results = ai_agent.rag_system.query_knowledge(user_question)
            response = generate_ai_response(user_question, rag_results, ai_agent.data)
            
        # Add to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()

def generate_ai_response(question: str, rag_results: List[str], data: Optional[pd.DataFrame]) -> str:
    """Generate AI response using RAG and data context"""
    response_parts = []
    
    # Start with a contextual response
    if "quality" in question.lower():
        response_parts.append("Based on healthcare quality management best practices:")
    elif "patient" in question.lower():
        response_parts.append("Regarding patient care and safety:")
    elif "data" in question.lower() and data is not None:
        response_parts.append(f"Analyzing your uploaded dataset with {data.shape[0]} records:")
    else:
        response_parts.append("Here's what I found in our healthcare knowledge base:")
    
    # Add RAG results
    if rag_results:
        response_parts.append("\n\n**Relevant Information:**")
        for result in rag_results[:3]:  # Limit to top 3 results
            response_parts.append(f"• {result}")
    
    # Add data-specific insights if available
    if data is not None:
        if "correlation" in question.lower():
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) >= 2:
                corr_matrix = data[numeric_cols].corr()
                high_corr = []
                for i in range(len(corr_matrix.columns)):
                    for j in range(i+1, len(corr_matrix.columns)):
                        if abs(corr_matrix.iloc[i, j]) > 0.7:
                            high_corr.append(f"{corr_matrix.columns[i]} and {corr_matrix.columns[j]} ({corr_matrix.iloc[i, j]:.2f})")
                
                if high_corr:
                    response_parts.append(f"\n\n**Data Insights:** Strong correlations found between: {', '.join(high_corr[:2])}")
        
        elif "summary" in question.lower() or "overview" in question.lower():
            response_parts.append(f"\n\n**Dataset Summary:**")
            response_parts.append(f"• {data.shape[0]} records with {data.shape[1]} variables")
            response_parts.append(f"• Missing values: {data.isnull().sum().sum()}")
            response_parts.append(f"• Data types: {dict(data.dtypes.value_counts())}")
    
    # Add recommendations
    response_parts.append("\n\n**Recommendations:**")
    if "improvement" in question.lower():
        response_parts.append("• Implement continuous monitoring systems")
        response_parts.append("• Use data-driven decision making")
        response_parts.append("• Regular staff training and feedback")
    elif "automation" in question.lower():
        response_parts.append("• Consider AI-powered workflow automation")
        response_parts.append("• Implement predictive analytics for risk management")
        response_parts.append("• Use real-time monitoring dashboards")
    else:
        response_parts.append("• Regular quality assessments")
        response_parts.append("• Evidence-based practice implementation")
        response_parts.append("• Stakeholder engagement and communication")
    
    return "\n".join(response_parts)

def main():
    """Main application entry point"""
    try:
        create_ui()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        logger.error(f"Application error: {str(e)}")

if __name__ == "__main__":
    main()
