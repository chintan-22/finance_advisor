#!/bin/bash

# Financial Advisor Chatbot Launcher
# This script activates the virtual environment and launches the chatbot

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR"

echo "🚀 Starting Financial Advisor Chatbot..."
echo ""

# Check if virtual environment exists
if [ ! -d "$PROJECT_ROOT/.venv" ]; then
    echo "❌ Virtual environment not found at $PROJECT_ROOT/.venv"
    echo ""
    echo "Please set up the virtual environment first:"
    echo ""
    echo "  cd $PROJECT_ROOT"
    echo "  python -m venv .venv"
    echo "  source .venv/bin/activate"
    echo "  pip install -r requirements.txt"
    echo ""
    exit 1
fi

# Activate virtual environment and run chatbot
source "$PROJECT_ROOT/.venv/bin/activate"
python "$PROJECT_ROOT/scripts/chatbot.py"
