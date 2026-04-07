# 🤖 LLM + RAG for Finance - AI Investment Advisor

## 📊 Project Overview

**AI-Powered Investment Recommendation System** that uses Large Language Models (LLM) and Retrieval-Augmented Generation (RAG) to provide intelligent stock investment analysis and recommendations.

This project combines:
- 📰 **Real-time financial data** from multiple APIs
- 🧠 **AI language models** for intelligent analysis
- 🎯 **Vector embeddings** for semantic search
- 💬 **Natural language interface** for easy interaction
- 📈 **Investment recommendations** with detailed insights

### ✨ What It Does

The system analyzes stocks and provides:
1. **Detailed Investment Analysis** - For any specific stock you ask about
2. **Stock Recommendations** - Top stocks ranked by investment quality
3. **Sentiment Analysis** - Market sentiment from recent news
4. **Risk Assessment** - Risk levels based on financial metrics
5. **Financial Metrics** - P/E ratios, market cap, dividends, etc.
6. **Investment Recommendations** - 5-level recommendation system

### 🎯 Key Features

- ✅ Analyze ANY stock with natural language questions
- ✅ Get recommendations for best stocks to invest
- ✅ Real-time news sentiment analysis
- ✅ Risk assessment and financial metrics
- ✅ Conversational AI interface
- ✅ Conversation history tracking
- ✅ Multiple query formats support
- ✅ Graceful fallbacks for API limitations

## 🏗️ System Architecture & Workflow

### Complete Data Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│                    USER NATURAL LANGUAGE QUERY                         │
│          "Should I invest $5000 in Tesla?"                             │
│          "Suggest best stocks to invest $5000"                         │
│                                                                         │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────────┐
                    │  QUERY PARSER      │
                    │  Extract ticker &  │
                    │  investment amount │
                    └────────┬───────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
                ▼                         ▼
        ┌──────────────┐         ┌──────────────────┐
        │ SPECIFIC     │         │ RECOMMENDATIONS  │
        │ STOCK        │         │ ENGINE           │
        │ ANALYSIS     │         │ (15 stocks)      │
        └────────┬─────┘         └────────┬─────────┘
                 │                        │
                 └────────────┬───────────┘
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
        ┌─────────────────┐      ┌──────────────────┐
        │ DATA FETCHING   │      │ DATA FETCHING    │
        │ • FMP API       │      │ • FMP API (15x)  │
        │ • NewsAPI       │      │ • NewsAPI (15x)  │
        │ • Stock Data    │      │ • News Data      │
        │ • News Articles │      │ • All stocks     │
        └────────┬────────┘      └────────┬─────────┘
                 │                        │
                 ▼                        ▼
        ┌─────────────────┐      ┌──────────────────┐
        │ PREPROCESSING   │      │ PREPROCESSING    │
        │ • Clean data    │      │ • Clean data     │
        │ • Normalize     │      │ • Normalize      │
        │ • Combine       │      │ • Combine        │
        └────────┬────────┘      └────────┬─────────┘
                 │                        │
                 ▼                        ▼
        ┌─────────────────┐      ┌──────────────────┐
        │ EMBEDDINGS      │      │ EMBEDDINGS       │
        │ • HuggingFace   │      │ • HuggingFace    │
        │ • Create vectors│      │ • Create vectors │
        │ • Chroma DB     │      │ • Chroma DB      │
        └────────┬────────┘      └────────┬─────────┘
                 │                        │
                 ▼                        ▼
        ┌─────────────────┐      ┌──────────────────┐
        │ RAG ANALYSIS    │      │ INVESTMENT SCORE │
        │ • Query chain   │      │ • Score calc     │
        │ • Sentiment     │      │ • Rank stocks    │
        │ • Risk assess   │      │ • Top 5          │
        └────────┬────────┘      └────────┬─────────┘
                 │                        │
                 └────────────┬───────────┘
                              │
                              ▼
                  ┌──────────────────────┐
                  │  RECOMMENDATION      │
                  │  GENERATION          │
                  │  • Financial metrics │
                  │  • Risk level        │
                  │  • Sentiment         │
                  │  • Shares calc       │
                  └────────┬─────────────┘
                           │
                           ▼
                  ┌──────────────────────┐
                  │  USER OUTPUT         │
                  │  📊 Recommendation   │
                  │  📈 Analysis         │
                  │  ⚠️ Disclaimer      │
                  └──────────────────────┘

