# 🚀 Streamlit App - Quick Start Guide

## Overview

The Financial Advisor is now available as a beautiful, interactive **Streamlit web application** with:

✅ **Real-time stock data** from Yahoo Finance  
✅ **Interactive charts** with Plotly  
✅ **AI-powered analysis** using LangChain & Transformers  
✅ **Modern UI/UX** with custom styling  
✅ **Export capabilities** (JSON, CSV)  
✅ **Analysis history** tracking  
✅ **Mobile-responsive** design  

---

## 🎯 Features

### 1. **Stock Analysis** 📊
- Enter any stock ticker symbol (AAPL, MSFT, GOOGL, etc.)
- Specify your investment amount
- Get AI-powered investment recommendations
- View:
  - Financial metrics (P/E ratio, dividend yield, market cap)
  - Interactive price charts with moving averages
  - Detailed analysis reports
  - Export options

### 2. **Stock Recommendations** 💡
- Enter your investment budget
- Get top 5-10 recommended stocks
- See:
  - Overall recommendation scores (0-100)
  - Risk assessment per stock
  - Market sentiment analysis
  - Score breakdown by category

### 3. **Analysis History** 📋
- View all past analyses
- Review previous recommendations
- Export historical data
- Clear history anytime

---

## 🚀 Quick Start

### Method 1: Using the Startup Script (Recommended)

```bash
# Navigate to project directory
cd /Users/chintanshah/Documents/llm_rag_finance

# Run the startup script
./run_streamlit.sh
```

The app will open automatically at `http://localhost:8501`

### Method 2: Direct Command

```bash
cd /Users/chintanshah/Documents/llm_rag_finance
source .venv/bin/activate
streamlit run app.py
```

---

## 🔗 Data Sources

### Real-Time Stock Data
The app now uses **multiple data sources** with intelligent fallback:

1. **Yahoo Finance** (Primary)
   - Live stock prices
   - Historical data
   - Company information
   - P/E ratios, dividend yields, market caps

2. **Alpha Vantage API** (Backup)
   - Real-time quotes
   - Technical indicators
   - Set API key in `.env` if you have one

3. **Sample Data** (Fallback)
   - Realistic stock prices
   - Historical averages calculated locally

### News Data
- **NewsAPI** for real-time market sentiment
- Configured in `.env`

---

## 📊 Using the Stock Analysis Feature

### Step 1: Navigate to "Stock Analysis"
- Click on "🔍 Stock Analysis" in the sidebar

### Step 2: Enter Stock Details
```
Stock Ticker Symbol: AAPL
Investment Amount: $5000
```

### Step 3: Click "Analyze Stock"
The app will:
1. Fetch live data from Yahoo Finance
2. Retrieve recent news articles
3. Analyze sentiment
4. Calculate risk metrics
5. Generate AI recommendation
6. Display interactive charts

### Step 4: View Results
- **Recommendation Card**: Overall verdict
- **Financial Metrics**: Key numbers
- **Price Chart**: 1-year history with moving averages
- **Detailed Analysis**: Full text report
- **Export**: Download as JSON or CSV

---

## 💡 Using the Stock Recommendations Feature

### Step 1: Navigate to "Stock Recommendations"
- Click on "📊 Stock Recommendations" in the sidebar

### Step 2: Enter Your Budget
```
Investment Budget: $5000
Number of Recommendations: 5
```

### Step 3: Click "Get Recommendations"
The system will analyze 15 popular stocks and rank them based on:
- Investment recommendation strength
- Risk assessment
- Market sentiment
- Valuation metrics

### Step 4: Review Recommendations
Each stock shows:
- Score (0-100)
- Recommendation level
- Risk classification
- Market sentiment
- Score breakdown chart

---

## 🎨 UI/UX Features

### Modern Design
- **Gradient buttons** with hover effects
- **Custom color scheme** (Purple/Blue gradient)
- **Responsive layout** that works on mobile
- **Interactive cards** with shadows and borders

### Data Visualization
- **Interactive charts** using Plotly
- **Moving averages** (50-day and 200-day)
- **Real-time price updates**
- **Score breakdown** visualizations

### User Experience
- **Spinners** while loading data
- **Success/error messages** with emojis
- **Expandable sections** for detailed info
- **Download buttons** for data export
- **Conversation history** tracking

---

## 📥 Export Options

