#!/usr/bin/env python3
"""
Financial Advisor Chatbot - Interactive CLI
A conversational AI that helps users make informed investment decisions.
"""

import sys
import os
from datetime import datetime
import re

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.financial_advisor import FinancialAdvisor
from src.stock_recommender import StockRecommender


class FinancialAdvisorChatbot:
    """Interactive chatbot for financial advice."""
    
    def __init__(self):
        """Initialize the chatbot."""
        self.advisor = FinancialAdvisor()
        self.recommender = StockRecommender()
        self.conversation_history = []
        self.current_analysis = None
        
    def print_welcome(self):
        """Print welcome message."""
        print("\n")
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 78 + "║")
        print("║" + "  🤖 FINANCIAL ADVISOR CHATBOT - AI INVESTMENT RECOMMENDATION ENGINE".center(78) + "║")
        print("║" + " " * 78 + "║")
        print("╚" + "═" * 78 + "╝")
        print()
        print("Welcome to your AI Financial Advisor! I can help you make informed")
        print("investment decisions by analyzing stocks, financial data, and market trends.")
        print()
        print("💡 USAGE EXAMPLES:")
        print("   • 'Should I invest $10,000 in Apple?'")
        print("   • 'I have $5000, is Tesla a good investment?'")
        print("   • 'Analyze Microsoft with my $20000'")
        print("   • 'What about investing in Google with $15000?'")
        print("   • 'Suggest best stocks to invest $5000'")
        print("   • 'Which stocks should I buy with $10000?'")
        print()
        print("📋 COMMANDS:")
        print("   • 'report'    - Show the latest analysis report")
        print("   • 'history'   - Show conversation history")
        print("   • 'clear'     - Clear conversation history")
        print("   • 'help'      - Show help message")
        print("   • 'exit'      - Exit the chatbot")
        print()
        print("⚠️  DISCLAIMER: This is AI-generated analysis, not financial advice.")
        print("   Always consult with a qualified financial advisor before investing.")
        print()
        print("─" * 80)
        print()
    
    def print_help(self):
        """Print help message."""
        print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                         CHATBOT HELP & USAGE                              ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 HOW TO USE:
──────────────
Simply ask questions about whether you should invest in a particular stock.
The chatbot will analyze the company, fetch recent data, and provide a 
comprehensive investment recommendation.

📝 NATURAL LANGUAGE EXAMPLES:
─────────────────────────────
1. "Should I invest $10000 in Apple?"
2. "I have 5k, is Tesla worth investing in?"
3. "Can I invest $20000 in Microsoft and make good returns?"
4. "Is Google a good investment with my $15000?"
5. "Should I put $8000 into Amazon?"

🔍 WHAT THE ADVISOR ANALYZES:
──────────────────────────────
✓ Current stock price and valuation metrics (P/E ratio, market cap, etc.)
✓ Financial health (EPS, dividend yield)
✓ Recent news and market sentiment
✓ Risk assessment based on company fundamentals
✓ Stock price trends (50-day and 200-day averages)
✓ Number of shares you could potentially buy

📊 RECOMMENDATION LEVELS:
─────────────────────────
🟢 STRONG BUY    - Excellent investment opportunity
🟢 BUY           - Good investment opportunity
🟡 HOLD          - Neutral, wait for better conditions
🔴 SELL          - Consider alternatives
🔴 STRONG SELL   - Avoid this investment

⚙️ AVAILABLE COMMANDS:
──────────────────────
• report    - Display the most recent analysis report
• history   - View your conversation history
• clear     - Clear all conversation history
• help      - Show this help message
• exit      - Exit the chatbot