```

## 🔄 Project Workflow

### Mode 1: Streamlit Web Interface (Recommended) ⭐ NEW

```bash
./run_chatbot.sh
# Opens browser at http://localhost:8501
```

**Features:**
- 💻 Beautiful modern web interface with gradient design
- 💬 Real-time conversational chat with message history
- 🎯 Smart conversation flow: Budget → Risk Tolerance → Recommendations
- 📊 Live user profile card showing budget & risk level
- 🚀 Instant stock recommendations upon providing budget + risk
- 📱 Mobile-friendly responsive design

**Workflow:**
1. User enters investment amount (e.g., "$5000")
2. Chatbot asks for risk tolerance (Conservative/Moderate/Aggressive)
3. System generates **risk-aware recommendations** instantly
4. Top 5 stocks displayed with detailed analysis
5. Different recommendations for different risk profiles

### Mode 2: Interactive CLI Chatbot

```bash
python scripts/chatbot.py
```

**Workflow:**
1. User asks investment question in natural language
2. Chatbot parses query and extracts ticker/amount
3. System fetches latest data from APIs
4. Data is preprocessed and cleaned
5. Embeddings created and stored in Chroma DB
6. RAG chain analyzes the data
7. AI generates investment recommendation
8. Results displayed to user with analysis

### Mode 3: Demo Pipeline

```bash
python scripts/run_demo.py
```

**Workflow:**
1. Demonstrates complete 5-step pipeline
2. Fetches Apple (AAPL) data
3. Preprocesses and creates embeddings
4. Builds RAG chain
5. Shows example queries
6. Provides interactive mode for custom queries

## 📋 Features & Capabilities

### Analysis Features
- ✅ **Real-time stock prices** via yfinance API
- ✅ **Financial metrics** (P/E, EPS, market cap, dividend yield)
- ✅ **50-day and 200-day price averages**
- ✅ **News sentiment analysis** (15+ articles)
- ✅ **Risk assessment** (LOW/MEDIUM/HIGH)
- ✅ **Share quantity calculation**
- ✅ **Investment recommendation** (5-level system)
- ✅ **Risk-aware stock ranking** - Different stocks for different risk tolerances
- ✅ **Beautiful Streamlit web interface** with gradient design
- ✅ **Conversational AI** that understands natural language

### Risk-Aware Recommendations ⭐ NEW

The recommendation engine now adapts stock suggestions based on user risk tolerance:

| Risk Level | Characteristics | Example Stocks |
|-----------|-----------------|-----------------|
| **Conservative (LOW)** | Stable, dividend-paying, lower volatility | MSFT, JNJ, UNH, JPM |
| **Moderate (MEDIUM)** | Balance of growth and stability | GOOGL, DIS, V, AMZN |
| **Aggressive (HIGH)** | High growth potential, higher volatility | TSLA, NVDA, META, NFLX |

**Scoring System:**
- Matches user risk tolerance with stock risk profile
- Conservative investors get +30 bonus for LOW-risk stocks
- Aggressive investors get +30 bonus for HIGH-risk stocks
- Moderate investors get balanced scoring across all risk levels

### Query Types Supported

**Specific Stock Analysis:**
```
"Should I invest $5000 in Tesla?"
"Is Microsoft a good investment with $10000?"
"Can I invest $20000 in Apple?"
"What about putting $15000 into Google?"
"Analyze Amazon with my $8000"
```

**Stock Recommendations:**
```
"Suggest best stocks to invest $5000"
"Which stocks should I buy with $10000?"
"What are the top investments for $5000?"
"Recommend the best stocks"
"I have $8000, which stocks are best?"
```

### Analyzed Stocks (15 Total)
- **Tech Giants:** AAPL, MSFT, GOOGL, AMZN, META, NFLX
- **High Growth:** TSLA, NVDA
- **Financial:** JPM, V
- **Healthcare:** JNJ, UNH
- **Consumer:** PG, HD, DIS

## 🛠️ Tech Stack

### Web & UI
- **Streamlit 1.50.0** - Modern web UI for chatbot interface
- **Plotly** - Interactive charts and visualizations

### Core Technologies
- **Python 3.9+** - Programming language
- **LangChain 0.3.28** - LLM orchestration & RAG framework
- **Hugging Face** - Embeddings & language models
  - `sentence-transformers` - For vector embeddings (all-MiniLM-L6-v2)
  - `transformers` - For LLM loading
  - `huggingface-hub` - Model management

### Data & Financial APIs
- **yfinance** - Real-time stock prices and financial data from Yahoo Finance
- **pandas** - Data manipulation & analysis
- **numpy** - Numerical computing
- **scikit-learn** - ML utilities & risk calculations
- **scipy** - Scientific computing

### Vector Database & Search
- **Chroma 1.5.5** - Vector database for embeddings
- **Persistent storage** - Saves embeddings for reuse

### External APIs
- **NewsAPI** - Real news data (newsapi-python 0.2.7)
- **Financial Modeling Prep (FMP)** - Stock financial data
- **yfinance** - Yahoo Finance data
- **requests 2.32.5** - HTTP requests

### Utilities
- **python-dotenv** - Environment variable management
- **PyTorch 2.8.0** - Deep learning backend

## 📁 Repository Layout

```
llm_rag_finance/
├── README.md                           # Project documentation
├── STOCK_RECOMMENDATION_GUIDE.md       # Stock recommendation feature guide
├── CHATBOT_GUIDE.md                    # Chatbot usage guide
├── PROJECT_SUMMARY.md                  # Architecture overview
├── COMPLETION_SUMMARY.py               # Project completion info
│
├── .env                                # API keys (keep secret!)
├── .gitignore                          # Git ignore rules
├── requirements.txt                    # Python dependencies
│
├── src/                                # Main Python package
│   ├── __init__.py
│   ├── config.py                       # Environment configuration
│   ├── data_fetch.py                   # FMP & yfinance API helpers
│   ├── news_fetch.py                   # NewsAPI helpers
│   ├── preprocess.py                   # Data cleaning & normalization
│   ├── embeddings.py                   # Vector embeddings & Chroma DB
│   ├── rag.py                          # RAG pipeline with LLM
│   ├── financial_advisor.py            # Investment analysis engine
│   └── stock_recommender.py            # Stock recommendation engine (risk-aware)
│
├── scripts/                            # Executable scripts
│   ├── run_demo.py                     # Complete demo pipeline
│   ├── chatbot.py                      # Interactive CLI chatbot
│   └── recommend_demo.py               # Stock recommendation demo
│
├── streamlit_chatbot.py                # Modern Streamlit web interface ⭐ NEW
├── run_chatbot.sh                      # Convenient launcher script (activates venv)
│
└── docs/chroma_rag/                    # Persistent vector database
```

## 🚀 Quick Start Guide

### Step 1: Setup Environment

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install all dependencies
pip install -r requirements.txt
```

