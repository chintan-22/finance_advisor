# Financial Advisor Chatbot Guide

## Overview

The **Financial Advisor Chatbot** is an interactive AI-powered investment recommendation engine that helps users make informed investment decisions. It analyzes stocks, fetches real-time financial data, analyzes market sentiment from news, and provides comprehensive investment recommendations.

## Features

✨ **Intelligent Analysis**
- Fetches real-time stock data and financial metrics
- Analyzes 15+ recent news articles for market sentiment
- Calculates risk assessment based on company fundamentals
- Provides valuation analysis (P/E ratio, market cap, dividend yield, etc.)

🤖 **Conversational Interface**
- Natural language understanding of investment queries
- Interactive chat-based interface
- Conversation history tracking
- Simple command system

📊 **Comprehensive Recommendations**
- 5-level recommendation system (STRONG BUY → STRONG SELL)
- Detailed investment summary with key metrics
- Risk and sentiment assessment
- Share quantity calculation based on investment amount

## Installation

### Prerequisites
- Python 3.8+
- Virtual environment with dependencies installed

### Setup

```bash
# Navigate to project directory
cd /Users/chintanshah/Documents/llm_rag_finance

# Activate virtual environment (if not already activated)
source .venv/bin/activate

# Ensure all dependencies are installed
pip install -r requirements.txt
```

## Quick Start

### Starting the Chatbot

```bash
# Using the virtual environment Python directly
/Users/chintanshah/Documents/llm_rag_finance/.venv/bin/python scripts/chatbot.py

# Or if venv is activated:
python scripts/chatbot.py
```

### Example Conversations

**Example 1: Basic Investment Query**
```
Assistant: 🤖 FINANCIAL ADVISOR CHATBOT - AI INVESTMENT RECOMMENDATION ENGINE

You: Should I invest $10,000 in Apple?
