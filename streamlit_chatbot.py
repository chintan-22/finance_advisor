#!/usr/bin/env python3
"""
Financial Advisor Chatbot - Streamlit Web App
Beautiful, intelligent investment advisor with proper conversation flow.
"""

import sys
import os
from datetime import datetime
import re

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd

from src.financial_advisor import FinancialAdvisor
from src.stock_recommender import StockRecommender
from src.data_fetch import fetch_stock_data

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="💬 AI Financial Advisor",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Beautiful Custom CSS
st.markdown("""
    <style>
        * {
            margin: 0;
            padding: 0;
        }
        
        .header-container {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
        }
        
        .header-container h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        
        .header-container p {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        .chat-container {
            background: white;
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
            min-height: 400px;
            max-height: 600px;
            overflow-y: auto;
        }
        
        .message-user {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.2rem;
            border-radius: 12px;
            margin: 0.8rem 0;
            margin-left: 2rem;
            text-align: right;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
        }
        
        .message-assistant {
            background: #f0f2f6;
            color: #333;
            padding: 1.2rem;
            border-radius: 12px;
            margin: 0.8rem 0;
            margin-right: 2rem;
            border-left: 4px solid #667eea;
        }
        
        .input-container {
            background: white;
            border-radius: 15px;
            padding: 2rem;
            margin-top: 1.5rem;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
        }
        
        .profile-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
        }
        
        .stButton > button {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white !important;
            border: none !important;
            border-radius: 8px;
            padding: 0.8rem 1.5rem !important;
            font-weight: bold;
            width: 100%;
            transition: transform 0.2s;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
        
        .ticker-badge {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 0.4rem 1rem;
            border-radius: 20px;
            display: inline-block;
            margin: 0.3rem 0.3rem;
            font-weight: bold;
            font-size: 0.95rem;
        }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# INITIALIZE SESSION STATE
# ============================================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_profile" not in st.session_state:
    st.session_state.user_profile = {
        "budget": None,
        "risk_tolerance": None,
        "investment_goals": None,
    }

if "advisor" not in st.session_state:
    st.session_state.advisor = FinancialAdvisor()

if "recommender" not in st.session_state:
    st.session_state.recommender = StockRecommender()

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def extract_budget(text):
    """Extract budget from text like '$450', '450', '$5k', '5k'"""
    pattern = r'\$?([\d,]+(?:\.\d{2})?)\s*(?:k)?(?:\s+to\s+invest)?'
    match = re.search(pattern, text, re.IGNORECASE)
    
    if match:
        try:
            amount_str = match.group(1).replace(',', '')
            budget = float(amount_str)
            if re.search(r'\d+\s*k\b', text, re.IGNORECASE):
                budget *= 1000
            return budget if budget > 0 else None
        except:
            return None
    return None

def extract_risk(text):
    """Extract risk tolerance: LOW, MEDIUM, or HIGH"""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['conservative', 'safe', 'low risk', 'cautious', 'stable']):
        return "LOW"
    elif any(word in text_lower for word in ['moderate', 'balanced', 'medium risk', 'medium']):
        return "MEDIUM"
    elif any(word in text_lower for word in ['aggressive', 'high risk', 'growth', 'risky', 'high']):
        return "HIGH"
    
    return None

def extract_ticker(text):
    """Extract stock tickers from text"""
    common_words = {'THE', 'AND', 'OR', 'FOR', 'WITH', 'HAVE', 'ABOUT', 'WHAT', 
                   'WHICH', 'WHO', 'WHEN', 'WHERE', 'WHY', 'HOW', 'IS', 'A', 'I', 'P', 'E', 'M'}
    
    words = re.findall(r'\b[A-Z][A-Z0-9]{1,4}\b', text.upper())
    return list(set([w for w in words if len(w) >= 2 and w not in common_words]))

def get_recommendations(budget, risk):
    """Get stock recommendations based on budget and risk"""
    try:
        recommendations = st.session_state.recommender.get_stock_recommendations(
            budget, num_recommendations=5, risk_tolerance=risk
        )
        return recommendations
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def handle_user_input(user_message):
    """Main handler: Process input and generate response"""
    # Extract information
    budget = extract_budget(user_message)
    risk = extract_risk(user_message)
    tickers = extract_ticker(user_message)
    
    # Update profile
    if budget:
        st.session_state.user_profile['budget'] = budget
    if risk:
        st.session_state.user_profile['risk_tolerance'] = risk
    
    text_lower = user_message.lower()
    
    # **KEY LOGIC**: Budget only? Ask for risk
    if budget and not risk:
        return f"✅ **Perfect!** You want to invest **${budget:,.0f}**\n\nNow, what's your risk tolerance?\n\n🟢 **Conservative** - Safe, stable stocks\n🟡 **Moderate** - Balanced growth\n🔴 **Aggressive** - High growth, high risk"
    
    # **KEY LOGIC**: Budget AND risk? Give recommendations immediately!
    elif budget and risk:
        recommendations = get_recommendations(budget, risk)
        if recommendations:
            summary = recommendations.get('summary', '')
            return f"🎯 **Top Stocks for ${budget:,.0f} ({risk} Risk)**\n\n{summary}"
        else:
            return f"❌ Error generating recommendations. Please try again."
    
    # Only risk? Ask for budget
    elif risk and not budget:
        return f"Great! You're **{risk} risk** investor.\n\nHow much do you want to invest? (e.g., $5000, $450, $10k)"
    
    elif 'recommend' in text_lower or 'suggest' in text_lower or 'best' in text_lower:
        return "I'd love to help! Tell me:\n1. **Budget**: How much to invest? (e.g., $5000)\n2. **Risk**: Conservative, moderate, or aggressive?"
    
    elif tickers:
        return f"You're interested in: {', '.join(tickers)}\n\nTo find matching stocks:\n- **How much** do you want to invest?\n- **Risk level**: Conservative, moderate, aggressive?"
    
    elif 'hello' in text_lower or 'hi' in text_lower or 'start' in text_lower:
        return "👋 **Welcome!** I'm your AI Financial Advisor.\n\nLet's find the best stocks for you!\n\nJust tell me:\n- **Budget**: e.g., \"I have $5000\"\n- **Risk**: e.g., \"I'm conservative\"\n\nI'll instantly show you the top stocks! 📈"
    
    else:
        return "Tell me your **budget** and **risk tolerance**, and I'll recommend the best stocks!\n\nExample: \"I have $5000 and I'm conservative\""

# ============================================================================
# MAIN UI
# ============================================================================

# Header
st.markdown("""
    <div class='header-container'>
        <h1>� AI Financial Advisor</h1>
        <p>Find the best stocks to invest in - Instantly</p>
    </div>
""", unsafe_allow_html=True)

# Main layout
col_chat, col_profile = st.columns([3, 1])

with col_profile:
    st.markdown("### 👤 Your Profile")
    if st.session_state.user_profile['budget']:
        st.success(f"💰 ${st.session_state.user_profile['budget']:,.0f}")
    else:
        st.info("Budget: Not set")
    
    if st.session_state.user_profile['risk_tolerance']:
        if st.session_state.user_profile['risk_tolerance'] == 'LOW':
            st.success(f"🟢 Conservative")
        elif st.session_state.user_profile['risk_tolerance'] == 'MEDIUM':
            st.warning(f"� Moderate")
        else:
            st.error(f"🔴 Aggressive")
    else:
        st.info("Risk: Not set")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.user_profile = {
            "budget": None,
            "risk_tolerance": None,
            "investment_goals": None,
        }
        st.rerun()

with col_chat:
    # Chat display
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    
    if st.session_state.messages:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"<div class='message-user'>{message['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='message-assistant'>{message['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='text-align: center; padding: 3rem; color: #999;'>
                <h3>👋 Hello! Let's find your best stocks</h3>
                <p style='font-size: 1.1rem;'>Try: "I have $450 to invest"</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Input area
st.markdown("<div class='input-container'>", unsafe_allow_html=True)

col_input, col_btn = st.columns([5, 1])

with col_input:
    user_input = st.text_input(
        "💬 Tell me your budget and risk tolerance",
        placeholder="e.g., I have $450 to invest, I'm conservative",
        label_visibility="collapsed"
    )

with col_btn:
    send_button = st.button("Send ➜", use_container_width=True, key="send_btn")

st.markdown("</div>", unsafe_allow_html=True)

# Process input
if send_button and user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    response = handle_user_input(user_input)
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
    
    st.rerun()

# Example buttons
if not st.session_state.messages:
    st.divider()
    st.markdown("### 💡 Quick Examples:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("I have $450", use_container_width=True, key="btn_450"):
            st.session_state.messages.append({
                "role": "user",
                "content": "I have $450 to invest"
            })
            st.session_state.messages.append({
                "role": "assistant",
                "content": handle_user_input("I have $450 to invest")
            })
            st.rerun()
    
    with col2:
        if st.button("I have $5000, conservative", use_container_width=True, key="btn_5k"):
            st.session_state.messages.append({
                "role": "user",
                "content": "I have $5000 and I'm conservative"
            })
            st.session_state.messages.append({
                "role": "assistant",
                "content": handle_user_input("I have $5000 and I'm conservative")
            })
            st.rerun()
    
    with col3:
        if st.button("I have $10k, aggressive", use_container_width=True, key="btn_10k"):
            st.session_state.messages.append({
                "role": "user",
                "content": "I have $10000 and I'm aggressive"
            })
            st.session_state.messages.append({
                "role": "assistant",
                "content": handle_user_input("I have $10000 and I'm aggressive")
            })
            st.rerun()

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #999; font-size: 0.9rem;'>
        ⚠️ <b>Disclaimer:</b> AI-generated analysis, not financial advice. 
        Consult qualified advisors before investing.
    </div>
""", unsafe_allow_html=True)