### Step 2: Configure API Keys

Create `.env` file in project root:

```env
FMP_API_KEY=your_key_here
NEWSAPI_API_KEY=your_key_here
HUGGINGFACEHUB_API_TOKEN=your_token_here
CHROMA_PERSIST_DIR=docs/chroma/
CHROMA_PERSIST_DIR_RAG=docs/chroma_rag/
```

### Step 3a: Run the Streamlit Web Interface (Recommended) ⭐

```bash
./run_chatbot.sh
```

Then open browser to `http://localhost:8501`

**Try these inputs:**
```
Budget: "I have $5000 to invest"
Risk: "I'm conservative" / "I'm moderate" / "I'm aggressive"
→ Get instant risk-aware stock recommendations!
```

### Step 3b: Run the CLI Chatbot

```bash
python scripts/chatbot.py
```

**Example Questions:**
```
You: Should I invest $5000 in Tesla?
You: Suggest best stocks to invest $10000
You: Is Microsoft a good investment?
You: What's your recommendation for $8000?
```

## 📊 Example Workflow

### Complete Flow for a User Query

```
User Input: "Should I invest $5000 in Apple?"
    │
    ├─→ Query Parser: Extracts AAPL, $5000
    │
    ├─→ Data Fetching:
    │   ├─ FMP API: Stock price, P/E, market cap, dividends
    │   └─ NewsAPI: 15+ recent articles about Apple
    │
    ├─→ Data Preprocessing:
    │   ├─ Clean and normalize data
    │   ├─ Combine financial + news data
    │   └─ Handle missing values
    │
    ├─→ Embeddings Creation:
    │   ├─ Convert text to vectors (HuggingFace)
    │   ├─ Store in Chroma DB
    │   └─ Create semantic index
    │
    ├─→ RAG Analysis:
    │   ├─ Retrieve relevant documents
    │   ├─ Query LLM for analysis
    │   └─ Generate insights
    │
    ├─→ Investment Scoring:
    │   ├─ Calculate risk level
    │   ├─ Analyze sentiment
    │   ├─ Assess valuation
    │   └─ Generate recommendation
    │
    └─→ Output to User:
        ├─ 📈 Recommendation: STRONG BUY
        ├─ 💰 Financial Metrics
        ├─ 📰 Sentiment Analysis
        ├─ ⚠️ Risk Assessment
        └─ 📋 Important Disclaimers
```

