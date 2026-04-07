#!/bin/bash
# Financial Advisor Streamlit App Launcher

echo "╔════════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                            ║"
echo "║          🎉 Launching AI Financial Advisor Streamlit Application 🎉       ║"
echo "║                                                                            ║"
echo "╚════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Get the directory where this script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the project directory
cd "$DIR"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "✅ Activating virtual environment..."
    source .venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Please run setup first."
    exit 1
fi

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit is not installed. Installing now..."
    pip install streamlit plotly -q
fi

echo ""
echo "📊 Starting Streamlit application..."
echo "🌐 Your app will open at: http://localhost:8501"
echo ""
echo "💡 Tips:"
echo "   • Press Ctrl+C to stop the server"
echo "   • Press 'r' to rerun the app"
echo "   • Press 'c' to clear the console"
echo ""
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

# Start Streamlit app
streamlit run app.py --logger.level=error --client.showErrorDetails=false
