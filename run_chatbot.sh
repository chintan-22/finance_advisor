#!/bin/bash
# Launch the Streamlit Chatbot

cd /Users/chintanshah/Documents/llm_rag_finance

echo "🚀 Starting Financial Advisor Chatbot..."
echo ""
echo "Opening in browser: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Use the virtual environment's Python
source .venv/bin/activate
python3 -m streamlit run streamlit_chatbot.py