## 🎯 Recommendation Scoring System

### Investment Score Calculation

| Factor | Max Points | Description |
|--------|-----------|-------------|
| **Recommendation** | 50 | STRONG BUY (50), BUY (35), HOLD (15), SELL (0) |
| **Risk Level** | 30 | LOW (30), MEDIUM (15), HIGH (0) |
| **Sentiment** | 20 | POSITIVE (20), NEUTRAL (10), NEGATIVE (0) |
| **Valuation** | 10 | P/E < 20 (10 bonus points) |
| **TOTAL** | **100** | Final investment score |

### Recommendation Levels

- 🟢 **STRONG BUY** - Excellent opportunity (Score: 85+)
- 🟢 **BUY** - Good opportunity (Score: 70-84)
- 🟡 **HOLD** - Neutral, wait (Score: 50-69)
- 🔴 **SELL** - Consider alternatives (Score: 30-49)
- 🔴 **STRONG SELL** - Avoid (Score: < 30)

## 📚 Documentation

For detailed information, see:
- **[CHATBOT_GUIDE.md](CHATBOT_GUIDE.md)** - Interactive chatbot usage
- **[STOCK_RECOMMENDATION_GUIDE.md](STOCK_RECOMMENDATION_GUIDE.md)** - Recommendation engine
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Architecture details
- **[COMPLETION_SUMMARY.py](COMPLETION_SUMMARY.py)** - Project info script

## ⚙️ How Each Component Works

### 1. **data_fetch.py** - Financial Data Retrieval
- Fetches stock quotes from Financial Modeling Prep API
- Retrieves: Price, P/E ratio, EPS, market cap, dividends, etc.
- Handles API errors with sample data fallback

### 2. **news_fetch.py** - News & Sentiment Data
- Fetches latest news articles from NewsAPI
- Filters by stock ticker and date range
- Collects 15+ articles for sentiment analysis

