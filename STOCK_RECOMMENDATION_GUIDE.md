# 🎯 Stock Recommendation Feature - Complete Guide

## What's New ✨

Your chatbot now answers BOTH types of investment questions:

### ✅ Specific Stock Analysis
"Should I invest $5000 in Tesla?"
"Is Microsoft a good investment with $10000?"

### ✅ Stock Recommendations (NEW!)
"Suggest best stocks to invest $5000"
"Which stocks should I buy with $10000?"
"What are the top investments?"

## How It Works

1. **Analyzes 15 Popular Stocks**: AAPL, MSFT, GOOGL, AMZN, TSLA, NVDA, META, NFLX, JPM, V, JNJ, PG, UNH, HD, DIS

2. **Scores Each Stock** (0-100 points):
   - Recommendation level (STRONG BUY = 50pts, BUY = 35pts, HOLD = 15pts)
   - Risk assessment (LOW = 30pts, MEDIUM = 15pts)
   - Market sentiment (POSITIVE = 20pts, NEUTRAL = 10pts)
   - P/E ratio valuation

3. **Returns Top 5 Stocks** ranked by investment score

4. **Provides Full Analysis**:
   - Financial metrics
   - Risk levels
   - Sentiment analysis
   - Share calculations
   - Detailed recommendations

## 🚀 Quick Start

```bash
python scripts/chatbot.py
```

Then ask:
```
You: Suggest best stocks to invest $5000
Assistant: 🎯 Finding the best stocks for $5,000...
[Analyzes stocks and provides top 5 recommendations]
```

## Example Output

```
Top Stock Recommendations:
1. MSFT (Microsoft) - Score: 95/100 - STRONG BUY
2. AAPL (Apple) - Score: 92/100 - STRONG BUY  
3. GOOGL (Google) - Score: 88/100 - BUY
4. NVDA (Nvidia) - Score: 85/100 - BUY
5. JPM (JPMorgan) - Score: 80/100 - BUY
```

## Features

✅ Analyzes 15 major stocks in your portfolio tier
✅ Calculates comprehensive investment scores
✅ Considers sentiment, risk, valuation
✅ Provides full financial analysis
✅ Shows market sentiment (positive/negative)
✅ Assesses risk levels (LOW/MEDIUM/HIGH)
✅ Calculates shares you can buy
✅ Stores analysis history

## Natural Language Support

The chatbot understands many ways of asking:
- "Suggest best stocks to invest $5000"
- "Which stocks should I buy with $10000?"
- "What are the top investments for $5000?"
- "Recommend the best stocks for $8000"
- "I have $10000, which stocks are best?"

## ⚠️ Important Notes

- This is AI-generated analysis, NOT financial advice
- Always consult with a qualified financial advisor
- Past performance ≠ Future results
- Diversify your portfolio
- Consider your risk tolerance
- Monitor investments regularly

## New Files Created

- `src/stock_recommender.py` - Stock recommendation engine
- `scripts/recommend_demo.py` - Recommendation demonstration

## API Keys Required

Make sure .env has:
- FMP_API_KEY (for stock data)
- NEWSAPI_API_KEY (for news sentiment)
- HUGGINGFACEHUB_API_TOKEN (for LLM)

