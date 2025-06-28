# healthcare-ai-rag
Agentic AI and RAG-powered application published through Streamlit that will help modern hospital and healthcare quality systems based on agentic AI, with a focus on AI workflow automation which is designed to help hospital quality systems utilize AI technology effectively

# 🏥 Agentic AI & RAG for Healthcare Quality Management

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![AI](https://img.shields.io/badge/AI-Powered-00D4AA?style=for-the-badge)

A comprehensive Agentic AI application designed to revolutionize healthcare quality management through advanced analytics, decision support, and automated workflow optimization.

## 🚀 Features

### 📊 **Advanced Data Analysis**
- **Multimodal Data Processing**: Support for Excel and CSV files
- **Automated Insights Generation**: AI-powered pattern recognition
- **Statistical Analysis with RAG**: Enhanced analysis using healthcare knowledge base
- **Real-time Data Validation**: Comprehensive data quality checks

### ⚖️ **Decision Support Systems**
- **AHP (Analytic Hierarchy Process)**: Multi-criteria decision analysis
- **ANP (Analytic Network Process)**: Network-based decision modeling
- **Consistency Validation**: Automated consistency ratio calculations
- **Priority Ranking**: Intelligent alternative evaluation

### 📈 **Interactive Visualizations**
- **Dynamic Charts**: Histogram, boxplot, scatter plot, heatmap
- **Real-time Updates**: Interactive plotly-based visualizations
- **Group Analysis**: Split visualizations by categorical variables
- **Export Capabilities**: Save charts and analysis results

### 🎯 **AI-Powered Scenario Planning**
- **Monte Carlo Simulations**: Statistical scenario generation
- **Risk Assessment**: Automated risk analysis and reporting
- **Parameter Optimization**: AI-guided parameter tuning
- **Predictive Modeling**: Future state predictions

### 📰 **News Intelligence**
- **Real-time News Monitoring**: Healthcare industry updates
- **Keyword-based Search**: Customizable news filtering
- **Source Aggregation**: Multiple news source integration
- **Trend Analysis**: Pattern recognition in healthcare news

### 🤖 **AI Assistant with RAG**
- **Natural Language Queries**: Ask questions in plain English
- **Healthcare Knowledge Base**: Specialized medical and quality management insights
- **Contextual Responses**: Data-aware intelligent responses
- **Continuous Learning**: Adaptive knowledge enhancement

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Local Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/healthcare-ai-rag.git
cd healthcare-ai-rag
```

2. **Create virtual environment**
```bash
python -m venv healthcare_ai_env
source healthcare_ai_env/bin/activate  # On Windows: healthcare_ai_env\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run app.py
```

5. **Access the application**
Open your browser and go to `http://localhost:8501`

### Streamlit Cloud Deployment

1. **Fork this repository** to your GitHub account

2. **Go to [Streamlit Cloud](https://share.streamlit.io/)**

3. **Deploy your app**:
   - Connect your GitHub account
   - Select this repository
   - Choose `app.py` as the main file
   - Click "Deploy"

## 📋 Usage Guide

### 1. Data Upload and Analysis
1. Navigate to **"📊 Data Analysis"**
2. Upload your healthcare data (CSV or Excel format)
3. Click **"🔍 Perform Comprehensive Analysis"**
4. Review AI-generated insights and recommendations

### 2. Decision Analysis
1. Go to **"⚖️ Decision Methods"**
2. Choose between AHP or ANP analysis
3. Configure your comparison matrices
4. Review priority rankings and consistency ratios

### 3. Data Visualization
1. Visit **"📈 Visualization"**
2. Select your preferred chart type
3. Configure axes and grouping variables
4. Interact with dynamic visualizations

### 4. Scenario Planning
1. Access **"🎯 Scenario Planning"**
2. Define base parameters for simulation
3. Run Monte Carlo simulations
4. Analyze risk distributions and outcomes

### 5. AI Assistant
1. Open **"🤖 AI Assistant"**
2. Ask questions about healthcare quality management
3. Receive context-aware responses with actionable insights
4. Explore the integrated knowledge base

## 📊 Sample Data

The application works with various healthcare data formats:

- **Quality Metrics**: Patient satisfaction scores, readmission rates, infection rates
- **Operational Data**: Bed occupancy, staff productivity, resource utilization
- **Clinical Indicators**: Mortality rates, treatment outcomes, care coordination metrics
- **Financial Data**: Cost per case, revenue cycles, efficiency ratios

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
# Optional: QWEN: Qwen 2.5 VL 32B Instruct (free)
API Key for enhanced AI features
QWEN 2.5 VL 32B Instruct_API_KEY=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


# Optional: Custom knowledge base URL
KNOWLEDGE_BASE_URL=https://your-knowledge-base.com

# Application settings
DEBUG_MODE=false
LOG_LEVEL=INFO
```

### Customization Options

#### Adding Custom Knowledge Base Entries
Edit the `RAGSystem._initialize_knowledge_base()` method in `app.py` to add domain-specific knowledge.

#### Extending Visualization Types
Add new chart types in the `show_visualization_page()` function.

#### Custom Analysis Modules
Create new analysis modules by extending the `AgenticAI` class.

## 🏗️ Project Structure

```
healthcare-ai-rag/
├── app.py                  # Main application file
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── .streamlit/
│   └── config.toml        # Streamlit configuration
├── data/
│   └── sample_data.csv    # Sample healthcare data
├── docs/
│   ├── user_guide.md      # Detailed user guide
│   └── api_reference.md   # API documentation
└── tests/
    ├── test_data_analysis.py
    ├── test_decision_methods.py
    └── test_ai_assistant.py
```

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/ -v
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check our [User Guide](docs/user_guide.md)
- **Issues**: Report bugs on [GitHub Issues](https://github.com/yourusername/healthcare-ai-rag/issues)
- **Discussions**: Join our [GitHub Discussions](https://github.com/yourusername/healthcare-ai-rag/discussions)

## 🚀 Roadmap

### Current Version (v1.0)
- ✅ Basic data analysis and visualization
- ✅ AHP/ANP decision support
- ✅ AI assistant with RAG
- ✅ Scenario planning capabilities

### Upcoming Features (v1.1)
- 🔄 Real-time data streaming
- 🔄 Advanced ML models integration
- 🔄 Multi-language support
- 🔄 Enhanced security features

### Future Releases
- 📅 API integration with hospital systems
- 📅 Mobile application
- 📅 Advanced reporting and compliance modules
- 📅 Integration with electronic health records (EHR)

## 🏆 Acknowledgments

- Healthcare quality management best practices from Joint Commission
- AI and machine learning frameworks from scikit-learn
- Visualization capabilities powered by Plotly
- Web framework provided by Streamlit

---

**Made with ❤️ for Healthcare Quality Management**
