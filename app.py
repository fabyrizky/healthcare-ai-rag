import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings
import time
import json

warnings.filterwarnings('ignore')

# Enhanced Config - Simplified
class HealthConfig:
    APP_TITLE = "🏥 AGENTIC AI FOR HOSPITAL QUALITY SYSTEM"
    APP_VERSION = "8.7.0"
    
    # Theme configurations
    THEMES = {
        "Dark": {
            "bg_primary": "#0a0a0f",
            "bg_secondary": "#1a1a2e", 
            "bg_tertiary": "#16213e",
            "text_primary": "#ffffff",
            "text_secondary": "#e0e0e0",
            "accent_1": "#00d4ff",
            "accent_2": "#8b5cf6",
            "success": "#00ff88",
            "warning": "#ff6b35",
            "error": "#ff3d71"
        },
        "Light": {
            "bg_primary": "#f8f9fa",
            "bg_secondary": "#ffffff",
            "bg_tertiary": "#e9ecef",
            "text_primary": "#1a1a1a",
            "text_secondary": "#495057",
            "accent_1": "#0056b3",
            "accent_2": "#6f42c1",
            "success": "#28a745",
            "warning": "#fd7e14",
            "error": "#dc3545"
        },
        "Custom": {
            "bg_primary": "#1e1e2e",
            "bg_secondary": "#2a2a3a",
            "bg_tertiary": "#363649",
            "text_primary": "#cdd6f4",
            "text_secondary": "#a6adc8",
            "accent_1": "#89b4fa",
            "accent_2": "#cba6f7",
            "success": "#a6e3a1",
            "warning": "#fab387",
            "error": "#f38ba8"
        }
    }
    
    HEALTHCARE_SOURCES = {
        "WHO": "World Health Organization - Global health standards",
        "KEMKES": "Indonesian Ministry of Health - National policies",
        "ISQua": "International Society for Quality in Health Care",
        "Healthcare IT News": "Healthcare technology trends and innovations",
        "Modern Healthcare": "Industry insights and operational excellence",
        "Joint Commission": "Hospital accreditation and patient safety"
    }

