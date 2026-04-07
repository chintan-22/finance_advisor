# 💬 Financial Advisor Chatbot - Streamlit Version

## What You Have Now

✅ **Real Conversational Streamlit Chatbot** - No hallucinations, clean interface  
✅ **Chat naturally** - Just type what you want to know  
✅ **Budget extraction** - Says "I have $5000" and it understands  
✅ **Stock analysis** - Mention stocks and get real data  
✅ **Smart recommendations** - Get top stocks based on your profile  
✅ **Educational content** - Learn about P/E, dividends, diversification  
✅ **Beautiful UI** - Modern gradient interface with profile tracking  

---

## 🚀 Quick Start

### Option 1: Simple (Recommended)
```bash
cd /Users/chintanshah/Documents/llm_rag_finance
chmod +x run_chatbot.sh
./run_chatbot.sh
```

### Option 2: Direct Command
```bash
cd /Users/chintanshah/Documents/llm_rag_finance
streamlit run streamlit_chatbot.py
```

Then open: **http://localhost:8501**

---

## 💬 How to Use

Just type naturally! Examples:

```
"I have $5000 to invest"
"Tell me about Apple"
"I'm conservative, recommend dividend stocks"
"What's a P/E ratio?"
"How many shares of Tesla can I buy?"
"Compare Microsoft and Google"
```

---

## 🤖 What the Chatbot Understands

### 1. Budget Information
```
"I have $5000"
"I want to invest $10000"
"With $20k to invest"
```
✅ Automatically detected and stored in your profile

### 2. Risk Tolerance
```
"I'm conservative"
"I want safe investments"
"I prefer growth stocks"
"I'm aggressive with risk"
```
✅ LOW / MEDIUM / HIGH automatically detected

### 3. Stock Analysis
```
"What about Apple?"
"Tell me about Tesla"
"Analyze Microsoft"
"How's Google doing?"
```
✅ Fetches real live prices and P/E ratios

### 4. Recommendations
```
"Recommend stocks"
"What should I buy with $10000?"
"Best dividend stocks"
"Suggest growth stocks"
```
✅ Gets top 5 stocks scored 0-100

### 5. Education
```
"What's a P/E ratio?"
"Explain dividends"
"What is diversification?"
"How to manage risk?"
```
✅ Detailed educational responses

---

## 👤 Your Profile (Sidebar)

The chatbot automatically builds your profile:

- 💰 **Budget** - How much you want to invest
- ⚠️ **Risk Tolerance** - Conservative/Moderate/Aggressive
- 📈 **Interested Stocks** - Stocks you've asked about
- 🎯 **Investment Goals** - Your investment style

Visible in the sidebar at all times!

---

## ⚙️ Features

✨ **Smart Extraction**
- Automatically finds "$5000" in "I have $5000 to invest"
- Detects "conservative" in natural sentences
- Recognizes stock tickers (AAPL, MSFT, TSLA, etc.)

✨ **Real Data**
- Live stock prices from Yahoo Finance
- P/E ratios, market caps, dividend yields
- Not sample data - REAL current prices

✨ **Conversation Memory**
- Remembers your budget throughout chat
- Tracks stocks you're interested in
- Stores your risk tolerance

✨ **Multiple Topics**
- Stock analysis
- Recommendations
- Educational content
- Goal-based advice
- Share calculations

---

## ⚠️ Important

🔴 **This is NOT financial advice**
- AI-generated analysis only
- Always consult qualified financial advisors
- Do your own research
- Past performance ≠ future results

---

## Troubleshooting

**Issue**: "Module not found"  
**Solution**: 
```bash
cd /Users/chintanshah/Documents/llm_rag_finance
source .venv/bin/activate
pip install -r requirements.txt
```

**Issue**: "Port 8501 already in use"  
**Solution**:
```bash
streamlit run streamlit_chatbot.py --logger.level=debug --client.toolbarMode=minimal
```

**Issue**: Chat not responding  
**Solution**: Reload the page or click "Clear Conversation" in sidebar

---

## Files

- **streamlit_chatbot.py** - The main chatbot (this is what you run!)
- **run_chatbot.sh** - Startup script for easy launching
- **src/data_fetch.py** - Real stock data fetching
- **src/financial_advisor.py** - Analysis engine
- **src/stock_recommender.py** - Recommendation engine

---

## Ready to Chat?

```bash
./run_chatbot.sh
```

Then just start talking about your investment goals! 🚀💬

The chatbot will understand you naturally. No commands, no confusion, just real investment advice.

---

**Questions?** Look at the example buttons when you start - they'll show you exactly how to talk to it! 💡
