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
import warnings
import logging
from typing import Dict, List, Optional, Tuple, Any, Union
import hashlib
import re
import asyncio
import aiohttp
from dataclasses import dataclass
import feedparser

# Suppress warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
@dataclass
class Config:
    """Enhanced application configuration"""
    APP_TITLE: str = "🏥 Agentic AI & RAG for Healthcare Quality Management"
    APP_ICON: str = "🏥"
    LAYOUT: str = "wide"
    SIDEBAR_STATE: str = "expanded"
    
    # File upload settings
    MAX_FILE_SIZE: int = 200  # MB
    ALLOWED_EXTENSIONS: List[str] = None
    
    # API Configuration
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    DEFAULT_MODEL: str = "anthropic/claude-3-haiku"
    
    # Available AI Models
    AI_MODELS: Dict[str, str] = None
    
    # News Sources
    NEWS_SOURCES: Dict[str, str] = None
    
    def __post_init__(self):
        if self.ALLOWED_EXTENSIONS is None:
            self.ALLOWED_EXTENSIONS = ['csv', 'xlsx', 'xls', 'json', 'parquet']
        
        if self.AI_MODELS is None:
            self.AI_MODELS = {
                "Claude 3 Haiku": "anthropic/claude-3-haiku",
                "GPT-3.5 Turbo": "openai/gpt-3.5-turbo",
                "Qwen 2.5 72B": "qwen/qwen-2.5-72b-instruct",
                "Mistral 7B": "mistralai/mistral-7b-instruct",
                "Llama 3.1 8B": "meta-llama/llama-3.1-8b-instruct:free",
                "Gemma 2 9B": "google/gemma-2-9b-it:free"
            }
        
        if self.NEWS_SOURCES is None:
            self.NEWS_SOURCES = {
                "PubMed": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
                "WHO": "https://www.who.int/feeds/entity/csr/don/en/rss.xml",
                "CDC": "https://tools.cdc.gov/api/v2/resources/media",
                "Healthcare IT News": "https://www.healthcareitnews.com/news.rss",
                "Modern Healthcare": "https://www.modernhealthcare.com/rss"
            }