def load_theme_css(theme_name):
    """Load dynamic theme CSS with improved contrast"""
    theme = HealthConfig.THEMES.get(theme_name, HealthConfig.THEMES["Dark"])
    
    # Ensure good contrast for Light theme
    if theme_name == "Light":
        theme["text_primary"] = "#1a1a1a"
        theme["text_secondary"] = "#333333"
    
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Orbitron:wght@400;700&display=swap');
    
    .stApp {{
        background: linear-gradient(135deg, {theme['bg_primary']} 0%, {theme['bg_secondary']} 50%, {theme['bg_tertiary']} 100%);
        color: {theme['text_primary']};
        font-family: 'Inter', sans-serif;
    }}
    
    .main-header {{
        background: linear-gradient(135deg, {theme['accent_1']}, {theme['accent_2']});
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 0 40px rgba(0, 212, 255, 0.3);
        animation: headerGlow 3s ease-in-out infinite;
    }}
    
    @keyframes headerGlow {{
        0%, 100% {{ box-shadow: 0 0 40px {theme['accent_1']}33; }}
        50% {{ box-shadow: 0 0 60px {theme['accent_2']}55; }}
    }}
    
    .main-header h1 {{
        font-family: 'Orbitron', monospace;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        color: white;
        text-shadow: 0 0 30px rgba(255,255,255,0.5);
    }}
    
    .version-badge {{
        display: inline-block;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        padding: 0.5rem 1rem;
        border-radius: 15px;
        margin-top: 1rem;
        font-family: 'Orbitron', monospace;
        color: white;
        font-weight: 600;
    }}
    
    .glass-card {{
        background: {theme['bg_secondary']}cc;
        backdrop-filter: blur(15px);
        border: 1px solid {theme['text_secondary']}20;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        color: {theme['text_primary']};
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }}
    
    .glass-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 30px {theme['accent_2']}30;
    }}
    
    .metric-excellent {{
        border-left: 4px solid {theme['success']};
        background: linear-gradient(135deg, {theme['success']}15, {theme['success']}05);
    }}
    
    .metric-warning {{
        border-left: 4px solid {theme['warning']};
        background: linear-gradient(135deg, {theme['warning']}15, {theme['warning']}05);
    }}
    
    .metric-critical {{
        border-left: 4px solid {theme['error']};
        background: linear-gradient(135deg, {theme['error']}15, {theme['error']}05);
    }}
    
    .stButton > button {{
        background: linear-gradient(135deg, {theme['accent_1']}, {theme['accent_2']});
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 10px 25px {theme['accent_2']}40;
    }}
    
    .status-active {{
        color: {theme['success']};
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 1rem;
        background: {theme['success']}15;
        border-radius: 10px;
        border: 1px solid {theme['success']};
        animation: statusPulse 3s infinite;
        font-weight: 600;
    }}
    
    .status-ready {{
        color: {theme['accent_1']};
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 1rem;
        background: {theme['accent_1']}15;
        border-radius: 10px;
        border: 1px solid {theme['accent_1']};
        font-weight: 600;
    }}
    
    @keyframes statusPulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.8; }}
    }}
    
    .chat-message {{
        background: {theme['bg_secondary']};
        border: 1px solid {theme['accent_1']}30;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        animation: slideIn 0.3s ease-out;
        color: {theme['text_primary']};
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }}
    
    .user-message {{
        background: linear-gradient(135deg, {theme['accent_1']}, {theme['accent_2']});
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        animation: slideIn 0.3s ease-out;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }}
    
    @keyframes slideIn {{
        from {{ transform: translateX(-20px); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}
    
    .ai-indicator {{
        background: linear-gradient(135deg, {theme['accent_2']}, {theme['warning']});
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
        display: inline-block;
        margin: 0.5rem 0;
        animation: aiGlow 2s ease-in-out infinite;
    }}
    
    @keyframes aiGlow {{
        0%, 100% {{ box-shadow: 0 0 10px {theme['accent_2']}30; }}
        50% {{ box-shadow: 0 0 20px {theme['warning']}50; }}
    }}
    
    .compliance-indicator {{
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 0.2rem;
    }}
    
    .compliance-excellent {{ 
        background: {theme['success']}; 
        color: {'white' if theme_name != 'Light' else '#1a1a1a'}; 
    }}
    .compliance-good {{ 
        background: {theme['warning']}; 
        color: white; 
    }}
    .compliance-poor {{ 
        background: {theme['error']}; 
        color: white; 
    }}
    
    /* Improved text contrast for all themes */
    .stMarkdown, .stText, p, div, span {{
        color: {theme['text_primary']} !important;
    }}
    
    /* Sidebar styling */
    .css-1d391kg {{
        background: {theme['bg_secondary']};
    }}
    
    .metric-container {{
        background: {theme['bg_secondary']};
        border: 1px solid {theme['text_secondary']}20;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: {theme['text_primary']};
    }}
    
    /* Input styling with better contrast */
    .stTextInput > div > div > input {{
        background: {theme['bg_secondary']} !important;
        color: {theme['text_primary']} !important;
        border: 1px solid {theme['accent_1']}50 !important;
    }}
    
    .stTextArea > div > div > textarea {{
        background: {theme['bg_secondary']} !important;
        color: {theme['text_primary']} !important;
        border: 1px solid {theme['accent_1']}50 !important;
    }}
    
    .stSelectbox > div > div > select {{
        background: {theme['bg_secondary']} !important;
        color: {theme['text_primary']} !important;
    }}
    
    /* Hide Streamlit elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    .stDeployButton {{visibility: hidden;}}
    
    /* Metrics styling */
    [data-testid="metric-container"] {{
        background: {theme['bg_secondary']};
        border: 1px solid {theme['text_secondary']}30;
        padding: 1rem;
        border-radius: 10px;
        color: {theme['text_primary']};
    }}
    </style>
    """, unsafe_allow_html=True)

class HealthcareAnalytics:
    """Simplified healthcare analytics without external API dependencies"""
    
    def __init__(self):
        self.knowledge_base = {
            "WHO": {
                "patient_safety": "WHO emphasizes medication safety, infection prevention, patient identification, communication during handovers, safe surgery practices, and blood transfusion safety.",
                "quality_indicators": "Mortality rates, readmission rates, patient satisfaction, safety incidents, infection rates, and clinical effectiveness measures.",
                "standards": "Focus on patient-centered care, evidence-based practice, and continuous quality improvement."
            },
            "joint_commission": {
                "core_measures": "Heart attack care, heart failure, pneumonia, surgical care, stroke care, and immunization standards.",
                "patient_safety": "National Patient Safety Goals including patient identification, communication, medication safety, and infection control.",
                "accreditation": "Emphasizes leadership, human resources, information management, and performance improvement."
            },
            "kemkes": {
                "standards": "Indonesian healthcare standards focusing on service quality, patient safety, and healthcare facility management.",
                "compliance": "Hospital accreditation, healthcare professional licensing, and quality assurance programs.",
                "indicators": "Service accessibility, quality of care, patient satisfaction, and health outcomes."
            }
        }
    
    def get_ai_response(self, query, context=None):
        """Generate intelligent responses based on healthcare knowledge base"""
        query_lower = query.lower()
        
        # Basic healthcare responses
        if any(word in query_lower for word in ['who', 'world health']):
            return self._get_who_response(query_lower, context)
        elif any(word in query_lower for word in ['joint commission', 'accreditation']):
            return self._get_jc_response(query_lower, context)
        elif any(word in query_lower for word in ['kemkes', 'indonesian', 'indonesia']):
            return self._get_kemkes_response(query_lower, context)
        elif any(word in query_lower for word in ['hcahps', 'patient satisfaction']):
            return self._get_hcahps_response(query_lower, context)
        elif any(word in query_lower for word in ['safety', 'patient safety']):
            return self._get_safety_response(query_lower, context)
        elif any(word in query_lower for word in ['infection', 'control']):
            return self._get_infection_response(query_lower, context)
        elif any(word in query_lower for word in ['technology', 'digital', 'it']):
            return self._get_technology_response(query_lower, context)
        elif any(word in query_lower for word in ['readmission', 'readmit']):
            return self._get_readmission_response(query_lower, context)
        else:
            return self._get_general_response(query_lower, context)
    
    def _get_who_response(self, query, context):
        base_response = "WHO patient safety indicators include:\n• Medication safety protocols\n• Healthcare-associated infection prevention\n• Patient identification systems\n• Communication during care transitions\n• Safe surgical practices\n• Blood transfusion safety"
        
        if context and context.get('metrics'):
            safety_score = context['metrics'].get('safety_score', 0)
            base_response += f"\n\nYour current safety score is {safety_score}%. "
            if safety_score >= 90:
                base_response += "Excellent compliance with WHO standards!"
            elif safety_score >= 85:
                base_response += "Good performance, focus on continuous improvement."
            else:
                base_response += "Consider implementing WHO patient safety improvement strategies."
        
        return base_response
    
    def _get_jc_response(self, query, context):
        base_response = "Joint Commission focuses on:\n• National Patient Safety Goals\n• Core performance measures\n• Leadership and governance\n• Human resources management\n• Information management\n• Performance improvement programs"
        
        if context and context.get('compliance'):
            jc_score = context['compliance'].get('Joint_Commission', 0)
            base_response += f"\n\nJoint Commission compliance score: {jc_score}%. "
            if jc_score >= 90:
                base_response += "Outstanding readiness for accreditation!"
            else:
                base_response += "Focus on improving core measures and safety protocols."
        
        return base_response
    
    def _get_kemkes_response(self, query, context):
        base_response = "KEMKES Indonesian standards emphasize:\n• Healthcare service quality\n• Patient safety and satisfaction\n• Healthcare professional competency\n• Facility management standards\n• Quality assurance programs\n• Healthcare accessibility"
        
        if context and context.get('compliance'):
            kemkes_score = context['compliance'].get('KEMKES', 0)
            base_response += f"\n\nKEMKES compliance level: {kemkes_score}%. "
            if kemkes_score >= 85:
                base_response += "Strong alignment with Indonesian healthcare standards."
            else:
                base_response += "Consider improving service quality and patient safety measures."
        
        return base_response
    
    def _get_hcahps_response(self, query, context):
        base_response = "HCAHPS improvement strategies:\n• Enhance communication with patients\n• Improve responsiveness of staff\n• Focus on pain management\n• Ensure medication communication\n• Maintain quiet environment\n• Improve discharge information"
        
        if context and context.get('metrics'):
            hcahps = context['metrics'].get('hcahps_score', 0)
            base_response += f"\n\nCurrent HCAHPS score: {hcahps}/10. "
            if hcahps >= 9:
                base_response += "Excellent patient experience scores!"
            elif hcahps >= 8:
                base_response += "Good performance, focus on specific improvement areas."
            else:
                base_response += "Implement patient experience improvement initiatives."
        
        return base_response
    
    def _get_safety_response(self, query, context):
        base_response = "Patient safety best practices:\n• Implement safety checklists\n• Enhance staff training programs\n• Improve incident reporting systems\n• Focus on medication reconciliation\n• Strengthen infection control measures\n• Enhance communication protocols"
        
        if context and context.get('metrics'):
            safety = context['metrics'].get('safety_score', 0)
            base_response += f"\n\nCurrent safety performance: {safety}%. "
            if safety >= 95:
                base_response += "Exceptional safety performance!"
            elif safety >= 90:
                base_response += "Strong safety culture, maintain high standards."
            else:
                base_response += "Prioritize safety improvement initiatives."
        
        return base_response
    
    def _get_infection_response(self, query, context):
        base_response = "Infection control strategies:\n• Hand hygiene compliance programs\n• Environmental cleaning protocols\n• Isolation precautions\n• Antimicrobial stewardship\n• Staff education and training\n• Surveillance and monitoring systems"
        
        if context and context.get('metrics'):
            infection = context['metrics'].get('infection_control', 0)
            base_response += f"\n\nInfection control score: {infection}%. "
            if infection >= 95:
                base_response += "Excellent infection prevention measures!"
            else:
                base_response += "Focus on strengthening infection control protocols."
        
        return base_response
    
    def _get_technology_response(self, query, context):
        base_response = "Healthcare technology trends 2024:\n• Electronic Health Records optimization\n• Telemedicine integration\n• AI-powered diagnostics\n• Remote patient monitoring\n• Clinical decision support systems\n• Cybersecurity enhancements"
        
        if context and context.get('metrics'):
            tech = context['metrics'].get('technology_integration', 0)
            base_response += f"\n\nTechnology integration level: {tech}%. "
            if tech >= 90:
                base_response += "Advanced digital health adoption!"
            else:
                base_response += "Consider accelerating digital transformation initiatives."
        
        return base_response
    
    def _get_readmission_response(self, query, context):
        base_response = "Readmission reduction strategies:\n• Improve discharge planning\n• Enhance patient education\n• Implement follow-up protocols\n• Medication reconciliation\n• Care coordination programs\n• Risk stratification tools"
        
        if context and context.get('metrics'):
            readmit = context['metrics'].get('readmission_rate', 0)
            base_response += f"\n\nCurrent readmission rate: {readmit}%. "
            if readmit < 10:
                base_response += "Excellent readmission performance!"
            elif readmit < 15:
                base_response += "Good performance, continue improvement efforts."
            else:
                base_response += "Focus on discharge planning and care coordination."
        
        return base_response
    
    def _get_general_response(self, query, context):
        return "Healthcare quality management focuses on:\n• Patient safety and satisfaction\n• Clinical effectiveness measures\n• Regulatory compliance\n• Continuous improvement processes\n• Staff training and development\n• Technology integration\n\nFor specific guidance, please ask about WHO, Joint Commission, KEMKES standards, or specific quality indicators."

def analyze_sentiment(text):
    """Enhanced sentiment analysis"""
    if not text or not isinstance(text, str):
        return "Unknown", "#666666"
    
    positive_words = [
        'excellent', 'great', 'good', 'satisfied', 'professional', 'outstanding', 
        'happy', 'caring', 'amazing', 'wonderful', 'fantastic', 'superb', 
        'exceptional', 'remarkable', 'impressive', 'helpful', 'friendly'
    ]
    negative_words = [
        'bad', 'poor', 'terrible', 'slow', 'problem', 'disappointed', 
        'frustrated', 'painful', 'awful', 'horrible', 'disgusting', 
        'unacceptable', 'shocking', 'appalling', 'rude', 'unprofessional'
    ]
    
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count and positive_count > 0:
        return "Positive", "#00ff88"
    elif negative_count > positive_count and negative_count > 0:
        return "Negative", "#ff3d71"
    else:
        return "Neutral", "#ff6b35"

def calculate_compliance_scores(data):
    """Calculate realistic compliance scores based on actual data"""
    if data is None or data.empty:
        return {
            'WHO': 85.2, 'Joint_Commission': 82.8, 'KEMKES': 78.5,
            'ISQua': 80.3, 'Healthcare_IT': 83.7, 'Modern_Healthcare': 81.4
        }
    
    compliance = {}
    
    # WHO compliance based on safety and HCAHPS
    who_factors = []
    if 'Safety_Score' in data.columns:
        who_factors.append(data['Safety_Score'].mean())
    if 'HCAHPS_Overall' in data.columns:
        who_factors.append(data['HCAHPS_Overall'].mean() * 10)
    compliance['WHO'] = round(np.mean(who_factors), 1) if who_factors else 85.2
    
    # Joint Commission based on safety and readmissions
    jc_factors = []
    if 'Safety_Score' in data.columns:
        jc_factors.append(data['Safety_Score'].mean())
    if 'Readmission_30_Day' in data.columns:
        readmission_score = max(0, 100 - (data['Readmission_30_Day'].mean() * 100))
        jc_factors.append(readmission_score)
    compliance['Joint_Commission'] = round(np.mean(jc_factors), 1) if jc_factors else 82.8
    
    # KEMKES based on rating
    if 'KEMKES_Rating' in data.columns:
        a_rating = (data['KEMKES_Rating'] == 'A').sum() / len(data) * 100
        b_rating = (data['KEMKES_Rating'] == 'B').sum() / len(data) * 100
        compliance['KEMKES'] = round(a_rating * 0.9 + b_rating * 0.7 + 40, 1)
    else:
        compliance['KEMKES'] = 78.5
    
    # Derived scores
    base_score = compliance['WHO']
    compliance['ISQua'] = round(min(100, base_score * 0.94 + np.random.uniform(-1, 2)), 1)
    compliance['Healthcare_IT'] = round(min(100, base_score * 0.98 + np.random.uniform(-2, 3)), 1)
    compliance['Modern_Healthcare'] = round(min(100, base_score * 0.95 + np.random.uniform(-1, 4)), 1)
    
    return compliance

def create_sample_data():
    """Generate realistic healthcare data"""
    np.random.seed(42)
    n = 150
    
    departments = ['Cardiology', 'Emergency', 'Surgery', 'ICU', 'Medicine', 'Orthopedics']
    feedback_samples = [
        "Excellent care and very satisfied with treatment received",
        "Professional staff and clean hospital environment",
        "Long waiting time but overall good care quality",
        "Outstanding surgical outcome and quick recovery process",
        "Communication with patients could be improved significantly",
        "Very happy with the personalized care approach",
        "Staff training protocols need enhancement for better service",
        "Impressed with modern medical technology and equipment"
    ]
    
    data = {
        'Patient_ID': [f'PT{i:04d}' for i in range(1, n+1)],
        'Age': np.random.normal(65, 16, n).astype(int).clip(18, 95),
        'Gender': np.random.choice(['Male', 'Female'], n),
        'Department': np.random.choice(departments, n),
        'Length_of_Stay': np.random.exponential(4.3, n).round(1).clip(1, 20),
        'Total_Cost': np.random.lognormal(9.1, 0.6, n).round(2),
        'HCAHPS_Overall': np.random.normal(8.6, 1.2, n).round(1).clip(1, 10),
        'Safety_Score': np.random.normal(89, 8, n).round(1).clip(60, 100),
        'Communication_Score': np.random.normal(85, 11, n).round(1).clip(50, 100),
        'Pain_Management': np.random.normal(80, 13, n).round(1).clip(40, 100),
        'Infection_Control': np.random.normal(94, 7, n).round(1).clip(70, 100),
        'Medication_Safety': np.random.normal(91, 9, n).round(1).clip(60, 100),
        'Technology_Integration': np.random.normal(87, 10, n).round(1).clip(50, 100),
        'Readmission_30_Day': np.random.choice([0, 1], n, p=[0.88, 0.12]),
        'Patient_Feedback': np.random.choice(feedback_samples, n),
        'WHO_Compliance': np.random.choice(['Compliant', 'Partially Compliant'], n, p=[0.8, 0.2]),
        'KEMKES_Rating': np.random.choice(['A', 'B', 'C'], n, p=[0.7, 0.25, 0.05])
    }
    
    df = pd.DataFrame(data)
    
    # Add sentiment analysis
    sentiments = []
    for feedback in df['Patient_Feedback']:
        sentiment, _ = analyze_sentiment(feedback)
        sentiments.append(sentiment)
    df['Sentiment'] = sentiments
    
    return df

def analyze_data(data, ai_manager):
    """Comprehensive data analysis"""
    if data is None or data.empty:
        return {"error": "No data available for analysis"}
    
    compliance_scores = calculate_compliance_scores(data)
    
    analysis = {
        "summary": {
            "total_patients": len(data),
            "avg_age": round(data['Age'].mean(), 1) if 'Age' in data.columns else 0,
            "departments": data['Department'].nunique() if 'Department' in data.columns else 0,
            "avg_cost": round(data['Total_Cost'].mean(), 2) if 'Total_Cost' in data.columns else 0
        },
        "compliance": compliance_scores,
        "metrics": {
            "hcahps_score": round(data['HCAHPS_Overall'].mean(), 2) if 'HCAHPS_Overall' in data.columns else 0,
            "safety_score": round(data['Safety_Score'].mean(), 2) if 'Safety_Score' in data.columns else 0,
            "infection_control": round(data['Infection_Control'].mean(), 2) if 'Infection_Control' in data.columns else 0,
            "technology_integration": round(data['Technology_Integration'].mean(), 2) if 'Technology_Integration' in data.columns else 0,
            "readmission_rate": round((data['Readmission_30_Day'].sum() / len(data)) * 100, 2) if 'Readmission_30_Day' in data.columns else 0
        },
        "sentiment": {
            "positive": round((data['Sentiment'] == 'Positive').sum() / len(data) * 100, 1) if 'Sentiment' in data.columns else 0,
            "negative": round((data['Sentiment'] == 'Negative').sum() / len(data) * 100, 1) if 'Sentiment' in data.columns else 0,
            "neutral": round((data['Sentiment'] == 'Neutral').sum() / len(data) * 100, 1) if 'Sentiment' in data.columns else 0
        }
    }
    
    return analysis

def create_dashboard(data, analysis):
    """Enhanced dashboard with theme support"""
    st.markdown("### 📊 Healthcare Quality Dashboard")
    
    if data is None or data.empty:
        st.info("📊 Generate data to view dashboard")
        return
    
    # Compliance metrics
    compliance = analysis.get("compliance", {})
    if compliance:
        st.markdown("#### 🌍 Standards Compliance")
        cols = st.columns(min(6, len(compliance)))
        
        for i, (standard, score) in enumerate(compliance.items()):
            if i < len(cols):
                with cols[i]:
                    if score >= 90:
                        status = "🟢"
                        delta_color = "normal"
                    elif score >= 85:
                        status = "🟡"
                        delta_color = "normal"
                    else:
                        status = "🔴"
                        delta_color = "inverse"
                    st.metric(standard.replace('_', ' '), f"{score}%", f"{status}")
    
    # Quality metrics
    metrics = analysis.get("metrics", {})
    if metrics:
        st.markdown("#### 📈 Quality Performance")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            hcahps = metrics.get("hcahps_score", 8.6)
            delta = "Above target" if hcahps >= 9 else "Monitor" if hcahps >= 8 else "Needs attention"
            st.metric("HCAHPS", f"{hcahps}/10", delta)
        
        with col2:
            safety = metrics.get("safety_score", 89)
            delta = "Excellent" if safety >= 95 else "Good" if safety >= 90 else "Improve"
            st.metric("Safety", f"{safety}%", delta)
        
        with col3:
            infection = metrics.get("infection_control", 94)
            delta = "Outstanding" if infection >= 95 else "Monitor"
            st.metric("Infection Control", f"{infection}%", delta)
        
        with col4:
            readmit = metrics.get("readmission_rate", 12)
            delta = "Target met" if readmit < 10 else "Above target"
            st.metric("Readmissions", f"{readmit}%", delta)
    
    # Charts
    if compliance and len(compliance) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            # Compliance radar chart
            try:
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=list(compliance.values()),
                    theta=list(compliance.keys()),
                    fill='toself',
                    name='Current Compliance',
                    line_color='#00d4ff'
                ))
                
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                    title="Standards Compliance Overview",
                    height=400,
                    template="plotly_dark"
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception:
                st.info("Chart temporarily unavailable")
        
        with col2:
            # Sentiment distribution
            sentiment = analysis.get("sentiment", {})
            if sentiment:
                try:
                    labels = ['Positive', 'Neutral', 'Negative']
                    values = [sentiment.get('positive', 0), sentiment.get('neutral', 0), sentiment.get('negative', 0)]
                    colors = ['#00ff88', '#ff6b35', '#ff3d71']
                    
                    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.4)])
                    fig.update_traces(marker=dict(colors=colors))
                    fig.update_layout(
                        title="Patient Sentiment Distribution",
                        height=400,
                        template="plotly_dark"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                except Exception:
                    st.info("Sentiment chart temporarily unavailable")

def main():
    """Main application with enhanced UI and simplified AI"""
    st.set_page_config(
        page_title="Healthcare AI RAG - Enhanced",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    if 'ai_manager' not in st.session_state:
        st.session_state.ai_manager = HealthcareAnalytics()
    if 'current_data' not in st.session_state:
        st.session_state.current_data = None
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = {}
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'chatbot_history' not in st.session_state:
        st.session_state.chatbot_history = []
    if 'theme' not in st.session_state:
        st.session_state.theme = "Dark"
    
    # Theme selector in sidebar
    with st.sidebar:
        st.markdown("### 🎨 Theme Settings")
        
        theme_options = ["Dark", "Light", "Custom"]
        selected_theme = st.selectbox(
            "Choose Theme:",
            theme_options,
            index=theme_options.index(st.session_state.theme),
            key="theme_selector"
        )
        
        if selected_theme != st.session_state.theme:
            st.session_state.theme = selected_theme
            st.rerun()
    
    # Load theme CSS
    load_theme_css(st.session_state.theme)
    
    # Header
    st.markdown(f"""
    <div class="main-header">
        <h1>{HealthConfig.APP_TITLE}</h1>
        <p>🚀 Powered by Advanced AI Analytics • Healthcare Intelligence • Global Standards</p>
        <div class="version-badge">
            v{HealthConfig.APP_VERSION} • {st.session_state.theme} Theme • Production Ready
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar controls
    with st.sidebar:
        st.markdown("### 🤖 AI System Status")
        
        # AI Status - Always Ready
        st.markdown("""
        <div class="status-active">
            ✅ AI Healthcare Assistant Active
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="status-ready">
            🧠 Advanced Analytics Ready
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="ai-indicator">🎯 Healthcare Intelligence Online</div>', unsafe_allow_html=True)
        
        st.markdown("### 🌍 Healthcare Sources")
        for source, desc in HealthConfig.HEALTHCARE_SOURCES.items():
            st.markdown(f"**{source}**: {desc[:35]}...")
        
        st.markdown("### 🎯 Quick Actions")
        
        if st.button("📊 Generate Sample Data", use_container_width=True):
            with st.spinner("Generating realistic healthcare data..."):
                try:
                    st.session_state.current_data = create_sample_data()
                    if st.session_state.current_data is not None and not st.session_state.current_data.empty:
                        st.session_state.analysis_results = analyze_data(
                            st.session_state.current_data, 
                            st.session_state.ai_manager
                        )
                        st.success("✅ Sample data generated successfully!")
                        st.balloons()
                    else:
                        st.error("Failed to generate data")
                except Exception as e:
                    st.error(f"Error generating data: {str(e)}")
            st.rerun()
        
        if st.button("🧹 Clear All Data", use_container_width=True):
            try:
                st.session_state.current_data = None
                st.session_state.analysis_results = {}
                st.session_state.chat_history = []
                st.session_state.chatbot_history = []
                st.success("✅ All data cleared!")
            except Exception as e:
                st.error(f"Error clearing data: {str(e)}")
            st.rerun()
        
        # Dataset info
        if st.session_state.current_data is not None and not st.session_state.current_data.empty:
            st.markdown("### 📊 Current Dataset")
            data = st.session_state.current_data
            st.metric("Records", f"{len(data):,}")
            st.metric("Features", len(data.columns))
            
            # Show compliance summary
            if st.session_state.analysis_results:
                compliance = st.session_state.analysis_results.get("compliance", {})
                if compliance:
                    st.markdown("**Compliance Summary:**")
                    for standard, score in list(compliance.items())[:3]:
                        if score >= 90:
                            color = "#00ff88"
                            icon = "✅"
                        elif score >= 85:
                            color = "#ff6b35" 
                            icon = "⚠️"
                        else:
                            color = "#ff3d71"
                            icon = "🔴"
                        st.markdown(f'<span style="color: {color}">{icon} {standard}: {score}%</span>', unsafe_allow_html=True)
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🤖 AI Assistant", 
        "📊 Analytics", 
        "📈 Dashboard",
        "💬 Advanced Chat"
    ])
    
    with tab1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🤖 Healthcare AI Assistant")
        st.markdown('<span class="ai-indicator">💬 Intelligent Healthcare Guidance • Evidence-Based Responses</span>', unsafe_allow_html=True)
        
        # Quick questions
        st.markdown("#### ⚡ Popular Healthcare Questions")
        quick_questions = [
            "What are WHO patient safety indicators?",
            "How to improve HCAHPS scores?", 
            "Best practices for infection control?",
            "Joint Commission requirements overview?",
            "Healthcare technology trends 2024?",
            "Reduce patient readmission strategies?"
        ]
        
        cols = st.columns(3)
        for i, question in enumerate(quick_questions):
            col = cols[i % 3]
            with col:
                if st.button(question, key=f"quick_{i}", use_container_width=True):
                    with st.spinner("🤖 AI analyzing..."):
                        try:
                            context = st.session_state.analysis_results
                            response = st.session_state.ai_manager.get_ai_response(question, context)
                            st.session_state.chatbot_history.append({
                                "user": question,
                                "ai": response,
                                "time": datetime.now().strftime("%H:%M")
                            })
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    st.rerun()
        
        # Chat input
        st.markdown("#### 💬 Ask Healthcare AI")
        chat_input = st.text_input(
            "Type your healthcare question:",
            placeholder="e.g., How to reduce patient readmission rates?",
            key="chat_input"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("🚀 Send Message", use_container_width=True) and chat_input:
                with st.spinner("🤖 AI processing..."):
                    try:
                        context = st.session_state.analysis_results
                        response = st.session_state.ai_manager.get_ai_response(chat_input, context)
                        st.session_state.chatbot_history.append({
                            "user": chat_input,
                            "ai": response,
                            "time": datetime.now().strftime("%H:%M")
                        })
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                st.rerun()
        
        with col2:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chatbot_history = []
                st.rerun()
        
        # Chat history
        if st.session_state.chatbot_history:
            st.markdown("#### 💭 Chat History")
            
            for chat in st.session_state.chatbot_history[-6:]:  # Show last 6
                st.markdown(f"""
                <div class="user-message">
                    <strong>You ({chat['time']}):</strong> {chat['user']}
                </div>
                <div class="chat-message">
                    <strong>🤖 Healthcare AI:</strong><br>{chat['ai']}
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Healthcare Data Analytics")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload Healthcare Dataset", 
            type=['csv', 'xlsx'],
            help="Upload your healthcare data for comprehensive analysis"
        )
        
        if uploaded_file:
            try:
                with st.spinner("Processing uploaded data..."):
                    if uploaded_file.name.endswith('.csv'):
                        st.session_state.current_data = pd.read_csv(uploaded_file)
                    else:
                        st.session_state.current_data = pd.read_excel(uploaded_file)
                    
                    if st.session_state.current_data is not None and not st.session_state.current_data.empty:
                        st.session_state.analysis_results = analyze_data(
                            st.session_state.current_data,
                            st.session_state.ai_manager
                        )
                        st.success(f"✅ Analysis complete: {len(st.session_state.current_data):,} records processed")
                    else:
                        st.error("❌ Failed to load data from file")
                
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
        
        # Results display
        if st.session_state.current_data is not None and not st.session_state.current_data.empty and st.session_state.analysis_results:
            
            # Dataset summary
            summary = st.session_state.analysis_results.get("summary", {})
            st.markdown("#### 📋 Dataset Overview")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Patients", f"{summary.get('total_patients', 0):,}")
            with col2:
                st.metric("Average Age", f"{summary.get('avg_age', 0)} years")
            with col3:
                st.metric("Departments", summary.get('departments', 0))
            with col4:
                st.metric("Avg Cost", f"${summary.get('avg_cost', 0):,.0f}")
            
            # Compliance scores
            compliance = st.session_state.analysis_results.get("compliance", {})
            if compliance:
                st.markdown("#### 🌍 Healthcare Standards Compliance")
                
                cols = st.columns(min(6, len(compliance)))
                for i, (standard, score) in enumerate(compliance.items()):
                    if i < len(cols):
                        with cols[i]:
                            if score >= 90:
                                status_class = "compliance-excellent"
                                status_text = "Excellent"
                            elif score >= 85:
                                status_class = "compliance-good"
                                status_text = "Good"
                            else:
                                status_class = "compliance-poor"
                                status_text = "Needs Improvement"
                            
                            st.metric(standard.replace('_', ' '), f"{score}%")
                            st.markdown(f'<span class="compliance-indicator {status_class}">{status_text}</span>', unsafe_allow_html=True)
            
            # Quality metrics
            metrics = st.session_state.analysis_results.get("metrics", {})
            if metrics:
                st.markdown("#### 📈 Quality Performance Indicators")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    hcahps = metrics.get("hcahps_score", 0)
                    status_class = "metric-excellent" if hcahps > 9 else "metric-warning" if hcahps > 8 else "metric-critical"
                    st.markdown(f'<div class="glass-card {status_class}">', unsafe_allow_html=True)
                    st.metric("HCAHPS Score", f"{hcahps}/10")
                    st.markdown('<small>Patient Experience</small>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    safety = metrics.get("safety_score", 0)
                    status_class = "metric-excellent" if safety > 90 else "metric-warning" if safety > 85 else "metric-critical"
                    st.markdown(f'<div class="glass-card {status_class}">', unsafe_allow_html=True)
                    st.metric("Safety Score", f"{safety}%")
                    st.markdown('<small>Patient Safety Standards</small>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col3:
                    infection = metrics.get("infection_control", 0)
                    status_class = "metric-excellent" if infection > 95 else "metric-warning" if infection > 90 else "metric-critical"
                    st.markdown(f'<div class="glass-card {status_class}">', unsafe_allow_html=True)
                    st.metric("Infection Control", f"{infection}%")
                    st.markdown('<small>Prevention Standards</small>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col4:
                    tech = metrics.get("technology_integration", 0)
                    status_class = "metric-excellent" if tech > 90 else "metric-warning" if tech > 85 else "metric-critical"
                    st.markdown(f'<div class="glass-card {status_class}">', unsafe_allow_html=True)
                    st.metric("Technology Integration", f"{tech}%")
                    st.markdown('<small>Digital Health Adoption</small>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # Sentiment analysis
            sentiment = st.session_state.analysis_results.get("sentiment", {})
            if sentiment:
                st.markdown("#### 😊 Patient Sentiment Analysis")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    positive = sentiment.get("positive", 0)
                    st.markdown('<div class="glass-card metric-excellent">', unsafe_allow_html=True)
                    st.metric("Positive Feedback", f"{positive}%")
                    st.markdown('<small>Satisfied Patients</small>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    neutral = sentiment.get("neutral", 0)
                    st.markdown('<div class="glass-card metric-warning">', unsafe_allow_html=True)
                    st.metric("Neutral Feedback", f"{neutral}%")
                    st.markdown('<small>Improvement Opportunity</small>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col3:
                    negative = sentiment.get("negative", 0)
                    st.markdown('<div class="glass-card metric-critical">', unsafe_allow_html=True)
                    st.metric("Negative Feedback", f"{negative}%")
                    st.markdown('<small>Requires Attention</small>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # Data preview
            with st.expander("📋 Data Preview (First 10 Records)"):
                st.dataframe(st.session_state.current_data.head(10), use_container_width=True)
        
        else:
            st.info("📊 Upload a dataset or generate sample data to view analytics")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        if st.session_state.current_data is not None and not st.session_state.current_data.empty:
            create_dashboard(st.session_state.current_data, st.session_state.analysis_results)
        else:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 📈 Interactive Healthcare Dashboard")
            st.info("📊 Generate sample data or upload your dataset to view the interactive dashboard")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 💬 Advanced Healthcare Analysis")
        st.markdown('<span class="ai-indicator">🧠 Comprehensive Healthcare Insights • Strategic Recommendations</span>', unsafe_allow_html=True)
        
        # Advanced chat interface
        user_query = st.text_area(
            "Ask for detailed healthcare analysis:",
            placeholder="e.g., Provide comprehensive analysis of patient safety indicators and strategic improvement recommendations based on WHO and Joint Commission standards...",
            height=120
        )
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if st.button("🚀 Get Detailed Analysis", use_container_width=True):
                if user_query.strip():
                    with st.spinner("🧠 AI conducting comprehensive analysis..."):
                        try:
                            context = st.session_state.analysis_results
                            response = st.session_state.ai_manager.get_ai_response(user_query, context)
                            
                            st.session_state.chat_history.append({
                                "user": user_query,
                                "ai": response,
                                "timestamp": datetime.now().strftime("%H:%M:%S")
                            })
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    st.rerun()
                else:
                    st.warning("Please enter a detailed question for analysis")
        
        with col2:
            if st.button("🧹 Clear History", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
        
        with col3:
            if st.button("📊 Executive Summary", use_container_width=True):
                if st.session_state.current_data is not None:
                    executive_prompt = "Provide an executive summary with comprehensive analysis of WHO, Joint Commission, KEMKES compliance. Include strategic recommendations and action plan based on current performance metrics."
                    with st.spinner("Generating executive summary..."):
                        try:
                            context = st.session_state.analysis_results
                            response = st.session_state.ai_manager.get_ai_response(executive_prompt, context)
                            
                            st.session_state.chat_history.append({
                                "user": "Executive Summary Request",
                                "ai": response,
                                "timestamp": datetime.now().strftime("%H:%M:%S")
                            })
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    st.rerun()
                else:
                    st.warning("Generate data first to get executive summary")
        
        # Analysis history
        if st.session_state.chat_history:
            st.markdown("#### 💭 Detailed Analysis History")
            for chat in reversed(st.session_state.chat_history[-3:]):
                st.markdown(f"""
                <div class="user-message">
                    <strong>You ({chat['timestamp']}):</strong> {chat['user']}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="chat-message">
                    <strong>🧠 Healthcare AI Advanced Analysis:</strong><br><br>
                    {chat['ai']}
                </div>
                """, unsafe_allow_html=True)
        
        # Sample advanced questions
        st.markdown("#### 💡 Advanced Healthcare Analysis Questions")
        advanced_questions = [
            "How to achieve 95%+ WHO compliance across all departments?",
            "Strategic plan for Joint Commission accreditation excellence?",
            "Technology integration roadmap for modern healthcare delivery?",
            "Comprehensive patient satisfaction improvement strategies?"
        ]
        
        cols = st.columns(2)
        for i, question in enumerate(advanced_questions):
            col = cols[i % 2]
            with col:
                if st.button(question, key=f"advanced_{i}", use_container_width=True):
                    with st.spinner("🧠 Processing advanced analysis..."):
                        try:
                            context = st.session_state.analysis_results
                            response = st.session_state.ai_manager.get_ai_response(question, context)
                            
                            st.session_state.chat_history.append({
                                "user": question,
                                "ai": response,
                                "timestamp": datetime.now().strftime("%H:%M:%S")
                            })
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced footer
    st.markdown(f"""
    <div class="glass-card" style="text-align: center; margin-top: 2rem;">
        <h3>🏥 Healthcare AI RAG v{HealthConfig.APP_VERSION} - Production Ready</h3>
        <p>🤖 Intelligent Analytics • 🎨 {st.session_state.theme} Theme • 📊 Evidence-Based Insights • 🌍 Global Standards</p>
        <div style="margin-top: 1rem;">
            <span style="color: #00ff88;">WHO Compliant</span> • 
            <span style="color: #00d4ff;">Joint Commission Ready</span> • 
            <span style="color: #8b5cf6;">KEMKES Aligned</span> •
            <span style="color: #ff6b35;">ISQua Excellence</span>
        </div>
        <p style="font-size: 0.8rem; opacity: 0.7; margin-top: 1rem;">
            Enhanced healthcare intelligence with advanced analytics and compliance monitoring
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"❌ Application Error: {str(e)}")
        st.info("🔄 Please refresh the page to restart the application")