### JSON Export
- Complete analysis in structured format
- Includes all financial metrics
- Timestamp for tracking
- Easy integration with other tools

### CSV Export
- Tabular format
- Perfect for spreadsheets
- Comparison between analyses
- Historical tracking

---

## ⚙️ Configuration

### Environment Variables
Edit `.env` file:

```bash
# Financial API Keys
FMP_API_KEY=your_fmp_key_here
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key_here

# News API
NEWSAPI_API_KEY=your_newsapi_key_here

# LLM Configuration
HUGGINGFACE_API_KEY=your_hf_key_here
```

### Streamlit Config
The app uses default settings. To customize:

1. Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
maxUploadSize = 200
enableCORS = false
```

2. Restart the app

---

## 🔍 How It Works

### Data Pipeline

```
User Input
    ↓
┌─────────────────────────────┐
│  Fetch Live Data            │
│  • Yahoo Finance (Primary)  │
│  • Alpha Vantage (Backup)   │
│  • Sample Data (Fallback)   │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  Fetch News & Sentiment     │
│  • NewsAPI Integration      │
│  • Keyword Analysis         │
│  • Trend Detection          │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  Process with RAG Pipeline  │
│  • Build Vector DB          │
│  • Semantic Search          │
│  • LLM Generation           │
└─────────────────────────────┘
    ↓
┌─────────────────────────────┐
│  Generate Recommendation    │
│  • Risk Assessment          │
│  • Sentiment Score          │
│  • Investment Grade         │
└─────────────────────────────┘
    ↓
Display Results with Charts
```

---

## ⚠️ Important Notes

### Data Accuracy
- Stock data from Yahoo Finance is real-time
- Historical data may have a slight delay
- News sentiment is AI-generated and indicative only

### API Limitations
- Yahoo Finance: No API key required ✅
- NewsAPI: Free tier (500 requests/day)
- Alpha Vantage: Free tier has rate limits

### Performance
- First load may take 10-15 seconds
- Chart generation takes 2-3 seconds
- Subsequent analyses are faster due to caching

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'yfinance'"

**Solution:**
```bash
source .venv/bin/activate
pip install yfinance streamlit plotly
```

### Issue: "No data available for TICKER"

**Causes:**
- Invalid ticker symbol
- Market not open (US markets)
- Network connectivity issue

**Solution:**
- Verify ticker is correct
- Try a major stock (AAPL, MSFT, GOOGL)
- Check internet connection

### Issue: Charts not displaying

**Solution:**
```bash
pip install --upgrade plotly
streamlit run app.py
```

### Issue: "Too many requests" from NewsAPI

**Solution:**
- Wait a few minutes before retrying
- Upgrade to paid NewsAPI plan
- Remove news analysis from config

---

## 🔒 Privacy & Security

- **No data stored** on servers
- **No tracking** of user actions
- **Local processing** of all inputs
- **Secure API calls** with encrypted keys
- All data stays in your environment

---

## 📚 Example Workflows

### Workflow 1: Research Before Investing

1. Open "Stock Analysis"
2. Analyze 3-5 stocks you're interested in
3. Compare metrics and recommendations
4. Export analyses for comparison
5. Review history before making decision

### Workflow 2: Get Recommendations

1. Open "Stock Recommendations"
2. Enter your budget ($5000)
3. Get top 5 recommendations
4. Click on each to see breakdown
5. Further analyze top 2-3 in Stock Analysis

### Workflow 3: Track Your Research

1. Perform multiple analyses over time
2. View history of all research
3. Export for record-keeping
4. Monitor how predictions align with reality

---

## 🚀 Advanced Features

### Coming Soon
- Portfolio optimization
- Risk-adjusted returns calculation
- Technical indicator integration
- Custom watchlist creation
- Alerts for price changes
- Mobile app version

---

## 📖 Documentation

For more information:
- [Main README](README.md) - Project overview
- [Stock Recommendation Guide](STOCK_RECOMMENDATION_GUIDE.md) - Scoring system
- [GitHub Repository](https://github.com/chintan-22/llm_rag_finance)

---

## 💬 Support

If you encounter issues:
1. Check troubleshooting section above
2. Verify all dependencies are installed
3. Check internet connectivity
4. Review API key configuration
5. Open an issue on GitHub

---

## 📝 License

This project is open source and available under the MIT License.

---

**Enjoy your AI-powered financial advisor! 🎉**

For live updates: `./run_streamlit.sh`