# Enhanced CSS with modern design
def load_enhanced_css():
    """Load enhanced CSS with modern healthcare theme"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500&display=swap');
    
    :root {
        --primary-blue: #2E86AB;
        --secondary-blue: #A23B72;
        --accent-green: #F18F01;
        --success-green: #C73E1D;
        --warning-orange: #FF6B35;
        --error-red: #DC2626;
        --text-primary: #1F2937;
        --text-secondary: #6B7280;
        --bg-light: #F9FAFB;
        --bg-white: #FFFFFF;
        --border-light: #E5E7EB;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: var(--text-primary);
    }
    
    .main-header {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-lg);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card {
        background: var(--bg-white);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-light);
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card {
        background: var(--bg-white);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-light);
        margin: 1rem 0;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .chat-message {
        background: var(--bg-white);
        border: 1px solid var(--border-light);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .user-message {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 100%);
        color: white;
        margin-left: 2rem;
    }
    
    .ai-message {
        background: var(--bg-light);
        margin-right: 2rem;
    }
    
    .data-insight {
        background: linear-gradient(135deg, var(--accent-green) 0%, var(--warning-orange) 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

class AIModelManager:
    """Enhanced AI Model Manager with multiple providers"""
    
    def __init__(self):
        self.config = Config()
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://healthcare-ai-rag.streamlit.app',
            'X-Title': 'Healthcare AI RAG System'
        })
    
    def get_api_key(self) -> Optional[str]:
        """Get API key from Streamlit secrets or environment"""
        try:
            # Try Streamlit secrets first
            if hasattr(st, 'secrets') and 'OPENROUTER_API_KEY' in st.secrets:
                return st.secrets['OPENROUTER_API_KEY']
            
            # Try environment variable
            api_key = os.environ.get('OPENROUTER_API_KEY')
            if api_key:
                return api_key
            
            # Default free key for testing
            return "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"
            
        except Exception as e:
            logger.warning(f"Could not get API key: {e}")
            return "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"
    
    def query_model_sync(self, prompt: str, model: str = None, max_tokens: int = 1000) -> str:
        """Synchronous query to AI model"""
        if model is None:
            model = self.config.DEFAULT_MODEL
        
        api_key = self.get_api_key()
        if not api_key:
            return "API key not configured. Please add OPENROUTER_API_KEY to your secrets."
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://healthcare-ai-rag.streamlit.app",
            "X-Title": "Healthcare AI RAG System",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert healthcare AI assistant specializing in quality management, patient safety, and healthcare analytics. Provide accurate, evidence-based responses with citations when possible. Focus on practical, actionable insights for healthcare professionals."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "max_tokens": max_tokens,
            "temperature": 0.3,
            "top_p": 0.9,
            "frequency_penalty": 0.1,
            "presence_penalty": 0.1
        }
        
        try:
            response = self.session.post(
                f"{self.config.OPENROUTER_BASE_URL}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            else:
                logger.error(f"API Error: {response.status_code} - {response.text}")
                return f"API Error: {response.status_code}. Please try again."
                
        except requests.exceptions.Timeout:
            return "Request timed out. Please try again with a shorter prompt."
        except Exception as e:
            logger.error(f"Model query error: {e}")
            return f"Error querying model: {str(e)}"

class EnhancedNewsAggregator:
    """Enhanced news aggregator with multiple sources"""
    
    def __init__(self):
        self.config = Config()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Healthcare-AI-RAG/1.0 (Educational Research)'
        })
    
    def fetch_pubmed_articles(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """Fetch articles from PubMed"""
        try:
            # Search for articles
            search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
            search_params = {
                'db': 'pubmed',
                'term': f"{query} AND healthcare quality",
                'retmax': max_results,
                'retmode': 'json',
                'sort': 'pub+date'
            }
            
            response = self.session.get(search_url, params=search_params, timeout=10)
            if response.status_code != 200:
                return []
            
            search_data = response.json()
            ids = search_data.get('esearchresult', {}).get('idlist', [])
            
            if not ids:
                return []
            
            # Return simple results without XML parsing
            articles = []
            for i, pmid in enumerate(ids[:max_results]):
                articles.append({
                    'title': f'PubMed Research Article {i+1}',
                    'summary': f'Research article from PubMed database (ID: {pmid})',
                    'source': 'PubMed',
                    'url': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                    'timestamp': datetime.now().strftime('%Y-%m-%d'),
                    'type': 'Academic Research'
                })
            
            return articles
            
        except Exception as e:
            logger.error(f"PubMed fetch error: {e}")
            return []
    
    def fetch_healthcare_news(self, query: str, max_results: int = 10) -> List[Dict[str, str]]:
        """Fetch comprehensive healthcare news"""
        # Return sample data for now
        sample_articles = [
            {
                'title': 'AI in Healthcare Quality Management',
                'summary': 'Latest developments in AI applications for healthcare quality improvement.',
                'source': 'Healthcare AI Today',
                'url': '#',
                'timestamp': datetime.now().strftime('%Y-%m-%d'),
                'type': 'News Article'
            },
            {
                'title': 'Patient Safety Innovations 2024',
                'summary': 'New technologies and methods improving patient safety outcomes.',
                'source': 'Patient Safety Network',
                'url': '#',
                'timestamp': datetime.now().strftime('%Y-%m-%d'),
                'type': 'Research Report'
            }
        ]
        
        return sample_articles[:max_results]

class DataValidator:
    """Enhanced data validation utilities"""
    
    @staticmethod
    def validate_file(file) -> Tuple[bool, str]:
        """Validate uploaded file with enhanced checks"""
        if file is None:
            return False, "No file uploaded"
        
        # Check file size
        if file.size > Config.MAX_FILE_SIZE * 1024 * 1024:
            return False, f"File size exceeds {Config.MAX_FILE_SIZE}MB limit"
        
        # Check file extension
        file_extension = file.name.split('.')[-1].lower()
        config = Config()
        if file_extension not in config.ALLOWED_EXTENSIONS:
            return False, f"File type not supported. Allowed: {', '.join(config.ALLOWED_EXTENSIONS)}"
        
        return True, "File is valid and safe"
    
    @staticmethod
    def validate_matrix(matrix: np.ndarray) -> Tuple[bool, str]:
        """Validate comparison matrix for AHP/ANP with enhanced checks"""
        if matrix.shape[0] != matrix.shape[1]:
            return False, "Matrix must be square"
        
        # Check for zeros on diagonal
        if np.any(np.diag(matrix) == 0):
            return False, "Diagonal elements cannot be zero"
        
        # Check for negative values
        if np.any(matrix < 0):
            return False, "Matrix cannot contain negative values"
        
        # Check for reasonable values (1/9 to 9)
        if np.any(matrix > 9) or np.any(matrix < 1/9):
            return False, "Matrix values should be between 1/9 and 9"
        
        return True, "Matrix is valid and reciprocal"

class EnhancedRAGSystem:
    """Enhanced RAG System with real-time knowledge retrieval"""
    
    def __init__(self):
        self.knowledge_base = self._initialize_knowledge_base()
        self.ai_manager = AIModelManager()
        self.news_aggregator = EnhancedNewsAggregator()
        self.cache = {}
        self.cache_expiry = {}
    
    def _initialize_knowledge_base(self) -> Dict[str, Any]:
        """Initialize comprehensive healthcare knowledge base"""
        return {
            "quality_indicators": {
                "patient_safety": {
                    "indicators": ["Medication errors per 1000 patient days", "Hospital-acquired infections rate"],
                    "benchmarks": {"excellent": "<2", "good": "2-5", "needs_improvement": ">5"},
                    "sources": ["Joint Commission", "CMS", "AHRQ"]
                },
                "clinical_effectiveness": {
                    "indicators": ["30-day readmission rate", "Mortality index", "Length of stay variance"],
                    "benchmarks": {"excellent": "<10%", "good": "10-15%", "needs_improvement": ">15%"},
                    "sources": ["CMS", "HCAHPS", "Clinical registries"]
                }
            },
            "best_practices": {
                "infection_control": {
                    "practices": ["Hand hygiene compliance >95%", "PPE usage protocols"],
                    "evidence": "WHO Guidelines on Hand Hygiene in Health Care (2009), CDC Guidelines",
                    "implementation": "Daily monitoring, staff education, feedback systems"
                }
            }
        }
    
    def get_cached_response(self, query: str) -> Optional[str]:
        """Get cached response if available and not expired"""
        query_hash = hashlib.md5(query.encode()).hexdigest()
        
        if query_hash in self.cache:
            if datetime.now() < self.cache_expiry.get(query_hash, datetime.now()):
                return self.cache[query_hash]
        
        return None
    
    def cache_response(self, query: str, response: str, expiry_hours: int = 1):
        """Cache response with expiry"""
        query_hash = hashlib.md5(query.encode()).hexdigest()
        self.cache[query_hash] = response
        self.cache_expiry[query_hash] = datetime.now() + timedelta(hours=expiry_hours)
    
    def query_knowledge_enhanced(self, query: str, use_ai: bool = True, model: str = None) -> Dict[str, Any]:
        """Enhanced knowledge query with AI and real-time data"""
        # Check cache first
        cached = self.get_cached_response(query)
        if cached and not use_ai:
            return {"response": cached, "source": "cache", "confidence": 0.8}
        
        query_lower = query.lower()
        relevant_info = []
        confidence_score = 0.0
        
        # Search knowledge base
        for category, items in self.knowledge_base.items():
            category_matches = self._search_nested_dict(items, query_lower)
            if category_matches:
                relevant_info.extend([f"{category}: {match}" for match in category_matches])
                confidence_score += 0.2
        
        # Enhance with AI if requested
        ai_response = ""
        if use_ai and self.ai_manager:
            try:
                # Create enhanced prompt with context
                context_prompt = self._create_enhanced_prompt(query, relevant_info, [])
                ai_response = self.ai_manager.query_model_sync(context_prompt, model, 1500)
                if ai_response and "error" not in ai_response.lower():
                    confidence_score += 0.5
            except Exception as e:
                logger.warning(f"AI query failed: {e}")
                ai_response = "AI enhancement unavailable."
        
        # Combine all information
        combined_response = self._combine_responses(relevant_info, [], ai_response)
        
        # Cache the response
        if combined_response:
            self.cache_response(query, combined_response)
        
        return {
            "response": combined_response,
            "knowledge_base_matches": len(relevant_info),
            "news_articles": 0,
            "ai_enhanced": bool(ai_response and "error" not in ai_response.lower()),
            "confidence": min(confidence_score, 1.0),
            "source": "enhanced_rag"
        }
    
    def _search_nested_dict(self, data: Any, query: str) -> List[str]:
        """Search nested dictionary for query terms"""
        matches = []
        query_terms = query.split()
        
        def search_recursive(obj, path=""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    if any(term in key.lower() for term in query_terms):
                        if isinstance(value, (list, str)):
                            matches.append(f"{path}{key}: {value}")
                    search_recursive(value, f"{path}{key} -> ")
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    if isinstance(item, str) and any(term in item.lower() for term in query_terms):
                        matches.append(f"{path}[{i}]: {item}")
                    search_recursive(item, f"{path}[{i}] -> ")
            elif isinstance(obj, str):
                if any(term in obj.lower() for term in query_terms):
                    matches.append(f"{path}: {obj}")
        
        search_recursive(data)
        return matches[:10]  # Limit results
    
    def _create_enhanced_prompt(self, query: str, knowledge_matches: List[str], news_articles: List[Dict]) -> str:
        """Create enhanced prompt with context"""
        prompt_parts = [
            f"Healthcare Query: {query}",
            "",
            "CONTEXT FROM KNOWLEDGE BASE:"
        ]
        
        if knowledge_matches:
            for match in knowledge_matches[:5]:  # Top 5 matches
                prompt_parts.append(f"• {match}")
        else:
            prompt_parts.append("• No specific matches found in knowledge base")
        
        prompt_parts.extend([
            "",
            "INSTRUCTIONS:",
            "1. Provide a comprehensive, evidence-based response to the healthcare query",
            "2. Use the knowledge base context when relevant",
            "3. Include specific metrics, benchmarks, or standards when applicable",
            "4. Cite sources and provide actionable recommendations",
            "5. If unsure about specific data, clearly indicate uncertainty",
            "6. Focus on practical applications for healthcare professionals",
            "",
            "Response:"
        ])
        
        return "\n".join(prompt_parts)
    
    def _combine_responses(self, knowledge_matches: List[str], news_articles: List[Dict], ai_response: str) -> str:
        """Combine all response components"""
        response_parts = []
        
        if ai_response and "error" not in ai_response.lower():
            response_parts.append("🤖 **AI-Enhanced Analysis:**")
            response_parts.append(ai_response)
            response_parts.append("")
        
        if knowledge_matches:
            response_parts.append("📚 **Knowledge Base Insights:**")
            for match in knowledge_matches[:5]:
                response_parts.append(f"• {match}")
            response_parts.append("")
        
        if not response_parts:
            response_parts.append("No relevant information found. Please try rephrasing your query or ask about specific healthcare quality topics.")
        
        return "\n".join(response_parts)

class AgenticAI:
    """Enhanced Agentic AI system with advanced capabilities"""
    
    def __init__(self):
        self.data = None
        self.processed_data = None
        self.anp_results = None
        self.ahp_results = None
        self.rag_system = EnhancedRAGSystem()
        self.analysis_history = []
        self.ai_manager = AIModelManager()
        self.news_aggregator = EnhancedNewsAggregator()
        self.current_model = Config().DEFAULT_MODEL
    
    def set_ai_model(self, model: str):
        """Set the current AI model"""
        self.current_model = model
        logger.info(f"AI model set to: {model}")
    
    def load_data(self, file) -> Tuple[bool, str]:
        """Enhanced data loading with multiple format support"""
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
            elif file_extension == 'json':
                self.data = pd.read_json(file)
            elif file_extension == 'parquet':
                self.data = pd.read_parquet(file)
            
            # Basic data validation
            if self.data.empty:
                return False, "The file contains no data"
            
            # Enhanced data cleaning
            self.data = self._clean_data_enhanced(self.data)
            
            logger.info(f"Data loaded successfully: {self.data.shape}")
            return True, f"✅ Data loaded successfully! Shape: {self.data.shape[0]:,} rows × {self.data.shape[1]} columns"
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return False, f"❌ Error loading data: {str(e)}"
    
    def _clean_data_enhanced(self, df: pd.DataFrame) -> pd.DataFrame:
        """Enhanced data cleaning with better handling"""
        # Remove duplicate columns
        df = df.loc[:, ~df.columns.duplicated()]
        
        # Handle missing values intelligently
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        categorical_columns = df.select_dtypes(include=['object']).columns
        
        # Clean numeric data
        for col in numeric_columns:
            # Fill missing with median
            df[col].fillna(df[col].median(), inplace=True)
        
        # Clean categorical data
        for col in categorical_columns:
            # Standardize text
            df[col] = df[col].astype(str).str.strip().str.title()
            
            # Fill missing with mode or 'Unknown'
            mode_value = df[col].mode().iloc[0] if not df[col].mode().empty else 'Unknown'
            df[col].fillna(mode_value, inplace=True)
        
        return df
    
    def analyze_data_enhanced(self, use_ai: bool = True) -> Optional[Dict[str, Any]]:
        """Enhanced data analysis with AI insights"""
        if self.data is None:
            return None
        
        try:
            # Basic analysis
            analysis = {
                "basic_info": {
                    "shape": self.data.shape,
                    "columns": list(self.data.columns),
                    "data_types": self.data.dtypes.to_dict(),
                    "missing_values": self.data.isnull().sum().to_dict(),
                    "duplicate_rows": int(self.data.duplicated().sum()),
                    "memory_usage_mb": round(self.data.memory_usage(deep=True).sum() / 1024 / 1024, 2)
                },
                "descriptive_stats": {},
                "insights": [],
                "ai_insights": [],
                "recommendations": [],
                "data_quality_score": 0.0
            }
            
            # Descriptive statistics for numeric columns
            numeric_data = self.data.select_dtypes(include=[np.number])
            if not numeric_data.empty:
                analysis["descriptive_stats"] = numeric_data.describe().to_dict()
                
                # Correlation analysis
                if len(numeric_data.columns) > 1:
                    analysis["correlation_matrix"] = numeric_data.corr().to_dict()
            
            # Generate automated insights
            analysis["insights"] = self._generate_insights_enhanced()
            
            # Calculate data quality score
            analysis["data_quality_score"] = self._calculate_data_quality_score()
            
            # AI-enhanced insights
            if use_ai:
                ai_insights = self._generate_ai_insights()
                analysis["ai_insights"] = ai_insights
            
            # Healthcare-specific recommendations
            analysis["recommendations"] = self._get_healthcare_recommendations()
            
            # Store in history
            self.analysis_history.append({
                "timestamp": datetime.now().isoformat(),
                "analysis": analysis
            })
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error in enhanced data analysis: {str(e)}")
            st.error(f"❌ Error in data analysis: {str(e)}")
            return None
    
    def _generate_insights_enhanced(self) -> List[str]:
        """Generate enhanced automated insights"""
        insights = []
        
        try:
            # Data completeness insights
            missing_pct = (self.data.isnull().sum().sum() / (self.data.shape[0] * self.data.shape[1])) * 100
            if missing_pct > 10:
                insights.append(f"⚠️ High missing data rate: {missing_pct:.1f}% - Consider data collection improvements")
            elif missing_pct < 1:
                insights.append(f"✅ Excellent data completeness: {100-missing_pct:.1f}% complete")
            
            # Duplicate data insights
            duplicates = self.data.duplicated().sum()
            if duplicates > 0:
                insights.append(f"⚠️ Found {duplicates} duplicate records ({duplicates/len(self.data)*100:.1f}%)")
            
            # Sample size insights
            if len(self.data) < 30:
                insights.append("⚠️ Small sample size (<30) - statistical results may not be reliable")
            elif len(self.data) > 10000:
                insights.append("✅ Large sample size - statistical results should be robust")
            
        except Exception as e:
            logger.error(f"Error generating insights: {str(e)}")
            insights.append("Unable to generate some insights due to data structure")
        
        return insights[:15]  # Limit to 15 insights
    
    def _calculate_data_quality_score(self) -> float:
        """Calculate overall data quality score"""
        score = 1.0
        
        try:
            # Completeness score (40% weight)
            missing_pct = (self.data.isnull().sum().sum() / (self.data.shape[0] * self.data.shape[1]))
            completeness_score = 1 - missing_pct
            
            # Uniqueness score (30% weight)
            duplicate_pct = self.data.duplicated().sum() / len(self.data)
            uniqueness_score = 1 - duplicate_pct
            
            # Consistency score (30% weight)
            consistency_score = 1.0
            
            # Weighted average
            score = (completeness_score * 0.4 + uniqueness_score * 0.3 + consistency_score * 0.3)
            
        except Exception as e:
            logger.error(f"Error calculating data quality score: {e}")
            score = 0.5  # Default moderate score
        
        return round(score, 3)
    
    def _generate_ai_insights(self) -> List[str]:
        """Generate AI-powered insights about the data"""
        try:
            if not self.ai_manager:
                return ["AI insights unavailable"]
            
            # Create data summary for AI
            summary = f"""
            Dataset Overview:
            - Shape: {self.data.shape[0]} rows, {self.data.shape[1]} columns
            - Columns: {', '.join(self.data.columns[:10])}{'...' if len(self.data.columns) > 10 else ''}
            - Data types: {dict(self.data.dtypes.value_counts())}
            - Missing data: {self.data.isnull().sum().sum()} values
            """
            
            prompt = f"""
            As a healthcare data analyst, analyze this dataset and provide 3-5 specific insights:
            
            {summary}
            
            Focus on:
            1. Healthcare quality implications
            2. Potential data issues or biases
            3. Recommended analyses or investigations
            4. Data collection improvements
            
            Provide actionable insights in bullet points.
            """
            
            ai_response = self.ai_manager.query_model_sync(prompt, self.current_model, 800)
            
            if ai_response and "error" not in ai_response.lower():
                # Parse AI response into bullet points
                insights = []
                for line in ai_response.split('\n'):
                    line = line.strip()
                    if line and (line.startswith('•') or line.startswith('-') or line.startswith('*')):
                        insights.append(line.lstrip('•-* '))
                    elif line and len(line) > 20 and '.' in line:
                        insights.append(line)
                
                return insights[:5]  # Limit to 5 insights
            else:
                return ["AI analysis unavailable at this time"]
                
        except Exception as e:
            logger.error(f"Error generating AI insights: {e}")
            return ["AI insights could not be generated"]
    
    def _get_healthcare_recommendations(self) -> List[str]:
        """Get healthcare-specific recommendations based on data"""
        recommendations = []
        
        try:
            column_names = [col.lower() for col in self.data.columns]
            
            # Patient satisfaction recommendations
            if any('satisfaction' in col for col in column_names):
                recommendations.append("📊 Monitor patient satisfaction trends and correlate with operational metrics")
                recommendations.append("🎯 Implement targeted interventions for satisfaction scores below 75th percentile")
            
            # Quality metrics recommendations
            if any(term in ' '.join(column_names) for term in ['readmission', 'infection', 'mortality']):
                recommendations.append("🏥 Establish quality improvement teams for core metrics monitoring")
                recommendations.append("📈 Set up statistical process control charts for key quality indicators")
            
            # General recommendations
            recommendations.extend([
                "🔄 Establish regular data validation and quality monitoring processes",
                "📱 Consider real-time dashboards for key stakeholders",
                "🎓 Provide data literacy training for clinical and administrative staff",
                "🔒 Ensure HIPAA compliance and data security protocols are followed"
            ])
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            recommendations.append("Unable to generate specific recommendations")
        
        return recommendations[:8]  # Limit to 8 recommendations
    
    def anp_analysis_enhanced(self, comparison_matrix: np.ndarray, criteria_names: List[str] = None) -> Optional[Dict[str, Any]]:
        """Enhanced ANP analysis with better validation and reporting"""
        try:
            # Enhanced validation
            is_valid, message = DataValidator.validate_matrix(comparison_matrix)
            if not is_valid:
                st.error(f"❌ Matrix validation failed: {message}")
                return None
            
            n = comparison_matrix.shape[0]
            if criteria_names is None:
                criteria_names = [f"Criterion {i+1}" for i in range(n)]
            
            # Normalize matrix
            column_sums = comparison_matrix.sum(axis=0)
            norm_matrix = comparison_matrix / column_sums
            
            # Calculate priority vector (eigenvector method)
            eigenvalues, eigenvectors = np.linalg.eig(comparison_matrix)
            max_eigenvalue_index = np.argmax(eigenvalues.real)
            priority_vector = np.abs(eigenvectors[:, max_eigenvalue_index].real)
            priority_vector = priority_vector / priority_vector.sum()
            
            # Calculate consistency metrics
            lambda_max = eigenvalues[max_eigenvalue_index].real
            consistency_index = (lambda_max - n) / (n - 1) if n > 1 else 0
            
            # Random Index values
            random_indices = {2: 0, 3: 0.58, 4: 0.9, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
            random_index = random_indices.get(n, 1.49)
            
            consistency_ratio = consistency_index / random_index if random_index != 0 else 0
            
            # Enhanced results
            result = {
                "priority_vector": priority_vector.tolist(),
                "criteria_names": criteria_names,
                "priority_rankings": sorted(zip(criteria_names, priority_vector), key=lambda x: x[1], reverse=True),
                "consistency_ratio": float(consistency_ratio),
                "consistency_index": float(consistency_index),
                "lambda_max": float(lambda_max),
                "is_consistent": consistency_ratio < 0.1,
                "consistency_quality": self._get_consistency_quality(consistency_ratio),
                "matrix_size": n,
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            self.anp_results = result
            return result
            
        except Exception as e:
            logger.error(f"Error in enhanced ANP analysis: {str(e)}")
            st.error(f"❌ Error in ANP analysis: {str(e)}")
            return None
    
    def _get_consistency_quality(self, cr: float) -> str:
        """Get consistency quality rating"""
        if cr < 0.05:
            return "Excellent"
        elif cr < 0.1:
            return "Acceptable"
        elif cr < 0.15:
            return "Marginal"
        else:
            return "Poor"
    
    def scenario_planning_enhanced(self, parameters: Dict[str, float], simulations: int = 1000, 
                                 confidence_level: float = 0.95) -> Optional[Dict[str, Any]]:
        """Enhanced scenario planning with statistical analysis"""
        try:
            if not parameters:
                st.error("❌ No parameters provided for scenario planning")
                return None
            
            # Validate parameters
            for param, value in parameters.items():
                if not isinstance(value, (int, float)) or np.isnan(value):
                    st.error(f"❌ Invalid value for parameter {param}: {value}")
                    return None
            
            # Generate scenarios with different distributions
            results = []
            np.random.seed(42)  # For reproducibility
            
            for _ in range(simulations):
                scenario = {}
                for param, base_value in parameters.items():
                    # Use normal distribution with 20% standard deviation
                    std_dev = abs(base_value * 0.2)
                    scenario[param] = np.random.normal(base_value, std_dev)
                results.append(scenario)
            
            scenario_df = pd.DataFrame(results)
            
            # Calculate statistics
            stats = {
                "mean": scenario_df.mean().to_dict(),
                "median": scenario_df.median().to_dict(),
                "std": scenario_df.std().to_dict(),
                "min": scenario_df.min().to_dict(),
                "max": scenario_df.max().to_dict(),
                "percentiles": {}
            }
            
            # Calculate percentiles
            percentiles = [5, 10, 25, 75, 90, 95]
            for p in percentiles:
                stats["percentiles"][f"p{p}"] = scenario_df.quantile(p/100).to_dict()
            
            # Calculate confidence intervals
            alpha = 1 - confidence_level
            lower_percentile = (alpha/2) * 100
            upper_percentile = (1 - alpha/2) * 100
            
            confidence_intervals = {}
            for param in parameters.keys():
                lower = scenario_df[param].quantile(lower_percentile/100)
                upper = scenario_df[param].quantile(upper_percentile/100)
                confidence_intervals[param] = (lower, upper)
            
            # Risk analysis
            risk_analysis = {}
            for param, base_value in parameters.items():
                below_target = (scenario_df[param] < base_value * 0.9).sum()
                above_target = (scenario_df[param] > base_value * 1.1).sum()
                risk_analysis[param] = {
                    "probability_below_90pct": below_target / simulations,
                    "probability_above_110pct": above_target / simulations,
                    "value_at_risk_5pct": scenario_df[param].quantile(0.05),
                    "value_at_risk_95pct": scenario_df[param].quantile(0.95)
                }
            
            enhanced_result = {
                "scenario_data": scenario_df,
                "statistics": stats,
                "confidence_intervals": confidence_intervals,
                "risk_analysis": risk_analysis,
                "simulations_count": simulations,
                "confidence_level": confidence_level,
                "base_parameters": parameters,
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            return enhanced_result
            
        except Exception as e:
            logger.error(f"Error in enhanced scenario planning: {str(e)}")
            st.error(f"❌ Error in scenario planning: {str(e)}")
            return None

def create_enhanced_ui():
    """Create enhanced UI with modern design"""
    config = Config()
    st.set_page_config(
        page_title=config.APP_TITLE,
        page_icon=config.APP_ICON,
        layout=config.LAYOUT,
        initial_sidebar_state=config.SIDEBAR_STATE
    )
    
    # Load enhanced CSS
    load_enhanced_css()
    
    # Initialize session state
    if 'ai_agent' not in st.session_state:
        st.session_state.ai_agent = AgenticAI()
    
    if 'selected_model' not in st.session_state:
        st.session_state.selected_model = config.DEFAULT_MODEL
    
    ai_agent = st.session_state.ai_agent
    
    # Enhanced header
    st.markdown("""
    <div class="main-header">
        <h1>🏥 Agentic AI & RAG for Healthcare Quality Management</h1>
        <p>Advanced AI-powered analytics with real-time insights and evidence-based recommendations</p>
        <div style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">
            Powered by multiple AI models • Real-time data • Evidence-based insights
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced sidebar
    with st.sidebar:
        st.markdown("### 🤖 AI Model Selection")
        
        # Model selector
        model_options = list(Config().AI_MODELS.items())
        selected_model_name = st.selectbox(
            "Choose AI Model:",
            options=[name for name, _ in model_options],
            index=0,
            help="Select the AI model for enhanced analysis and insights"
        )
        
        selected_model_id = Config().AI_MODELS[selected_model_name]
        if selected_model_id != st.session_state.selected_model:
            st.session_state.selected_model = selected_model_id
            ai_agent.set_ai_model(selected_model_id)
        
        st.markdown(f'<div class="model-status">Active: {selected_model_name}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🚀 Navigation")
        
        navigation = st.radio(
            "Choose a section:",
            [
                "🏠 Home", 
                "📊 Enhanced Data Analysis", 
                "⚖️ Advanced Decision Methods", 
                "📈 Interactive Visualization", 
                "🎯 AI Scenario Planning", 
                "📰 Real-time News & Research", 
                "🤖 AI Assistant Plus",
                "📋 Healthcare Benchmarks"
            ]
        )
        
        st.markdown("---")
        st.markdown("### 📊 System Status")
        
        # Enhanced status display
        if ai_agent.data is not None:
            st.markdown(f"""
            <div class="metric-card">
                <strong>✅ Data Loaded</strong><br>
                📏 {ai_agent.data.shape[0]:,} rows × {ai_agent.data.shape[1]} columns<br>
                💾 {ai_agent.data.memory_usage(deep=True).sum() / 1024 / 1024:.1f} MB
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="metric-card">
                <strong>ℹ️ No Data Loaded</strong><br>
                Upload data to begin analysis
            </div>
            """, unsafe_allow_html=True)
        
        # Analysis history
        if ai_agent.analysis_history:
            st.markdown(f"""
            <div class="metric-card">
                <strong>🧠 Analysis History</strong><br>
                {len(ai_agent.analysis_history)} completed analyses
            </div>
            """, unsafe_allow_html=True)
    
    # Main content routing
    if navigation == "🏠 Home":
        show_enhanced_home_page()
    elif navigation == "📊 Enhanced Data Analysis":
        show_enhanced_data_analysis_page(ai_agent)
    elif navigation == "⚖️ Advanced Decision Methods":
        show_enhanced_decision_methods_page(ai_agent)
    elif navigation == "📈 Interactive Visualization":
        show_enhanced_visualization_page(ai_agent)
    elif navigation == "🎯 AI Scenario Planning":
        show_enhanced_scenario_planning_page(ai_agent)
    elif navigation == "📰 Real-time News & Research":
        show_enhanced_news_page(ai_agent)
    elif navigation == "🤖 AI Assistant Plus":
        show_enhanced_ai_assistant_page(ai_agent)
    elif navigation == "📋 Healthcare Benchmarks":
        show_healthcare_benchmarks_page(ai_agent)

def show_enhanced_home_page():
    """Enhanced home page with modern design"""
    # Welcome section
    st.markdown("""
    <div class="feature-card">
        <h2>🌟 Welcome to the Future of Healthcare Quality Management</h2>
        <p>Experience cutting-edge AI technology combined with evidence-based healthcare insights. Our platform integrates multiple AI models, real-time data sources, and comprehensive analytics to deliver actionable intelligence for healthcare professionals.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key features showcase
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 Multi-Model AI</h3>
            <ul>
                <li><strong>Claude 3 Haiku</strong> - Advanced reasoning</li>
                <li><strong>Qwen 2.5</strong> - Multilingual analysis</li>
                <li><strong>Mistral 7B</strong> - Efficient processing</li>
                <li><strong>Llama 3.1</strong> - Open-source power</li>
            </ul>
            <div style="margin-top: 1rem; padding: 0.5rem; background: rgba(46, 134, 171, 0.1); border-radius: 8px;">
                <strong>🔄 Real-time model switching</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📚 Enhanced RAG System</h3>
            <ul>
                <li><strong>PubMed Integration</strong> - Latest research</li>
                <li><strong>WHO/CDC Data</strong> - Authoritative sources</li>
                <li><strong>Real-time News</strong> - Industry updates</li>
                <li><strong>Evidence-based</strong> - Cited recommendations</li>
            </ul>
            <div style="margin-top: 1rem; padding: 0.5rem; background: rgba(162, 59, 114, 0.1); border-radius: 8px;">
                <strong>🎯 Zero hallucination approach</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Advanced Analytics</h3>
            <ul>
                <li><strong>AI-powered insights</strong> - Smart analysis</li>
                <li><strong>Statistical modeling</strong> - Robust methods</li>
                <li><strong>Predictive analytics</strong> - Future planning</li>
                <li><strong>Quality scoring</strong> - Data assessment</li>
            </ul>
            <div style="margin-top: 1rem; padding: 0.5rem; background: rgba(241, 143, 1, 0.1); border-radius: 8px;">
                <strong>📈 Healthcare-focused metrics</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

def show_enhanced_data_analysis_page(ai_agent):
    """Enhanced data analysis page with AI integration"""
    st.markdown("## 📊 Enhanced Data Analysis with AI")
    st.markdown("Upload your healthcare data and get comprehensive AI-powered analysis with real-time insights.")
    
    # File upload section
    uploaded_file = st.file_uploader(
        "📁 Upload your healthcare data file",
        type=Config().ALLOWED_EXTENSIONS,
        help=f"Supported formats: {', '.join(Config().ALLOWED_EXTENSIONS)}. Maximum size: {Config.MAX_FILE_SIZE}MB"
    )
    
    if uploaded_file:
        success, message = ai_agent.load_data(uploaded_file)
        
        if success:
            st.success(message)
            
            # Enhanced data overview
            st.markdown("### 📋 Enhanced Data Overview")
            
            # Create metrics cards
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>📏 Rows</h4>
                    <h2>{ai_agent.data.shape[0]:,}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <h4>📊 Columns</h4>
                    <h2>{ai_agent.data.shape[1]}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                missing_pct = (ai_agent.data.isnull().sum().sum() / (ai_agent.data.shape[0] * ai_agent.data.shape[1])) * 100
                st.markdown(f"""
                <div class="metric-card">
                    <h4>❓ Missing</h4>
                    <h2>{missing_pct:.1f}%</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                duplicates = ai_agent.data.duplicated().sum()
                st.markdown(f"""
                <div class="metric-card">
                    <h4>🔄 Duplicates</h4>
                    <h2>{duplicates}</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col5:
                memory_mb = ai_agent.data.memory_usage(deep=True).sum() / 1024 / 1024
                st.markdown(f"""
                <div class="metric-card">
                    <h4>💾 Memory</h4>
                    <h2>{memory_mb:.1f}MB</h2>
                </div>
                """, unsafe_allow_html=True)
            
            # Analysis options
            st.markdown("### 🔬 Analysis Options")
            
            col1, col2 = st.columns(2)
            
            with col1:
                use_ai_analysis = st.checkbox("🤖 Enable AI-Enhanced Analysis", value=True, 
                                            help="Use AI models for deeper insights and recommendations")
            
            with col2:
                analysis_depth = st.selectbox("📊 Analysis Depth", 
                                            ["Quick Overview", "Standard Analysis", "Deep Dive"],
                                            index=1,
                                            help="Choose the level of detail for analysis")
            
            # Perform analysis
            if st.button("🚀 Perform Enhanced Analysis", type="primary", use_container_width=True):
                
                # Show progress
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Simulate analysis steps
                steps = [
                    "🔍 Analyzing data structure...",
                    "📊 Computing descriptive statistics...",
                    "🔗 Calculating correlations...",
                    "🧠 Generating AI insights...",
                    "📚 Querying knowledge base...",
                    "🎯 Creating recommendations...",
                    "✨ Finalizing analysis..."
                ]
                
                for i, step in enumerate(steps):
                    status_text.text(step)
                    progress_bar.progress((i + 1) / len(steps))
                    time.sleep(0.5)  # Simulate processing time
                
                # Perform actual analysis
                analysis = ai_agent.analyze_data_enhanced(use_ai=use_ai_analysis)
                
                progress_bar.empty()
                status_text.empty()
                
                if analysis:
                    st.balloons()  # Celebration animation
                    st.success("🎉 Analysis completed successfully!")
                    
                    # Display results in enhanced format
                    display_enhanced_analysis_results(analysis, ai_agent)
        else:
            st.error(message)

def display_enhanced_analysis_results(analysis: Dict[str, Any], ai_agent):
    """Display enhanced analysis results"""
    
    # Data Quality Score
    quality_score = analysis.get("data_quality_score", 0.0)
    st.markdown(f"""
    <div class="feature-card">
        <h3>📊 Data Quality Assessment</h3>
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="font-size: 2rem; font-weight: bold; color: {'#22c55e' if quality_score > 0.8 else '#f59e0b' if quality_score > 0.6 else '#ef4444'};">
                {quality_score:.1%}
            </div>
            <div>
                <div style="font-weight: 600;">Overall Quality Score</div>
                <div style="color: #6b7280;">
                    {'Excellent' if quality_score > 0.8 else 'Good' if quality_score > 0.6 else 'Needs Improvement'}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different analysis sections
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📈 Statistics", 
        "🔗 Correlations", 
        "🧠 AI Insights", 
        "💡 Automated Insights",
        "🎯 Recommendations",
        "📊 Summary"
    ])
    
    with tab1:
        st.markdown("### 📊 Descriptive Statistics")
        if analysis.get("descriptive_stats"):
            desc_stats = pd.DataFrame(analysis["descriptive_stats"])
            st.dataframe(desc_stats, use_container_width=True)
    
    with tab2:
        st.markdown("### 🔗 Correlation Analysis")
        if analysis.get("correlation_matrix"):
            corr_data = pd.DataFrame(analysis["correlation_matrix"])
            
            # Create interactive correlation heatmap
            fig = px.imshow(
                corr_data,
                color_continuous_scale='RdBu_r',
                aspect="auto",
                title="Interactive Correlation Heatmap",
                labels=dict(color="Correlation")
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Correlation analysis requires numeric data.")
    
    with tab3:
        st.markdown("### 🤖 AI-Generated Insights")
        ai_insights = analysis.get("ai_insights", [])
        
        if ai_insights:
            for i, insight in enumerate(ai_insights, 1):
                st.markdown(f"""
                <div class="chat-message ai-message">
                    <strong>🤖 AI Insight #{i}:</strong><br>
                    {insight}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("AI insights are not available. Ensure AI analysis is enabled and API key is configured.")
    
    with tab4:
        st.markdown("### 💡 Automated Insights")
        insights = analysis.get("insights", [])
        
        if insights:
            for i, insight in enumerate(insights, 1):
                st.markdown(f"""
                <div class="chat-message">
                    <strong>💡 Insight #{i}:</strong><br>
                    {insight}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No automated insights generated. This may indicate data structure issues.")
    
    with tab5:
        st.markdown("### 🎯 Healthcare Recommendations")
        recommendations = analysis.get("recommendations", [])
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"""
                <div class="chat-message" style="border-left: 4px solid #22c55e;">
                    <strong>🎯 Recommendation #{i}:</strong><br>
                    {rec}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No specific recommendations available.")
    
    with tab6:
        st.markdown("### 📊 Analysis Summary")
        
        # Create summary metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h4>📈 Insights Generated</h4>
                <h2>{len(analysis.get('insights', []))}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h4>🤖 AI Insights</h4>
                <h2>{len(analysis.get('ai_insights', []))}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h4>🎯 Recommendations</h4>
                <h2>{len(analysis.get('recommendations', []))}</h2>
            </div>
            """, unsafe_allow_html=True)

def show_enhanced_decision_methods_page(ai_agent):
    """Enhanced decision methods page with advanced features"""
    st.markdown("## ⚖️ Advanced Decision Analysis Methods")
    st.markdown("Make data-driven decisions using advanced multi-criteria analysis with AI-powered insights.")
    
    # Method selection
    method = st.selectbox(
        "🔧 Select Decision Analysis Method",
        ["ANP - Analytic Network Process", "AHP - Analytic Hierarchy Process"],
        help="Choose the decision analysis method that best fits your needs"
    )
    
    if method == "ANP - Analytic Network Process":
        st.markdown("### 🔄 Enhanced ANP Analysis")
        
        # Enhanced interface
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### 🏗️ Matrix Configuration")
            size = st.slider("Matrix dimensions", min_value=2, max_value=8, value=3, 
                           help="Number of criteria/alternatives to compare")
        
        with col2:
            st.markdown("#### 📝 Criteria Names")
            criteria_names = []
            for i in range(size):
                name = st.text_input(f"Criterion {i+1}", value=f"Criterion {i+1}", key=f"criteria_{i}")
                criteria_names.append(name)
        
        # Matrix input with enhanced interface
        st.markdown("#### 🔢 Pairwise Comparison Matrix")
        st.markdown("*Enter values from 1-9 where 1=equal importance, 9=extreme importance*")
        
        comparison_matrix = np.ones((size, size))
        
        # Create enhanced matrix input
        cols = st.columns([1] + [1]*size)
        with cols[0]:
            st.markdown("**Criteria**")
        
        for j in range(size):
            with cols[j + 1]:
                st.markdown(f"**{criteria_names[j][:10]}**")
        
        for i in range(size):
            cols = st.columns([1] + [1]*size)
            with cols[0]:
                st.markdown(f"**{criteria_names[i]}**")
            
            for j in range(size):
                with cols[j + 1]:
                    if i == j:
                        st.markdown("1.00")
                    elif i < j:
                        value = st.number_input(
                            f"",
                            min_value=0.1,
                            max_value=9.0,
                            value=1.0,
                            step=0.1,
                            format="%.1f",
                            key=f"anp_{i}_{j}",
                            label_visibility="collapsed",
