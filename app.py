#!/usr/bin/env python3
"""
Financial Advisor Chatbot - Streamlit Web App
A beautiful, interactive AI-powered investment recommendation platform.
"""

import sys
import os
import json
from datetime import datetime
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import yfinance as yf

from src.financial_advisor import FinancialAdvisor
from src.stock_recommender import StockRecommender

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="💰 AI Financial Advisor",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/chintan-22/llm_rag_finance',
        'Report a bug': "https://github.com/chintan-22/llm_rag_finance/issues",
    }
)

# Custom CSS for better UI
st.markdown("""
    <style>
        /* Main container styling */
        .main {
            padding: 0rem 1rem;
        }
        
        /* Metric cards */
        [data-testid="metric-container"] {
            background-color: #f0f2f6;
            padding: 10px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Chat message styling */
        .chat-message {
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            display: flex;
            gap: 1rem;
        }
        
        .chat-message.user {
            background-color: #e3f2fd;
            border-left: 4px solid #2196F3;
        }
        
        .chat-message.assistant {
            background-color: #f3e5f5;
            border-left: 4px solid #9c27b0;
        }
        
        /* Button styling */
        .stButton > button {
            width: 100%;
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background: linear-gradient(90deg, #764ba2 0%, #667eea 100%);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        
        /* Header styling */
        h1 {
            color: #667eea;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        
        h2 {
            color: #764ba2;
            border-bottom: 2px solid #667eea;
            padding-bottom: 0.5rem;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        }
        
        [data-testid="stSidebar"] .stRadio > label {
            color: white;
        }
        
        [data-testid="stSidebar"] .stSelectbox > label {
            color: white;
        }
        
        /* Info box */
        .info-box {
            background-color: #e8f5e9;
            border-left: 4px solid #4caf50;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        .warning-box {
            background-color: #fff3e0;
            border-left: 4px solid #ff9800;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        
        .error-box {
            background-color: #ffebee;
            border-left: 4px solid #f44336;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'advisor' not in st.session_state:
    st.session_state.advisor = FinancialAdvisor()

if 'recommender' not in st.session_state:
    st.session_state.recommender = StockRecommender()

if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

if 'current_analysis' not in st.session_state:
    st.session_state.current_analysis = None

if 'show_detailed_analysis' not in st.session_state:
    st.session_state.show_detailed_analysis = False

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_stock_chart(ticker: str, period: str = "1y"):
    """Create interactive stock price chart."""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        
        if hist.empty:
            st.warning(f"Could not fetch historical data for {ticker}")
            return None
        
        hist_reset = hist.reset_index()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=hist_reset['Date'],
            y=hist_reset['Close'],
            mode='lines',
            name='Close Price',
            line=dict(color='#667eea', width=2),
            hovertemplate='<b>Date:</b> %{x|%Y-%m-%d}<br><b>Close Price:</b> $%{y:.2f}<extra></extra>'
        ))
        
        # Add 50-day moving average
        hist_reset['MA50'] = hist_reset['Close'].rolling(window=50).mean()
        fig.add_trace(go.Scatter(
            x=hist_reset['Date'],
            y=hist_reset['MA50'],
            mode='lines',
            name='50-Day MA',
            line=dict(color='#ff9800', width=1, dash='dash'),
            hovertemplate='<b>50-Day MA:</b> $%{y:.2f}<extra></extra>'
        ))
        
        # Add 200-day moving average
        hist_reset['MA200'] = hist_reset['Close'].rolling(window=200).mean()
        fig.add_trace(go.Scatter(
            x=hist_reset['Date'],
            y=hist_reset['MA200'],
            mode='lines',
            name='200-Day MA',
            line=dict(color='#f44336', width=1, dash='dash'),
            hovertemplate='<b>200-Day MA:</b> $%{y:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=f'{ticker} - Historical Stock Price',
            xaxis_title='Date',
            yaxis_title='Price (USD)',
            hovermode='x unified',
            plot_bgcolor='rgba(240, 242, 246, 0.5)',
            paper_bgcolor='white',
            height=400,
            font=dict(family='Arial', size=12),
        )
        
        return fig
    except Exception as e:
        st.error(f"Error creating chart: {str(e)[:100]}")
        return None


def display_financial_metrics(data: dict):
    """Display financial metrics in a nice format."""
    metrics = data.get('financial_metrics', {})
    
    if not metrics:
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💵 Current Price",
            f"${metrics.get('current_price', 0):.2f}",
            delta=None,
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            "📊 P/E Ratio",
            f"{metrics.get('pe_ratio', 0):.2f}x",
            delta=None
        )
    
    with col3:
        st.metric(
            "💰 Dividend Yield",
            f"{metrics.get('dividend_yield', 0)*100:.2f}%",
            delta=None
        )
    
    with col4:
        st.metric(
            "🏢 Market Cap",
            f"${metrics.get('market_cap', 0) / 1e12:.2f}T" if metrics.get('market_cap', 0) > 1e12 else f"${metrics.get('market_cap', 0) / 1e9:.2f}B",
            delta=None
        )


def display_recommendation_card(recommendation: dict):
    """Display recommendation in a nice card format."""
    ticker = recommendation.get('ticker', 'N/A')
    amount = recommendation.get('investment_amount', 0)
    sentiment = recommendation.get('sentiment', 'NEUTRAL')
    risk = recommendation.get('risk_assessment', 'MEDIUM')
    
    # Determine colors based on sentiment
    sentiment_colors = {
        'VERY POSITIVE': '#4caf50',
        'POSITIVE': '#8bc34a',
        'NEUTRAL': '#ff9800',
        'NEGATIVE': '#ff5722',
        'VERY NEGATIVE': '#f44336'
    }
    
    risk_colors = {
        'VERY LOW': '#4caf50',
        'LOW': '#8bc34a',
        'MEDIUM': '#ff9800',
        'HIGH': '#ff5722',
        'VERY HIGH': '#f44336'
    }
    
    sentiment_color = sentiment_colors.get(sentiment, '#ff9800')
    risk_color = risk_colors.get(risk, '#ff9800')
    
    # Create HTML for card
    card_html = f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    ">
        <h2 style="color: white; border: none; margin-top: 0;">🎯 {ticker}</h2>
        <p style="font-size: 1.1rem; margin: 0.5rem 0;">
            <b>Investment Amount:</b> ${amount:,.2f}
        </p>
        <div style="display: flex; gap: 2rem; margin-top: 1rem;">
            <div>
                <span style="
                    background-color: {sentiment_color};
                    padding: 0.5rem 1rem;
                    border-radius: 5px;
                    font-weight: bold;
                    display: inline-block;
                ">
                    Sentiment: {sentiment}
                </span>
            </div>
            <div>
                <span style="
                    background-color: {risk_color};
                    padding: 0.5rem 1rem;
                    border-radius: 5px;
                    font-weight: bold;
                    display: inline-block;
                ">
                    Risk: {risk}
                </span>
            </div>
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)


def format_recommendation_text(recommendation: dict) -> str:
    """Format recommendation as readable text."""
    ticker = recommendation.get('ticker', 'N/A')
    amount = recommendation.get('investment_amount', 0)
    sentiment = recommendation.get('sentiment', 'NEUTRAL')
    risk = recommendation.get('risk_assessment', 'MEDIUM')
    metrics = recommendation.get('financial_metrics', {})
    
    text = f"""
### 📈 Investment Analysis for {ticker}

**Investment Amount:** ${amount:,.2f}

**Market Sentiment:** {sentiment} 📊
**Risk Assessment:** {risk} ⚠️

**Key Financial Metrics:**
- Current Price: ${metrics.get('current_price', 0):.2f}
- P/E Ratio: {metrics.get('pe_ratio', 0):.2f}x
- Dividend Yield: {metrics.get('dividend_yield', 0)*100:.2f}%
- Market Cap: ${metrics.get('market_cap', 0) / 1e12:.2f}T

**Analysis Details:**
"""
    
    if 'detailed_analysis' in recommendation:
        text += recommendation['detailed_analysis']
    
    return text


# ============================================================================
# MAIN APP LAYOUT
# ============================================================================

# Header
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center;">
        <h1 style="font-size: 3rem; margin-bottom: 0.5rem;">💎 AI Financial Advisor</h1>
        <p style="font-size: 1.2rem; color: #764ba2; margin: 0;">Intelligent Investment Recommendations Powered by AI</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Navigation")
    page = st.radio(
        "Choose a mode:",
        ["🔍 Stock Analysis", "📊 Stock Recommendations", "📋 History"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    st.markdown("""
    ### 📚 How to Use
    
    **Stock Analysis:**
    - Enter a stock ticker and investment amount
    - Get detailed AI-powered analysis
    - See live financial data and charts
    
    **Stock Recommendations:**
    - Enter your investment budget
    - Get top 5 recommended stocks
    - Based on comprehensive scoring system
    
    ### ⚠️ Disclaimer
    
    This is AI-generated analysis, **NOT** financial advice. Always consult with a qualified financial advisor before investing.
    
    ### 🔗 Links
    - [GitHub Repository](https://github.com/chintan-22/llm_rag_finance)
    - [Documentation](https://github.com/chintan-22/llm_rag_finance#readme)
    """)

# ============================================================================
# PAGE: STOCK ANALYSIS
# ============================================================================

if page == "🔍 Stock Analysis":
    st.markdown("## 🔍 Stock Analysis & Investment Recommendation")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        ticker = st.text_input(
            "Stock Ticker Symbol",
            value="AAPL",
            placeholder="Enter ticker (e.g., AAPL, MSFT, GOOGL)",
            help="Enter the stock ticker symbol you want to analyze"
        ).upper()
    
    with col2:
        investment_amount = st.number_input(
            "Investment Amount ($)",
            value=5000.0,
            min_value=100.0,
            step=100.0,
            help="How much do you want to invest?"
        )
    
    analyze_button = st.button(
        "🚀 Analyze Stock",
        use_container_width=True,
        type="primary",
        help="Click to get AI-powered investment recommendation"
    )
    
    if analyze_button:
        if ticker:
            with st.spinner(f"🔄 Analyzing {ticker}... This may take a moment"):
                try:
                    # Get analysis
                    analysis = st.session_state.advisor.analyze_investment_opportunity(
                        ticker, 
                        investment_amount
                    )
                    
                    if "error" not in analysis:
                        st.session_state.current_analysis = analysis
                        
                        # Display recommendation card
                        display_recommendation_card(analysis)
                        
                        # Display financial metrics
                        st.markdown("### 📊 Key Financial Metrics")
                        display_financial_metrics(analysis)
                        
                        # Create tabs for different views
                        tab1, tab2, tab3 = st.tabs(["📈 Price Chart", "📋 Detailed Analysis", "💾 Export"])
                        
                        with tab1:
                            st.subheader(f"{ticker} - 1 Year Price History")
                            chart = create_stock_chart(ticker, period="1y")
                            if chart:
                                st.plotly_chart(chart, use_container_width=True)
                        
                        with tab2:
                            st.subheader("Detailed Analysis")
                            st.markdown(format_recommendation_text(analysis))
                        
                        with tab3:
                            st.subheader("Export Analysis")
                            # Create JSON export
                            export_data = {
                                "timestamp": datetime.now().isoformat(),
                                "ticker": ticker,
                                "investment_amount": investment_amount,
                                "analysis": analysis
                            }
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.download_button(
                                    "📥 Download as JSON",
                                    json.dumps(export_data, indent=2),
                                    f"{ticker}_analysis.json",
                                    "application/json"
                                )
                            
                            with col2:
                                csv_data = pd.DataFrame([{
                                    "Ticker": ticker,
                                    "Investment Amount": investment_amount,
                                    "Current Price": analysis.get('financial_metrics', {}).get('current_price', 0),
                                    "P/E Ratio": analysis.get('financial_metrics', {}).get('pe_ratio', 0),
                                    "Sentiment": analysis.get('sentiment', ''),
                                    "Risk Level": analysis.get('risk_assessment', ''),
                                }])
                                st.download_button(
                                    "📥 Download as CSV",
                                    csv_data.to_csv(index=False),
                                    f"{ticker}_analysis.csv",
                                    "text/csv"
                                )
                        
                        # Add to history
                        st.session_state.conversation_history.append({
                            'timestamp': datetime.now().isoformat(),
                            'type': 'analysis',
                            'ticker': ticker,
                            'amount': investment_amount,
                            'analysis': analysis
                        })
                        
                        st.success(f"✅ Analysis complete for {ticker}!")
                    else:
                        st.error(f"❌ Error: {analysis.get('error', 'Unknown error')}")
                
                except Exception as e:
                    st.error(f"❌ Error analyzing {ticker}: {str(e)[:200]}")
        else:
            st.warning("⚠️ Please enter a stock ticker symbol")

# ============================================================================
# PAGE: STOCK RECOMMENDATIONS
# ============================================================================

elif page == "📊 Stock Recommendations":
    st.markdown("## 📊 Get Top Stock Recommendations")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        investment_budget = st.number_input(
            "Investment Budget ($)",
            value=5000.0,
            min_value=1000.0,
            step=500.0,
            help="Total amount you want to invest"
        )
    
    with col2:
        num_recommendations = st.slider(
            "Number of Recommendations",
            min_value=3,
            max_value=10,
            value=5,
            help="How many stock recommendations do you want?"
        )
    
    recommend_button = st.button(
        "💡 Get Recommendations",
        use_container_width=True,
        type="primary",
        help="Click to get AI-powered stock recommendations"
    )
    
    if recommend_button:
        with st.spinner(f"🔄 Generating recommendations for ${investment_budget:,.2f}..."):
            try:
                recommendations = st.session_state.recommender.get_stock_recommendations(
                    investment_budget,
                    num_recommendations
                )
                
                # Display summary
                st.markdown(recommendations.get('summary', ''))
                
                # Display detailed recommendations
                st.markdown("### 🏆 Top Recommended Stocks")
                
                for i, rec in enumerate(recommendations.get('top_recommendations', []), 1):
                    with st.expander(f"#{i} {rec.get('ticker', 'N/A')} - Score: {rec.get('score', 0):.1f}/100", expanded=(i==1)):
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("📊 Score", f"{rec.get('score', 0):.1f}/100")
                        with col2:
                            st.metric("💰 Recommendation", rec.get('recommendation', 'N/A'))
                        with col3:
                            st.metric("⚠️ Risk", rec.get('risk_level', 'N/A'))
                        with col4:
                            st.metric("📈 Sentiment", rec.get('sentiment', 'N/A'))
                        
                        # Display breakdown
                        if 'score_breakdown' in rec:
                            st.markdown("**Score Breakdown:**")
                            breakdown = rec['score_breakdown']
                            
                            fig = go.Figure(data=[
                                go.Bar(
                                    x=list(breakdown.keys()),
                                    y=list(breakdown.values()),
                                    marker_color=['#667eea', '#764ba2', '#ff9800', '#f44336'][:len(breakdown)]
                                )
                            ])
                            fig.update_layout(
                                height=300,
                                showlegend=False,
                                plot_bgcolor='rgba(240, 242, 246, 0.5)',
                            )
                            st.plotly_chart(fig, use_container_width=True)
                
                # Add to history
                st.session_state.conversation_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'type': 'recommendation',
                    'budget': investment_budget,
                    'recommendations': recommendations
                })
                
                st.success("✅ Recommendations generated successfully!")
                
            except Exception as e:
                st.error(f"❌ Error generating recommendations: {str(e)[:200]}")

# ============================================================================
# PAGE: CONVERSATION HISTORY
# ============================================================================

elif page == "📋 History":
    st.markdown("## 📋 Analysis History")
    
    if st.session_state.conversation_history:
        col1, col2 = st.columns([4, 1])
        with col2:
            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state.conversation_history = []
                st.rerun()
        
        for i, entry in enumerate(reversed(st.session_state.conversation_history), 1):
            timestamp = entry.get('timestamp', '')
            entry_type = entry.get('type', 'unknown')
            
            if entry_type == 'analysis':
                ticker = entry.get('ticker', 'N/A')
                amount = entry.get('amount', 0)
                
                with st.expander(f"📊 {ticker} Analysis - ${amount:,.2f} - {timestamp[:10]}"):
                    analysis = entry.get('analysis', {})
                    st.markdown(format_recommendation_text(analysis))
            
            elif entry_type == 'recommendation':
                budget = entry.get('budget', 0)
                
                with st.expander(f"💡 Recommendations for ${budget:,.2f} - {timestamp[:10]}"):
                    recs = entry.get('recommendations', {})
                    st.markdown(recs.get('summary', ''))
    else:
        st.info("📭 No analysis history yet. Start by analyzing a stock or getting recommendations!")

# ============================================================================
# FOOTER
# ============================================================================

st.divider()

footer = """
<div style="text-align: center; padding: 2rem; color: #666; font-size: 0.9rem;">
    <p>
        💎 <b>AI Financial Advisor</b> - Powered by Advanced LLMs and Real-time Market Data<br>
        ⚠️ <b>Disclaimer:</b> This is AI-generated analysis, NOT financial advice. Always consult professionals before investing.<br>
        🔒 Your privacy is important. No data is stored on our servers.
    </p>
</div>
"""

st.markdown(footer, unsafe_allow_html=True)
