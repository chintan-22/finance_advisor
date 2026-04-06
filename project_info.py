#!/usr/bin/env python3
"""
Quick start guide and project information script.
Run this to understand the project and get started.
"""

def print_project_info():
    """Print comprehensive project information."""
    
    info = """
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║         🤖 LLM + RAG FOR FINANCE - COMPLETE PROJECT GUIDE 🤖             ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

📌 PROJECT DESCRIPTION
══════════════════════════════════════════════════════════════════════════════

This is an AI-powered Financial Advisory System that helps users make informed
investment decisions. It combines:

  ✓ Real-time financial data from Financial Modeling Prep API
  ✓ News analysis from NewsAPI  
  ✓ AI embeddings with Hugging Face sentence transformers
  ✓ Vector database (Chroma) for semantic search
  ✓ LLM-powered RAG pipeline for intelligent analysis
  ✓ Interactive chatbot interface for natural conversations

══════════════════════════════════════════════════════════════════════════════

🎯 TWO WAYS TO USE THIS PROJECT
══════════════════════════════════════════════════════════════════════════════

┌─ MODE 1: INTERACTIVE CHATBOT (Recommended for Users) ─────────────────────┐
│                                                                            │
│  Run: python scripts/chatbot.py                                           │
│                                                                            │
│  This gives you an interactive experience:                               │
│  • Ask natural language questions about stocks                            │
│  • Get instant AI-powered investment recommendations                     │
│  • Track conversation history                                            │
│  • See detailed analysis reports                                          │
│                                                                            │
│  Example conversation:                                                    │
│    You: Should I invest $10,000 in Apple?                                │
│    Assistant: Analyzing AAPL for $10,000.00 investment...                │
│    [Fetches data, analyzes sentiment, calculates risk]                   │
│    📈 INVESTMENT RECOMMENDATION: STRONG BUY                               │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

┌─ MODE 2: DEMO PIPELINE (Educational, Shows Full Flow) ─────────────────────┐
│                                                                            │
│  Run: python scripts/run_demo.py                                          │
│                                                                            │
│  This demonstrates the complete pipeline:                                 │
│  1. Fetch stock data & news                                               │
│  2. Preprocess & clean data                                               │
│  3. Create AI embeddings                                                  │
│  4. Build knowledge base with Chroma                                      │
│  5. Query with RAG pipeline                                               │
│                                                                            │
│  Good for understanding how the system works internally.                 │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘

══════════════════════════════════════════════════════════════════════════════

🚀 GETTING STARTED (3 Simple Steps)
══════════════════════════════════════════════════════════════════════════════

STEP 1: Navigate to project directory
────────────────────────────────────────
  $ cd /Users/chintanshah/Documents/llm_rag_finance


STEP 2: Activate virtual environment (if not already)
──────────────────────────────────────────────────────
  $ source .venv/bin/activate


STEP 3: Run the chatbot!
────────────────────────
  $ python scripts/chatbot.py


That's it! 🎉

══════════════════════════════════════════════════════════════════════════════

💡 CHATBOT USAGE EXAMPLES
══════════════════════════════════════════════════════════════════════════════

Natural Language Queries (The chatbot understands all these):

  1. "Should I invest $10,000 in Apple?"
  2. "I have $5000, is Tesla a good investment?"
  3. "Can I invest $20000 in Microsoft?"
  4. "What about putting $15000 into Google?"
  5. "Analyze Amazon with my $8000"

Available Commands (Type these for special functions):

  • report    → Show the latest investment analysis report
  • history   → View your conversation history
  • clear     → Clear conversation history
  • help      → Show detailed help menu
  • exit      → Exit the chatbot

══════════════════════════════════════════════════════════════════════════════

📊 WHAT THE CHATBOT ANALYZES
══════════════════════════════════════════════════════════════════════════════

For each investment query, the system analyzes:

  Financial Metrics:
    ✓ Current stock price
    ✓ Market capitalization
    ✓ P/E Ratio (Price-to-Earnings)
    ✓ Earnings Per Share (EPS)
    ✓ Dividend Yield
    ✓ 50-day and 200-day price averages

  Market Sentiment:
    ✓ Fetches 15+ recent news articles
    ✓ Analyzes sentiment (positive/negative/neutral)
    ✓ Identifies key trends and catalysts

  Risk Assessment:
    ✓ Evaluates company size and stability
    ✓ Assesses valuation reasonableness
    ✓ Determines risk level (LOW/MEDIUM/HIGH)

  Investment Recommendation:
    ✓ STRONG BUY  → Excellent opportunity
    ✓ BUY         → Good opportunity
    ✓ HOLD        → Wait for better conditions
    ✓ SELL        → Consider alternatives
    ✓ STRONG SELL → Avoid this investment

══════════════════════════════════════════════════════════════════════════════

⚙️ SYSTEM ARCHITECTURE
══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE (Chatbot)                         │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
        ┌───────▼────────┐          ┌────────▼────────┐
        │ Parse Query    │          │ Generate Answer │
        │ (Extract      │          │ (Financial      │
        │  ticker &     │          │  Advisor)       │
        │  amount)      │          │                 │
        └───────┬────────┘          └────────▲────────┘
                │                             │
                └──────────────┬──────────────┘
                               │
        ┌──────────────────────┴──────────────────────┐
        │                                             │
   ┌────▼─────────┐                          ┌───────▼────────┐
   │ Data Fetching│                          │  AI Analysis   │
   ├───────────────┤                          ├────────────────┤
   │• FMP API      │                          │• Embeddings    │
   │  (Stock data) │                          │• Vector DB     │
   │• NewsAPI      │                          │• RAG Pipeline  │
   │  (News)       │                          │• LLM           │
   └───────┬───────┘                          └────────────────┘
           │                                         │
           └─────────────────┬──────────────────────┘
                             │
                ┌────────────▼─────────────┐
                │  Preprocessing Engine    │
                ├─────────────────────────┤
                │ • Data cleaning         │
                │ • Text normalization    │
                │ • Sentiment analysis    │
                │ • Risk calculation      │
                └─────────────────────────┘

══════════════════════════════════════════════════════════════════════════════

📚 PROJECT FILES
══════════════════════════════════════════════════════════════════════════════

Core Modules (src/):
  • config.py          → Load API keys from .env
  • data_fetch.py      → Fetch stock data from FMP
  • news_fetch.py      → Fetch news from NewsAPI
  • preprocess.py      → Clean and prepare data
  • embeddings.py      → Create vector embeddings
  • rag.py             → RAG pipeline & LLM
  • financial_advisor.py → Investment analysis engine

Scripts:
  • run_demo.py        → Complete demo pipeline
  • chatbot.py         → Interactive chatbot

Configuration:
  • .env               → Your API keys (SECRET!)
  • requirements.txt   → Python dependencies
  • .gitignore         → Files to ignore in git

════════════════════════════════════════════════════════════════════════════

⚠️  IMPORTANT DISCLAIMERS
════════════════════════════════════════════════════════════════════════════

🔴 THIS IS NOT FINANCIAL ADVICE!
   The recommendations provided are AI-generated analysis based on available
   data. They are NOT professional financial advice.

🔴 ALWAYS CONSULT WITH A PROFESSIONAL!
   Before making any investment decisions, consult with a qualified financial
   advisor or investment professional.

🔴 PAST PERFORMANCE ≠ FUTURE RESULTS!
   Historical data and trends do not guarantee future performance.

🔴 DIVERSIFY YOUR PORTFOLIO!
   Never invest all your money in a single stock. Spread risk across multiple
   investments.

🔴 UNDERSTAND YOUR RISK TOLERANCE!
   Only invest money you can afford to lose. Different stocks have different
   risk levels.

════════════════════════════════════════════════════════════════════════════

🎓 LEARNING RESOURCES
════════════════════════════════════════════════════════════════════════════

To understand how this project works:

1. Read PROJECT_SUMMARY.md for architecture overview
2. Read CHATBOT_GUIDE.md for detailed chatbot usage
3. Run scripts/run_demo.py to see the full pipeline
4. Explore the source code in src/ directory
5. Try the chatbot and experiment with queries

════════════════════════════════════════════════════════════════════════════

❓ TROUBLESHOOTING
════════════════════════════════════════════════════════════════════════════

Issue: "No module named 'src'"
  → Make sure you're running from project root directory
  → Run: cd /Users/chintanshah/Documents/llm_rag_finance

Issue: "ModuleNotFoundError: No module named 'dotenv'"
  → Activate virtual environment first
  → Run: source .venv/bin/activate
  → Then: pip install -r requirements.txt

Issue: "API Error 403: Forbidden"
  → Your FMP API key has limitations (free tier restrictions)
  → System will use sample data automatically
  → This is expected and normal

Issue: "Could not fetch from NewsAPI"
  → Your NewsAPI key might be invalid
  → Check .env file and verify your key

════════════════════════════════════════════════════════════════════════════

📞 NEED HELP?
════════════════════════════════════════════════════════════════════════════

Inside the chatbot, type:
  • help    → Show help menu with examples
  • report  → Show detailed analysis report
  • history → View past conversations

════════════════════════════════════════════════════════════════════════════

✅ YOU'RE ALL SET!
════════════════════════════════════════════════════════════════════════════

Ready to start? Run this command:

  python /Users/chintanshah/Documents/llm_rag_finance/scripts/chatbot.py

Happy investing! 🚀📈

════════════════════════════════════════════════════════════════════════════
"""
    
    print(info)

if __name__ == "__main__":
    print_project_info()