⚠️  IMPORTANT:
───────────────
• This advisor provides AI-generated analysis, NOT actual financial advice
• Do NOT make investment decisions based solely on this recommendation
• Always perform your own research and consult with professionals
• Past performance does not guarantee future results
• Diversify your portfolio and manage risk appropriately

        """)
    
    def parse_user_input(self, user_input: str) -> tuple:
        """
        Parse user input to extract ticker and investment amount.
        
        Returns:
            Tuple of (command_type, data, original_query)
        """
        user_input_lower = user_input.lower()
        
        # Check for commands
        if user_input_lower.strip() in ['exit', 'quit', 'q']:
            return ('exit', None, user_input)
        if user_input_lower.strip() in ['help', 'h']:
            return ('help', None, user_input)
        if user_input_lower.strip() in ['report', 'r']:
            return ('report', None, user_input)
        if user_input_lower.strip() in ['history', 'h']:
            return ('history', None, user_input)
        if user_input_lower.strip() in ['clear', 'c']:
            return ('clear', None, user_input)
        
        # Check for recommendation queries
        recommendation_patterns = [
            r'(suggest|recommend|best stocks?|top stocks?)\s+.*?\$?([\d,]+(?:\.\d{2})?)',
            r'which\s+(stocks?|investment).*?\$?([\d,]+(?:\.\d{2})?)',
            r'what.*?stocks?.*?invest\s+\$?([\d,]+(?:\.\d{2})?)',
        ]
        
        for pattern in recommendation_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                groups = match.groups()
                if len(groups) >= 1:
                    try:
                        # Extract amount from last group
                        amount = float(groups[-1].replace(',', ''))
                        if amount > 0:
                            return ('recommend', amount, user_input)
                    except:
                        continue
        
        # Pattern matching for investment queries
        # Patterns: "invest $X in TICKER", "I have $X, invest in TICKER", etc.
        patterns = [
            r'invest\s+\$?([\d,]+(?:\.\d{2})?)\s+in\s+([A-Za-z]+)',
            r'i\s+have\s+\$?([\d,]+(?:\.\d{2})?)\s+[,\s]+.*?([A-Za-z]+)',
            r'\$?([\d,]+(?:\.\d{2})?)\s+.*?invest\s+in\s+([A-Za-z]+)',
            r'([A-Za-z]+)\s+.*?\$?([\d,]+(?:\.\d{2})?)',
            r'([A-Za-z]+)\s+.*?invest.*?\$?([\d,]+(?:\.\d{2})?)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                groups = match.groups()
                # Handle different group arrangements
                if len(groups) == 2:
                    # Try to identify which is ticker and which is amount
                    group1, group2 = groups
                    
                    # Check if group1 looks like a number
                    try:
                        amount = float(group1.replace(',', ''))
                        ticker = group2
                    except:
                        # Otherwise assume group2 is amount
                        try:
                            amount = float(group2.replace(',', ''))
                            ticker = group1
                        except:
                            continue
                    
                    # Validate
                    if ticker.isalpha() and 1 <= len(ticker) <= 5 and amount > 0:
                        return ('invest', (ticker.upper(), amount), user_input)
        
        return (None, None, user_input)
    
    def process_investment_query(self, ticker: str, amount: float):
        """Process investment query."""
        print()
        analysis = self.advisor.analyze_investment_opportunity(ticker, amount)
        
        if "error" in analysis:
            print(f"\n❌ Error: {analysis['error']}")
            return
        
        # Print the recommendation
        print(analysis.get("recommendation", ""))
        
        # Store in history
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'query': f"Should I invest ${amount:,.2f} in {ticker}?",
            'recommendation': analysis.get('recommendation', ''),
            'ticker': ticker,
            'amount': amount
        })
        
        print("\n✅ Analysis complete! Type 'report' to see full details.")
    
    def process_recommendation_query(self, amount: float):
        """Process recommendation query for best stocks."""
        print()
        print(f"🎯 Generating stock recommendations for ${amount:,.2f}...")
        
        try:
            recommendations = self.recommender.get_stock_recommendations(
                amount, 
                num_recommendations=5
            )
            
            # Print summary
            print(recommendations['summary'])
            
            # Store in history
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'query': f"Suggest best stocks to invest ${amount:,.2f}",
                'type': 'recommendation',
                'recommendations': [r['ticker'] for r in recommendations['top_recommendations']],
                'amount': amount
            })
            
            print("✅ Recommendations generated! Type 'report' to see full details.")
            
        except Exception as e:
            print(f"\n❌ Error generating recommendations: {e}")
            print("   Please try again or ask about a specific stock.")

    
    def show_history(self):
        """Show conversation history."""
        if not self.conversation_history:
            print("\n📭 No conversation history yet. Ask me about an investment!")
            return
        
        print("\n" + "╔" + "═" * 78 + "╗")
        print("║" + "CONVERSATION HISTORY".center(78) + "║")
        print("╚" + "═" * 78 + "╝\n")
        
        for i, entry in enumerate(self.conversation_history, 1):
            timestamp = entry['timestamp']
            query = entry['query']
            ticker = entry['ticker']
            amount = entry['amount']
            
            print(f"{i}. [{timestamp}]")
            print(f"   Query: {query}")
            print(f"   Ticker: {ticker} | Amount: ${amount:,.2f}")
            print()
    
    def run(self):
        """Run the chatbot in interactive mode."""
        self.print_welcome()
        
        while True:
            try:
                print()
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                command, data, original = self.parse_user_input(user_input)
                
                if command == 'exit':
                    print("\n👋 Thank you for using Financial Advisor Chatbot!")
                    print("   Remember: Invest wisely and diversify your portfolio!\n")
                    break
                
                elif command == 'help':
                    self.print_help()
                
                elif command == 'report':
                    if self.advisor.analysis_data:
                        print("\n" + self.advisor.get_recommendation_report())
                    else:
                        print("\n📭 No analysis report available yet.")
                
                elif command == 'history':
                    self.show_history()
                
                elif command == 'clear':
                    self.conversation_history = []
                    print("\n🗑️  Conversation history cleared.")
                
                elif command == 'invest':
                    ticker, amount = data
                    print(f"\nAssistant: Analyzing {ticker} for an investment of ${amount:,.2f}...")
                    self.process_investment_query(ticker, amount)
                
                elif command == 'recommend':
                    amount = data
                    print(f"\nAssistant: Finding the best stocks for ${amount:,.2f}...")
                    self.process_recommendation_query(amount)
                
                elif command is None:
                    print("\nAssistant: I didn't understand that. You can ask me to:")
                    print("  • Analyze a specific stock: 'Should I invest $10000 in Apple?'")
                    print("  • Get recommendations: 'Suggest best stocks for $5000'")
                    print("  Type 'help' for more examples.")
                
            except KeyboardInterrupt:
                print("\n\n👋 Chatbot interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("   Please try again or type 'help' for assistance.")


def main():
    """Main entry point."""
    chatbot = FinancialAdvisorChatbot()
    chatbot.run()


if __name__ == "__main__":
    main()