### 3. **preprocess.py** - Data Cleaning & Preparation
- Removes duplicates and missing values
- Normalizes text and numerical values
- Combines financial and news data
- Handles special data types (dicts, lists)

### 4. **embeddings.py** - Vector Embeddings
- Creates semantic embeddings using HuggingFace models
- Stores embeddings in Chroma vector database
- Enables semantic similarity search
- Persists vectors for reuse

### 5. **rag.py** - Retrieval Augmented Generation
- Builds RAG chain with LLM
- Retrieves relevant documents
- Generates contextual responses
- Falls back to MockLLM if needed

### 6. **financial_advisor.py** - Investment Analysis Engine
- Orchestrates full analysis pipeline
- Calculates risk levels from metrics
- Analyzes news sentiment
- Generates recommendations

### 7. **stock_recommender.py** - Stock Ranking System
- Analyzes 15 popular stocks
- Scores each stock (0-100)
- Ranks by investment quality
- Returns top 5 recommendations

## 🔐 Security & API Keys

- ✅ Use `.env` file for sensitive data
- ✅ Never commit `.env` to git
- ✅ Add `.env` to `.gitignore`
- ✅ Rotate keys regularly
- ✅ Use free tier APIs for testing

## 🎓 Learning Outcomes

This project teaches:
- ✅ Building RAG pipelines with LangChain
- ✅ Working with LLMs and embeddings
- ✅ Vector database operations (Chroma)
- ✅ API integration and data fetching
- ✅ NLP and sentiment analysis
- ✅ Building conversational AI systems
- ✅ Production-ready error handling

## ⚠️ Important Disclaimers

- 🔴 **NOT financial advice** - AI analysis only
- 🔴 **Consult professionals** - Before investing
- 🔴 **Risk awareness** - Always understand risks
- 🔴 **Diversify portfolio** - Don't put all in one stock
- 🔴 **Past ≠ Future** - Historical data doesn't guarantee results
- 🔴 **Monitor regularly** - Check investments frequently

## 🐛 Troubleshooting

### Issue: "HTTP 403 Forbidden" from FMP API
**Solution:** FMP free tier has limitations. System falls back to sample data automatically.

### Issue: Model loading takes too long
**Solution:** First run loads the model. Subsequent runs use cache. Be patient on first run.

### Issue: No environment variables found
**Solution:** Make sure `.env` file exists in project root with required keys.

### Issue: Chroma DB not found
**Solution:** First run creates the database. It will be at `docs/chroma_rag/`

## 🚀 Recent Updates & Completed Features

✅ **Streamlit Web Interface** - Beautiful, modern web UI with gradient design  
✅ **Real-time Stock Prices** - yfinance API integration for live data  
✅ **Risk-Aware Recommendations** - Different stocks for Conservative/Moderate/Aggressive investors  
✅ **Risk Tolerance Detection** - Smart NLP to extract risk preference from user input  
✅ **Instant Recommendations** - Generate top 5 stocks immediately after budget + risk provided  
✅ **Conversation Flow** - Smart chatbot that asks for missing information  
✅ **Beautiful UI** - Gradient header, message bubbles, user profile card  
✅ **Session State Management** - Chat history and user profile tracking  
✅ **Responsive Design** - Works on desktop and mobile browsers  

## 🚀 Future Enhancements

- [ ] Portfolio tracking and optimization
- [ ] Technical analysis indicators (RSI, MACD, Bollinger Bands)
- [ ] Real-time price alerts and notifications
- [ ] User authentication and profiles
- [ ] Database for persistent chat history
- [ ] Advanced risk metrics (Value at Risk, Sharpe Ratio)
- [ ] Sector and industry filtering
- [ ] More advanced ML models for prediction
- [ ] Export analysis reports to PDF
- [ ] Multi-portfolio management

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

---

**Made with ❤️ for AI-powered investment analysis**

For questions or support, open an issue on GitHub.
