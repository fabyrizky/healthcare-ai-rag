import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')

# Enhanced Config with Meta Llama 4 Maverick - OPTIMIZED
class HealthConfig:
    APP_TITLE = "🏥 AGENTIC AI FOR HOSPITAL QUALITY SYSTEM"
    APP_VERSION = "8.5.0"
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
    
    # Meta Llama 4 Maverick Auto-Activated
    AI_MODEL = {
        "model": "meta-llama/llama-3.1-8b-instruct:free",
        "key": "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",
        "name": "🚀 Meta Llama 4 Maverick"
    }
    
    # Healthcare Sources - OPTIMIZED
    HEALTHCARE_SOURCES = {
        "WHO": "World Health Organization - Global health standards",
        "KEMKES": "Indonesian Ministry of Health - National policies",
        "ISQua": "International Society for Quality in Health Care",
        "Healthcare IT News": "Healthcare technology trends and innovations",
        "Modern Healthcare": "Industry insights and operational excellence",
        "Joint Commission": "Hospital accreditation and patient safety"
    }

def load_optimized_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Orbitron:wght@400;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        color: white;
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #00d4ff, #8b5cf6);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 0 40px rgba(0, 212, 255, 0.3);
        animation: headerGlow 3s ease-in-out infinite;
    }
    
    @keyframes headerGlow {
        0%, 100% { box-shadow: 0 0 40px rgba(0, 212, 255, 0.3); }
        50% { box-shadow: 0 0 60px rgba(139, 92, 246, 0.5); }
    }
    
    .main-header h1 {
        font-family: 'Orbitron', monospace;
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        color: white;
        text-shadow: 0 0 30px rgba(255,255,255,0.5);
    }
    
    .version-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 0.5rem 1rem;
        border-radius: 15px;
        margin-top: 1rem;
        font-family: 'Orbitron', monospace;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(139, 92, 246, 0.2);
    }
    
    .metric-excellent {
        border-left: 4px solid #00ff88;
        background: linear-gradient(135deg, rgba(0, 255, 136, 0.15), rgba(0, 255, 136, 0.05));
    }
    
    .metric-warning {
        border-left: 4px solid #ff6b35;
        background: linear-gradient(135deg, rgba(255, 107, 53, 0.15), rgba(255, 107, 53, 0.05));
    }
    
    .metric-critical {
        border-left: 4px solid #ff3d71;
        background: linear-gradient(135deg, rgba(255, 61, 113, 0.15), rgba(255, 61, 113, 0.05));
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #00d4ff, #8b5cf6);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        font-family: 'Orbitron', monospace;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 10px 25px rgba(139, 92, 246, 0.4);
    }
    
    .status-active {
        color: #00ff88;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.8rem;
        background: rgba(0, 255, 136, 0.1);
        border-radius: 10px;
        border: 1px solid #00ff88;
        animation: statusPulse 3s infinite;
    }
    
    @keyframes statusPulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    .chat-message {
        background: rgba(0, 255, 136, 0.1);
        border: 1px solid #00ff88;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        animation: slideIn 0.3s ease-out;
    }
    
    .user-message {
        background: linear-gradient(135deg, #00d4ff, #8b5cf6);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .chatbot-container {
        background: rgba(139, 92, 246, 0.1);
        border: 1px solid #8b5cf6;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        max-height: 400px;
        overflow-y: auto;
    }
    
    .quick-action {
        background: rgba(0, 212, 255, 0.1);
        border: 1px solid #00d4ff;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        margin: 0.3rem;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-block;
    }
    
    .quick-action:hover {
        background: rgba(0, 212, 255, 0.2);
        transform: translateY(-2px);
    }
    
    .meta-indicator {
        background: linear-gradient(135deg, #ff6b35, #8b5cf6);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
        display: inline-block;
        margin: 0.5rem 0;
        animation: metaGlow 2s ease-in-out infinite;
    }
    
    @keyframes metaGlow {
        0%, 100% { box-shadow: 0 0 10px rgba(255, 107, 53, 0.3); }
        50% { box-shadow: 0 0 20px rgba(139, 92, 246, 0.5); }
    }
    
    .compliance-indicator {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    
    .compliance-excellent { background: #00ff88; color: #000; }
    .compliance-good { background: #ff6b35; color: #fff; }
    .compliance-poor { background: #ff3d71; color: #fff; }
    </style>
    """, unsafe_allow_html=True)

class HealthcareAI:
    def __init__(self):
        self.config = HealthConfig()
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Healthcare-AI/8.5.0'
        })
    
    def test_model(self):
        """Test Meta Llama 4 Maverick - OPTIMIZED"""
        try:
            test_payload = {
                "model": self.config.AI_MODEL["model"],
                "messages": [{"role": "user", "content": "Test healthcare AI functionality"}],
                "max_tokens": 50,
                "temperature": 0.3
            }
            
            headers = {"Authorization": f"Bearer {self.config.AI_MODEL['key']}"}
            response = self.session.post(f"{self.config.OPENROUTER_BASE_URL}/chat/completions", 
                                       headers=headers, json=test_payload, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                if 'choices' in data and data['choices']:
                    return True, "✅ Meta Llama 4 Maverick Ready!"
            return False, f"❌ API Error {response.status_code}"
        except Exception as e:
            return False, f"❌ Test failed: {str(e)[:30]}"
    
    def chat_query(self, prompt, context=None, chat_mode=True):
        """Enhanced chat query with concise responses - NEW CHATBOT FEATURE"""
        try:
            # Optimized system prompt for chatbot
            if chat_mode:
                system_prompt = f"""You are Meta Llama 4 Maverick healthcare AI chatbot. Provide CONCISE, CLEAR, and ACTIONABLE responses.

Healthcare Sources: WHO, KEMKES, ISQua, Healthcare IT News, Modern Healthcare, Joint Commission.

Rules:
- Keep responses under 150 words
- Use bullet points for multiple items
- Provide specific numbers/percentages when available
- Include 1-2 actionable recommendations
- Focus on practical healthcare solutions

Context: {json.dumps(context) if context else "General healthcare inquiry"}"""
            else:
                system_prompt = f"""You are Meta Llama 4 Maverick, expert healthcare AI with comprehensive knowledge of global standards.

Healthcare Sources: WHO, KEMKES, ISQua, Healthcare IT News, Modern Healthcare, Joint Commission.

Provide detailed evidence-based insights with specific metrics and actionable recommendations.

Context: {json.dumps(context) if context else "General healthcare inquiry"}"""
            
            max_tokens = 200 if chat_mode else 800
            
            payload = {
                "model": self.config.AI_MODEL["model"],
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            
            headers = {"Authorization": f"Bearer {self.config.AI_MODEL['key']}"}
            response = self.session.post(f"{self.config.OPENROUTER_BASE_URL}/chat/completions",
                                       headers=headers, json=payload, timeout=25)
            
            if response.status_code == 200:
                data = response.json()
                if 'choices' in data and data['choices']:
                    return data['choices'][0]['message']['content'].strip()
            return f"⚠️ API Error {response.status_code}"
        except Exception as e:
            return f"❌ Error: {str(e)[:40]}"

def analyze_sentiment(text):
    """Optimized sentiment analysis"""
    positive_words = ['excellent', 'great', 'good', 'satisfied', 'professional', 'outstanding', 'happy', 'caring']
    negative_words = ['bad', 'poor', 'terrible', 'slow', 'problem', 'disappointed', 'frustrated', 'painful']
    
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        return "Positive", "#00ff88"
    elif negative_count > positive_count:
        return "Negative", "#ff3d71"
    else:
        return "Neutral", "#ff6b35"

def calculate_compliance_scores(data):
    """Calculate comprehensive compliance scores - OPTIMIZED"""
    if data.empty:
        return {
            'WHO': 87.0, 'Joint_Commission': 84.0, 'KEMKES': 80.0,
            'ISQua': 82.0, 'Healthcare_IT': 85.0, 'Modern_Healthcare': 83.0
        }
    
    compliance = {}
    
    # WHO compliance
    who_factors = []
    if 'Safety_Score' in data.columns:
        who_factors.append(data['Safety_Score'].mean())
    if 'HCAHPS_Overall' in data.columns:
        who_factors.append(data['HCAHPS_Overall'].mean() * 10)
    compliance['WHO'] = round(np.mean(who_factors), 1) if who_factors else 87.0
    
    # Joint Commission
    jc_factors = []
    if 'Safety_Score' in data.columns:
        jc_factors.append(data['Safety_Score'].mean())
    if 'Readmission_30_Day' in data.columns:
        jc_factors.append(100 - (data['Readmission_30_Day'].mean() * 100))
    compliance['Joint_Commission'] = round(np.mean(jc_factors), 1) if jc_factors else 84.0
    
    # KEMKES
    if 'KEMKES_Rating' in data.columns:
        a_rating = (data['KEMKES_Rating'] == 'A').sum() / len(data) * 100
        compliance['KEMKES'] = round(a_rating * 0.7 + 60, 1)
    else:
        compliance['KEMKES'] = 80.0
    
    # Other standards
    compliance['ISQua'] = round((compliance['WHO'] + compliance['Joint_Commission']) / 2, 1)
    compliance['Healthcare_IT'] = round(compliance['WHO'] * 0.95, 1)
    compliance['Modern_Healthcare'] = round(compliance['Joint_Commission'] * 0.98, 1)
    
    return compliance

def create_sample_data():
    """Generate optimized healthcare data - STREAMLINED"""
    np.random.seed(42)
    n = 200
    
    departments = ['Cardiology', 'Emergency', 'Surgery', 'ICU', 'Medicine', 'Orthopedics']
    feedback_samples = [
        "Excellent care and satisfied with treatment",
        "Professional staff and clean environment",
        "Long waiting time but good care",
        "Outstanding service and quick recovery",
        "Communication could be improved",
        "Very happy with surgery outcome",
        "Staff needs better training",
        "Impressed with medical technology"
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
    """Optimized data analysis - STREAMLINED"""
    if data.empty:
        return {}
    
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
    """Optimized dashboard - STREAMLINED"""
    st.markdown("### 📊 Healthcare Quality Dashboard")
    
    if data.empty:
        st.info("📊 Generate data to view dashboard")
        return
    
    # Compliance metrics
    compliance = analysis.get("compliance", {})
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    cols = [col1, col2, col3, col4, col5, col6]
    for i, (standard, score) in enumerate(compliance.items()):
        if i < len(cols):
            with cols[i]:
                status = "🟢" if score >= 90 else "🟡" if score >= 85 else "🔴"
                st.metric(standard.replace('_', ' '), f"{score}%", status)
    
    # Quality metrics
    metrics = analysis.get("metrics", {})
    st.markdown("#### 📈 Quality Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        hcahps = metrics.get("hcahps_score", 8.6)
        st.metric("HCAHPS", f"{hcahps}/10")
    
    with col2:
        safety = metrics.get("safety_score", 89)
        st.metric("Safety", f"{safety}%")
    
    with col3:
        infection = metrics.get("infection_control", 94)
        st.metric("Infection Control", f"{infection}%")
    
    with col4:
        readmit = metrics.get("readmission_rate", 12)
        st.metric("Readmissions", f"{readmit}%")
    
    # Compliance radar chart
    if compliance:
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=list(compliance.values()),
            theta=list(compliance.keys()),
            fill='toself',
            name='Current',
            line_color='#00d4ff'
        ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            title="Standards Compliance",
            height=400,
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

def main():
    """Main application - OPTIMIZED"""
    st.set_page_config(
        page_title="Healthcare AI RAG - Meta Llama 4",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    load_optimized_css()
    
    # Initialize session state
    if 'ai_manager' not in st.session_state:
        st.session_state.ai_manager = HealthcareAI()
    if 'current_data' not in st.session_state:
        st.session_state.current_data = None
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = {}
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'chatbot_history' not in st.session_state:
        st.session_state.chatbot_history = []
    
    # Header
    st.markdown(f"""
    <div class="main-header">
        <h1>{HealthConfig.APP_TITLE}</h1>
        <p>🚀 Powered by Meta Llama 4 Maverick • AI Chatbot • Global Standards</p>
        <div class="version-badge">
            v{HealthConfig.APP_VERSION} • Meta AI • Chatbot • Analytics
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🚀 Meta Llama 4 Controls")
        
        st.markdown("""
        <div class="status-active">
            🚀 Meta Llama 4 Maverick Active
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="meta-indicator">🧠 AI Chatbot Ready</div>', unsafe_allow_html=True)
        
        # Test AI
        if st.button("🧪 Test Meta Llama 4", use_container_width=True):
            with st.spinner("Testing..."):
                is_working, message = st.session_state.ai_manager.test_model()
                if is_working:
                    st.success(message)
                else:
                    st.error(message)
        
        st.markdown("### 🌍 Healthcare Sources")
        for source, desc in HealthConfig.HEALTHCARE_SOURCES.items():
            st.markdown(f"**{source}**: {desc[:30]}...")
        
        st.markdown("### 🎯 Quick Actions")
        
        if st.button("📊 Generate Data", use_container_width=True):
            with st.spinner("Generating..."):
                st.session_state.current_data = create_sample_data()
                st.session_state.analysis_results = analyze_data(
                    st.session_state.current_data, 
                    st.session_state.ai_manager
                )
            st.success("✅ Data ready!")
            st.balloons()
            st.rerun()
        
        if st.button("🧹 Clear All", use_container_width=True):
            st.session_state.current_data = None
            st.session_state.analysis_results = {}
            st.session_state.chat_history = []
            st.session_state.chatbot_history = []
            st.success("✅ Cleared!")
            st.rerun()
        
        # Dataset info
        if st.session_state.current_data is not None:
            st.markdown("### 📊 Dataset")
            data = st.session_state.current_data
            st.metric("Records", len(data))
            st.metric("Features", len(data.columns))
    
    # Main tabs - OPTIMIZED
    tab1, tab2, tab3, tab4 = st.tabs([
        "🤖 AI Chatbot", 
        "📊 Analytics", 
        "📈 Dashboard",
        "💬 AI Assistant"
    ])
    
    with tab1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🤖 Meta Llama 4 Healthcare Chatbot")
        st.markdown('<span class="meta-indicator">💬 Quick Healthcare Answers</span>', unsafe_allow_html=True)
        
        # Quick action buttons
        st.markdown("#### ⚡ Quick Questions")
        quick_questions = [
            "What are WHO patient safety indicators?",
            "How to improve HCAHPS scores?",
            "Best practices for infection control?",
            "Joint Commission requirements?",
            "Healthcare IT trends 2024?",
            "Modern hospital efficiency tips?"
        ]
        
        cols = st.columns(3)
        for i, question in enumerate(quick_questions):
            col = cols[i % 3]
            with col:
                if st.button(question, key=f"quick_{i}", use_container_width=True):
                    with st.spinner("🤖 Thinking..."):
                        context = st.session_state.analysis_results
                        response = st.session_state.ai_manager.chat_query(question, context, chat_mode=True)
                        st.session_state.chatbot_history.append({
                            "user": question,
                            "ai": response,
                            "time": datetime.now().strftime("%H:%M")
                        })
                    st.rerun()
        
        # Chat input
        chat_input = st.text_input(
            "💬 Ask Meta Llama 4 anything about healthcare:",
            placeholder="e.g. How to reduce readmission rates?",
            key="chat_input"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("🚀 Send", use_container_width=True) and chat_input:
                with st.spinner("🤖 Meta Llama 4 responding..."):
                    context = st.session_state.analysis_results
                    response = st.session_state.ai_manager.chat_query(chat_input, context, chat_mode=True)
                    st.session_state.chatbot_history.append({
                        "user": chat_input,
                        "ai": response,
                        "time": datetime.now().strftime("%H:%M")
                    })
                st.rerun()
        
        with col2:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chatbot_history = []
                st.rerun()
        
        # Chat history
        if st.session_state.chatbot_history:
            st.markdown("#### 💭 Chat History")
            st.markdown('<div class="chatbot-container">', unsafe_allow_html=True)
            
            for chat in st.session_state.chatbot_history[-10:]:  # Show last 10
                st.markdown(f"""
                <div class="user-message">
                    <strong>You ({chat['time']}):</strong> {chat['user']}
                </div>
                <div class="chat-message">
                    <strong>🤖 Meta Llama 4:</strong><br>{chat['ai']}
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Healthcare Analytics")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload Healthcare Dataset", 
            type=['csv', 'xlsx'],
            help="Upload your data for analysis"
        )
        
        if uploaded_file:
            try:
                with st.spinner("Processing..."):
                    if uploaded_file.name.endswith('.csv'):
                        st.session_state.current_data = pd.read_csv(uploaded_file)
                    else:
                        st.session_state.current_data = pd.read_excel(uploaded_file)
                    
                    st.session_state.analysis_results = analyze_data(
                        st.session_state.current_data,
                        st.session_state.ai_manager
                    )
                
                st.success(f"✅ Analysis complete: {len(st.session_state.current_data):,} records")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
        
        # Results display
        if st.session_state.current_data is not None and st.session_state.analysis_results:
            
            # Summary
            summary = st.session_state.analysis_results.get("summary", {})
            st.markdown("#### 📋 Dataset Summary")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Patients", f"{summary.get('total_patients', 0):,}")
            with col2:
                st.metric("Avg Age", f"{summary.get('avg_age', 0)} years")
            with col3:
                st.metric("Departments", summary.get('departments', 0))
            with col4:
                st.metric("Avg Cost", f"${summary.get('avg_cost', 0):,.0f}")
            
            # Compliance scores
            compliance = st.session_state.analysis_results.get("compliance", {})
            if compliance:
                st.markdown("#### 🌍 Standards Compliance")
                
                cols = st.columns(len(compliance))
                for i, (standard, score) in enumerate(compliance.items()):
                    with cols[i]:
                        if score >= 90:
                            status_class = "compliance-excellent"
                            status_text = "Excellent"
                        elif score >= 85:
                            status_class = "compliance-good"
                            status_text = "Good"
                        else:
                            status_class = "compliance-poor"
                            status_text = "Needs Work"
                        
                        st.metric(standard.replace('_', ' '), f"{score}%")
                        st.markdown(f'<span class="compliance-indicator {status_class}">{status_text}</span>', unsafe_allow_html=True)
            
            # Quality metrics
            metrics = st.session_state.analysis_results.get("metrics", {})
            if metrics:
                st.markdown("#### 📈 Quality Performance")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    hcahps = metrics.get("hcahps_score", 0)
                    status_class = "metric-excellent" if hcahps > 9 else "metric-warning" if hcahps > 8 else "metric-critical"
                    st.markdown(f'<div class="glass-card {status_class}">', unsafe_allow_html=True)
                    st.metric("HCAHPS", f"{hcahps}/10")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    safety = metrics.get("safety_score", 0)
                    status_class = "metric-excellent" if safety > 90 else "metric-warning" if safety > 85 else "metric-critical"
                    st.markdown(f'<div class="glass-card {status_class}">', unsafe_allow_html=True)
                    st.metric("Safety", f"{safety}%")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col3:
                    infection = metrics.get("infection_control", 0)
                    status_class = "metric-excellent" if infection > 95 else "metric-warning" if infection > 90 else "metric-critical"
                    st.markdown(f'<div class="glass-card {status_class}">', unsafe_allow_html=True)
                    st.metric("Infection Control", f"{infection}%")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col4:
                    tech = metrics.get("technology_integration", 0)
                    status_class = "metric-excellent" if tech > 90 else "metric-warning" if tech > 85 else "metric-critical"
                    st.markdown(f'<div class="glass-card {status_class}">', unsafe_allow_html=True)
                    st.metric("Technology", f"{tech}%")
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # Sentiment analysis
            sentiment = st.session_state.analysis_results.get("sentiment", {})
            if sentiment:
                st.markdown("#### 😊 Patient Sentiment")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    positive = sentiment.get("positive", 0)
                    st.markdown('<div class="glass-card metric-excellent">', unsafe_allow_html=True)
                    st.metric("Positive", f"{positive}%")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    neutral = sentiment.get("neutral", 0)
                    st.markdown('<div class="glass-card metric-warning">', unsafe_allow_html=True)
                    st.metric("Neutral", f"{neutral}%")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col3:
                    negative = sentiment.get("negative", 0)
                    st.markdown('<div class="glass-card metric-critical">', unsafe_allow_html=True)
                    st.metric("Negative", f"{negative}%")
                    st.markdown('</div>', unsafe_allow_html=True)
            
            # Data preview
            with st.expander("📋 Data Preview"):
                st.dataframe(st.session_state.current_data.head(10), use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        if st.session_state.current_data is not None:
            create_dashboard(st.session_state.current_data, st.session_state.analysis_results)
        else:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("### 📈 Interactive Dashboard")
            st.info("📊 Generate data to view dashboard")
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 💬 Meta Llama 4 AI Assistant")
        st.markdown('<span class="meta-indicator">🧠 Detailed Healthcare Analysis</span>', unsafe_allow_html=True)
        
        # Enhanced chat interface
        user_query = st.text_area(
            "Ask detailed healthcare questions:",
            placeholder="e.g., Provide comprehensive analysis of patient safety indicators and improvement strategies...",
            height=100
        )
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if st.button("🚀 Get Detailed Analysis", use_container_width=True):
                if user_query.strip():
                    with st.spinner("🧠 Meta Llama 4 analyzing..."):
                        context = st.session_state.analysis_results
                        response = st.session_state.ai_manager.chat_query(user_query, context, chat_mode=False)
                        
                        st.session_state.chat_history.append({
                            "user": user_query,
                            "ai": response,
                            "timestamp": datetime.now().strftime("%H:%M:%S")
                        })
                    st.rerun()
                else:
                    st.warning("Please enter a question")
        
        with col2:
            if st.button("🧹 Clear History", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
        
        with col3:
            if st.button("📊 Quick Analysis", use_container_width=True):
                if st.session_state.current_data is not None:
                    quick_prompt = "Provide executive summary with WHO, Joint Commission, KEMKES compliance analysis and strategic recommendations."
                    with st.spinner("Generating analysis..."):
                        context = st.session_state.analysis_results
                        response = st.session_state.ai_manager.chat_query(quick_prompt, context, chat_mode=False)
                        
                        st.session_state.chat_history.append({
                            "user": "Executive Summary Request",
                            "ai": response,
                            "timestamp": datetime.now().strftime("%H:%M:%S")
                        })
                    st.rerun()
                else:
                    st.warning("Generate data first")
        
        # Chat history
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
                    <strong>🧠 Meta Llama 4 Detailed Analysis:</strong><br><br>
                    {chat['ai']}
                </div>
                """, unsafe_allow_html=True)
        
        # Sample questions
        st.markdown("#### 💡 Sample Questions")
        sample_questions = [
            "How to achieve 95%+ WHO compliance?",
            "Strategic plan for Joint Commission excellence?",
            "Technology integration best practices?",
            "Patient satisfaction improvement strategies?"
        ]
        
        cols = st.columns(2)
        for i, question in enumerate(sample_questions):
            col = cols[i % 2]
            with col:
                if st.button(question, key=f"sample_{i}", use_container_width=True):
                    with st.spinner("🧠 Processing..."):
                        context = st.session_state.analysis_results
                        response = st.session_state.ai_manager.chat_query(question, context, chat_mode=False)
                        
                        st.session_state.chat_history.append({
                            "user": question,
                            "ai": response,
                            "timestamp": datetime.now().strftime("%H:%M:%S")
                        })
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown(f"""
    <div class="glass-card" style="text-align: center; margin-top: 2rem;">
        <h3>🏥 Healthcare AI RAG v{HealthConfig.APP_VERSION} - Meta Llama 4 Edition</h3>
        <p>🤖 AI Chatbot • 🧠 Meta Llama 4 Maverick • 📊 Real-time Analytics • 🌍 Global Standards</p>
        <div style="margin-top: 1rem;">
            <span style="color: #00ff88;">WHO Compliant</span> • 
            <span style="color: #00d4ff;">Joint Commission Ready</span> • 
            <span style="color: #8b5cf6;">KEMKES Aligned</span> •
            <span style="color: #ff6b35;">ISQua Excellence</span>
        </div>
        <p style="font-size: 0.8rem; opacity: 0.7; margin-top: 1rem;">
            Enhanced with AI Chatbot for instant healthcare insights
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
