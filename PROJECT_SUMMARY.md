# LLM + RAG for Finance - Complete Project Summary

## 📋 Project Overview

This is a complete **AI-powered Financial Advisory System** that combines:
- **Real-time Financial Data** from Financial Modeling Prep API
- **News Analysis** from NewsAPI
- **LLM & RAG** (Retrieval-Augmented Generation) for intelligent insights
- **Interactive Chatbot** for investment recommendations

## 🎯 What You Can Do

### Mode 1: Demo Pipeline (`scripts/run_demo.py`)
Run a complete end-to-end demonstration showing:
1. Fetching stock data and news
2. Data preprocessing and cleaning
3. Creating AI embeddings
4. Building a knowledge base
5. Querying with RAG pipeline

### Mode 2: Interactive Chatbot (`scripts/chatbot.py`)
Have a conversation with an AI financial advisor:
```
You: Should I invest $10,000 in Apple?
Assistant: [Analyzes all data and provides investment recommendation]
```

## 📁 Project Structure

```
llm_rag_finance/
├── README.md                          # Project overview
├── CHATBOT_GUIDE.md                   # Chatbot usage guide
├── PROJECT_SUMMARY.md                 # This file
├── requirements.txt                   # Python dependencies
├── .env                               # API keys (keep secret!)
├── .gitignore                         # Git ignore file
├── start_chatbot.sh                   # Easy chatbot launcher
│
├── src/                               # Main Python package
│   ├── __init__.py
│   ├── config.py                      # Load environment variables
│   ├── data_fetch.py                  # Financial Modeling Prep API
│   ├── news_fetch.py                  # NewsAPI integration
│   ├── preprocess.py                  # Data cleaning & normalization
│   ├── embeddings.py                  # Create vector embeddings
│   ├── rag.py                         # RAG pipeline & LLM
│   └── financial_advisor.py           # AI Financial advisor
│
└── scripts/
    ├── run_demo.py                    # Demo script
    └── chatbot.py                     # Interactive chatbot
```

## 🚀 Quick Start

### 1. Install & Setup (First Time Only)

```bash
cd /Users/chintanshah/Documents/llm_rag_finance

# Create virtual environment
python -m venv .venv

# Activate it
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Chatbot

```bash
# Option A: Direct Python
/Users/chintanshah/Documents/llm_rag_finance/.venv/bin/python scripts/chatbot.py

# Option B: If venv is activated
python scripts/chatbot.py

# Option C: Using the startup script (after chmod +x)
bash start_chatbot.sh
```

### 3. Run the Demo

```bash
python scripts/run_demo.py
```

## 💬 Chatbot Examples

### Example 1: Basic Query
```
You: Should I invest $10,000 in Apple?
