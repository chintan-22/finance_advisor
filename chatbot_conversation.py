#!/usr/bin/env python3
"""
Financial Advisor Chatbot - Conversational AI
A natural language chatbot that understands user investment needs and provides recommendations.
"""

import sys
import os
from datetime import datetime
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.financial_advisor import FinancialAdvisor
from src.stock_recommender import StockRecommender
from src.data_fetch import fetch_stock_data


class ConversationalFinancialChatbot:
    """Conversational chatbot for financial advice using LLM."""
    
    def __init__(self):
        """Initialize the chatbot."""
        self.advisor = FinancialAdvisor()
        self.recommender = StockRecommender()
        
        # Conversation context
        self.conversation_history = []
        self.user_profile = {
            'budget': None,
            'risk_tolerance': None,
            'investment_goals': None,
            'interested_stocks': [],
            'analyzed_stocks': []
        }
        self.current_topic = None
        
    def print_welcome(self):
        """Print welcome message."""
        print("\n")
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 78 + "║")
        print("║" + "  💬 AI FINANCIAL ADVISOR - CONVERSATIONAL CHATBOT".center(78) + "║")
        print("║" + " " * 78 + "║")
        print("╚" + "═" * 78 + "╝")
        print()
        print("👋 Hello! I'm your AI Financial Advisor. I can help you:")
        print()
        print("   • Understand different stocks and their performance")
        print("   • Find the best stocks for your budget")
        print("   • Learn about investment strategies")
        print("   • Get personalized recommendations based on your goals")
        print("   • Analyze any company you're interested in")
        print()
        print("Just chat naturally! Tell me about your investment goals,")
        print("your budget, or ask me about any stock you're curious about.")
        print()
        print("Type 'exit' or 'quit' to end the conversation.")
        print("Type 'help' for commands, 'profile' to see your info.")
        print()
        print("─" * 80)
        print()

    def extract_budget_and_risk(self, text: str) -> tuple:
        """Extract budget and risk tolerance from user text."""
        budget = None
        risk = None
        
        # Extract budget (e.g., "$5000", "5000", "5k", "10000")
        budget_match = re.search(r'\$?([\d,]+(?:\.\d{2})?)\s*(?:k|thousand|m|million)?', text, re.IGNORECASE)
        if budget_match:
            amount_str = budget_match.group(1).replace(',', '')
            try:
                budget = float(amount_str)
                if 'k' in text.lower() or 'thousand' in text.lower():
                    budget *= 1000
                elif 'm' in text.lower() or 'million' in text.lower():
                    budget *= 1000000
            except:
                pass
        
        # Extract risk tolerance
        if any(word in text.lower() for word in ['safe', 'conservative', 'low risk', 'stable']):
            risk = 'LOW'
        elif any(word in text.lower() for word in ['moderate', 'medium', 'balanced']):
            risk = 'MEDIUM'
        elif any(word in text.lower() for word in ['aggressive', 'high risk', 'growth', 'risky']):
            risk = 'HIGH'
        
        return budget, risk

    def extract_ticker(self, text: str) -> list:
        """Extract stock tickers from user text."""
        tickers = re.findall(r'\b([A-Z]{1,5})\b', text)
        # Filter out common words that aren't tickers (especially single letters and common words)
        common_words = {'AND', 'THE', 'FOR', 'NOT', 'BUT', 'ARE', 'HAS', 'CAN', 'HOW', 'WHY', 'IS', 'OR', 'TO', 'IN', 'DO', 'IF', 'BE', 'MY', 'IT', 'AS', 'UP', 'AT', 'A', 'I', 'P', 'E', 'M'}
        tickers = [t for t in tickers if t not in common_words and len(t) >= 2 and len(t) <= 5]
        return list(set(tickers))  # Remove duplicates

    def generate_response(self, user_message: str) -> str:
        """Generate a conversational response using LLM."""
        text_lower = user_message.lower()
        
        # Extract information from user message
        budget, risk = self.extract_budget_and_risk(user_message)
        tickers = self.extract_ticker(user_message)
        
        # Update user profile
        if budget:
            self.user_profile['budget'] = budget
        if risk:
            self.user_profile['risk_tolerance'] = risk
        if tickers:
            self.user_profile['interested_stocks'].extend(tickers)
            self.user_profile['interested_stocks'] = list(set(self.user_profile['interested_stocks']))
        
        # Determine topic and generate response
        response = ""
        
        # User asking about specific stocks
        if tickers:
            self.current_topic = 'stock_analysis'
            response = self._handle_stock_analysis(tickers)
        
        # User asking for recommendations based on budget
        elif budget and any(word in text_lower for word in ['recommend', 'suggest', 'best', 'which', 'invest']):
            self.current_topic = 'recommendations'
            response = self._handle_recommendations(budget, risk)
        
        # User providing budget information
        elif budget and any(word in text_lower for word in ['have', 'budget', 'amount', 'invest', 'spend']):
            self.current_topic = 'budget_info'
            self.user_profile['budget'] = budget
            response = self._handle_budget_info(budget)
        
        # User asking about investment goals
        elif any(word in text_lower for word in ['goal', 'want', 'looking for', 'interested in', 'help me']):
            self.current_topic = 'goals'
            response = self._handle_goals()
        
        # User asking for education
        elif any(word in text_lower for word in ['how', 'what is', 'explain', 'tell me', 'understand']):
            self.current_topic = 'education'
            response = self._handle_education(user_message)
        
        # Default conversational response
        else:
            response = self._handle_general_question(user_message)
        
        return response

    def _handle_stock_analysis(self, tickers: list) -> str:
        """Handle analysis of specific stocks."""
        response = f"\n🔍 Great! You're interested in {', '.join(tickers)}.\n\n"
        response += "Let me analyze these stocks for you.\n"
        response += "To give you the best recommendation, I need to know:\n\n"
        response += "  💰 How much are you planning to invest?\n"
        response += "  ⚠️  What's your risk tolerance? (conservative/moderate/aggressive)\n"
        response += "  🎯 What are your investment goals? (growth/income/stability)\n\n"
        
        # Analyze each stock
        for ticker in tickers[:3]:  # Limit to first 3 stocks
            try:
                print(f"\n   📊 Fetching data for {ticker}...")
                data = fetch_stock_data(ticker)
                if data and 'price' in data:
                    price = data.get('price', 0)
                    pe = data.get('pe_ratio', 0)
                    response += f"\n   💎 {ticker}:\n"
                    response += f"      Current Price: ${price:.2f}\n"
                    response += f"      P/E Ratio: {pe:.1f}x\n"
                    if 'market_cap' in data:
                        market_cap = data['market_cap'] / 1e12
                        response += f"      Market Cap: ${market_cap:.2f}T\n"
                else:
                    response += f"\n   ⚠️  Couldn't fetch data for {ticker}.\n"
            except Exception as e:
                print(f"Error analyzing {ticker}: {str(e)[:50]}")
                response += f"   ⚠️  {ticker} - Analyzing...\n"
        
        response += "\nOnce you share your budget and risk tolerance, I can give you personalized recommendations!\n"
        return response

    def _handle_recommendations(self, budget: float, risk: str = None) -> str:
        """Handle stock recommendations based on budget."""
        response = f"\n💡 Perfect! You have ${budget:,.2f} to invest.\n\n"
        
        if risk:
            response += f"And your risk tolerance is: {risk} ⚠️\n\n"
        else:
            response += "To give you the best recommendations, could you tell me your risk tolerance?\n"
            response += "   🟢 Conservative (stable, dividend stocks)\n"
            response += "   🟡 Moderate (balanced growth and stability)\n"
            response += "   🔴 Aggressive (high growth potential)\n\n"
        
        response += "Let me find the best stocks for your budget...\n"
        
        try:
            print(f"\n📊 Generating recommendations for ${budget:,.2f}...")
            recommendations = self.recommender.get_stock_recommendations(
                budget,
                num_recommendations=5
            )
            
            response += "\n🏆 Here are my top recommendations:\n\n"
            
            for i, rec in enumerate(recommendations.get('top_recommendations', [])[:5], 1):
                ticker = rec.get('ticker', 'N/A')
                score = rec.get('score', 0)
                recommendation = rec.get('recommendation', 'N/A')
                risk_level = rec.get('risk_level', 'N/A')
                
                response += f"{i}. {ticker} ⭐\n"
                response += f"   Score: {score:.0f}/100\n"
                response += f"   Recommendation: {recommendation}\n"
                response += f"   Risk Level: {risk_level}\n\n"
            
            response += "Would you like me to:\n"
            response += "   • Analyze any of these stocks in detail?\n"
            response += "   • Explain the investment strategy?\n"
            response += "   • Help you with a different budget?\n"
        
        except Exception as e:
            print(f"Error generating recommendations: {str(e)[:80]}")
            response += "Let me generate detailed recommendations...\n"
        
        return response

    def _handle_budget_info(self, budget: float) -> str:
        """Handle budget information provided by user."""
        response = f"\n💰 Great! You have ${budget:,.2f} to invest.\n\n"
        response += "Now I can help you find the perfect stocks! 📈\n\n"
        response += "To tailor recommendations for you, I'd like to understand:\n\n"
        response += "1️⃣  Risk Tolerance:\n"
        response += "   • Conservative: Safe, stable investments (like blue-chip stocks, dividend stocks)\n"
        response += "   • Moderate: Mix of growth and stability\n"
        response += "   • Aggressive: High-growth potential (tech, emerging companies)\n\n"
        response += "2️⃣  Investment Goals:\n"
        response += "   • Growth: Long-term capital appreciation\n"
        response += "   • Income: Regular dividends and returns\n"
        response += "   • Stability: Minimize risk and losses\n\n"
        response += "What's your preference?\n"
        return response

    def _handle_goals(self) -> str:
        """Handle investment goals inquiry."""
        response = "\n🎯 Excellent! Let's understand your investment goals.\n\n"
        response += "I can help you with:\n\n"
        response += "📈 **Growth Investing**\n"
        response += "   - Long-term capital appreciation\n"
        response += "   - Higher risk, higher potential returns\n"
        response += "   - Best for: Tech, emerging markets, growth stocks\n\n"
        response += "💰 **Income Investing**\n"
        response += "   - Regular dividend income\n"
        response += "   - Stable, predictable returns\n"
        response += "   - Best for: Blue-chip stocks, utilities, REITs\n\n"
        response += "🛡️ **Conservative Investing**\n"
        response += "   - Capital preservation\n"
        response += "   - Low risk, modest returns\n"
        response += "   - Best for: Bonds, stable dividend stocks\n\n"
        response += "Which strategy interests you? And how much are you looking to invest?\n"
        return response

    def _handle_education(self, user_message: str) -> str:
        """Handle educational questions."""
        response = "\n📚 Great question! Let me explain:\n\n"
        
        if 'p/e' in user_message.lower() or 'pe ratio' in user_message.lower():
            response += "💡 **P/E Ratio (Price-to-Earnings)**\n"
            response += "   - Shows how much investors are willing to pay per dollar of earnings\n"
            response += "   - Lower P/E = potentially undervalued (cheaper)\n"
            response += "   - Higher P/E = growth expectations (expensive)\n"
            response += "   - Example: P/E of 20 = investors pay $20 for every $1 of earnings\n\n"
        
        elif 'dividend' in user_message.lower():
            response += "💡 **Dividend Yield**\n"
            response += "   - Percentage return from company payouts\n"
            response += "   - Good for income investors\n"
            response += "   - Example: Stock at $100 with $3 dividend = 3% yield\n\n"
        
        elif 'risk' in user_message.lower():
            response += "💡 **Investment Risk**\n"
            response += "   - Higher risk = more volatility but higher potential returns\n"
            response += "   - Lower risk = more stable but lower returns\n"
            response += "   - Diversification helps manage risk\n\n"
        
        elif 'market cap' in user_message.lower():
            response += "💡 **Market Capitalization**\n"
            response += "   - Total value of a company's stock\n"
            response += "   - Large-cap: >$10B (stable, established)\n"
            response += "   - Mid-cap: $2B-$10B (moderate growth)\n"
            response += "   - Small-cap: <$2B (high growth, higher risk)\n\n"
        
        elif 'diversif' in user_message.lower():
            response += "💡 **Diversification**\n"
            response += "   - Spreading investments across different stocks/sectors\n"
            response += "   - Reduces risk by not putting all eggs in one basket\n"
            response += "   - A good portfolio might include: Tech, Healthcare, Finance, Consumer\n\n"
        
        else:
            response += "💡 **Stock Investing Basics**\n"
            response += "   - Buy stocks when they're undervalued (low P/E ratio)\n"
            response += "   - Diversify across different sectors and companies\n"
            response += "   - Invest for the long term (5+ years)\n"
            response += "   - Don't panic sell during market downturns\n"
            response += "   - Consider your risk tolerance and goals\n\n"
        
        response += "Want to know more? Ask me about any stock, or tell me your budget!\n"
        return response

    def _handle_general_question(self, user_message: str) -> str:
        """Handle general conversational questions."""
        response = "\n😊 I'm here to help you invest wisely!\n\n"
        
        if any(word in user_message.lower() for word in ['hi', 'hello', 'hey', 'how are']):
            response = "\n👋 Hi there! I'm doing great, thanks for asking!\n\n"
            response += "I'm here to help you with investment advice. I can:\n\n"
            response += "📊 Analyze specific stocks (just mention the ticker like AAPL, MSFT)\n"
            response += "💡 Recommend stocks based on your budget\n"
            response += "📚 Explain investment concepts\n"
            response += "💰 Help you plan your investment strategy\n\n"
            response += "What can I help you with today?\n"
        
        elif any(word in user_message.lower() for word in ['thank', 'thanks', 'appreciate']):
            response = "\n😊 You're welcome! Happy to help.\n\n"
            response += "Ready to analyze some stocks or get personalized recommendations?\n"
        
        elif any(word in user_message.lower() for word in ['best stock', 'good stock', 'buy']):
            response = "\n🤔 That depends on YOUR specific situation!\n\n"
            response += "The \"best\" stock depends on:\n"
            response += "   💰 How much money you want to invest\n"
            response += "   ⚠️  Your risk tolerance\n"
            response += "   🎯 Your investment goals\n"
            response += "   ⏰ Your investment timeline\n\n"
            response += "Tell me your budget and goals, and I'll recommend the perfect stocks for you!\n"
        
        else:
            response += "I can help you with:\n"
            response += "   • Analyzing specific stocks (mention ticker symbols)\n"
            response += "   • Getting recommendations based on your budget\n"
            response += "   • Understanding investment concepts\n\n"
            response += "What would you like to do?\n"
        
        return response

    def save_conversation(self):
        """Save conversation to file for reference."""
        if not self.conversation_history:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"conversation_{timestamp}.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write("=== FINANCIAL ADVISOR CHAT HISTORY ===\n\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("USER PROFILE:\n")
                f.write(f"  Budget: ${self.user_profile['budget']:,.2f}\n" if self.user_profile['budget'] else "  Budget: Not specified\n")
                f.write(f"  Risk Tolerance: {self.user_profile['risk_tolerance']}\n" if self.user_profile['risk_tolerance'] else "  Risk Tolerance: Not specified\n")
                f.write(f"  Interested Stocks: {', '.join(self.user_profile['interested_stocks'])}\n" if self.user_profile['interested_stocks'] else "")
                f.write("\n" + "="*50 + "\n\n")
                
                for entry in self.conversation_history:
                    f.write(f"You: {entry['user']}\n\n")
                    f.write(f"Assistant: {entry['assistant']}\n\n")
                    f.write("-" * 50 + "\n\n")
            
            print(f"\n✅ Conversation saved to {filename}")
        except Exception as e:
            print(f"\n⚠️  Could not save conversation: {str(e)[:80]}")

    def run(self):
        """Run the chatbot in interactive mode."""
        self.print_welcome()
        
        while True:
            try:
                print()
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                user_lower = user_input.lower()
                
                # Handle commands
                if user_lower in ['exit', 'quit', 'bye', 'goodbye']:
                    print("\n" + "─" * 80)
                    print("\n👋 Thank you for chatting with me!")
                    print("   Remember: Diversify your portfolio and invest wisely!")
                    print("   💡 This was AI-generated advice, not professional financial counsel.\n")
                    self.save_conversation()
                    break
                
                elif user_lower in ['help', '?']:
                    self._print_help()
                    continue
                
                elif user_lower == 'profile':
                    self._print_profile()
                    continue
                
                elif user_lower in ['history', 'chat history']:
                    self._print_history()
                    continue
                
                elif user_lower in ['clear', 'reset']:
                    self.conversation_history = []
                    print("\n🗑️  Conversation history cleared.")
                    continue
                
                # Generate and display response
                print()
                response = self.generate_response(user_input)
                print(f"Assistant:{response}")
                
                # Save to history
                self.conversation_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'user': user_input,
                    'assistant': response
                })
            
            except KeyboardInterrupt:
                print("\n\n👋 Chatbot interrupted. Goodbye!")
                self.save_conversation()
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")
                print("   Please try again or type 'help' for assistance.")

    def _print_help(self):
        """Print help information."""
        print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                      CHATBOT COMMANDS & HELP                              ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 JUST CHAT NATURALLY!
───────────────────────
The chatbot understands context. Try:

   • "I have $5000 to invest"
   • "I'm interested in Apple and Microsoft"
   • "What's a good stock for a conservative investor?"
   • "Explain P/E ratio to me"
   • "I want growth stocks, what do you recommend?"

⌨️  SPECIAL COMMANDS:
────────────────────
   help      - Show this help message
   profile   - Show your investment profile
   history   - Show chat history
   clear     - Clear chat history
   exit/quit - Exit the chatbot

💡 CONVERSATION EXAMPLES:
─────────────────────────

Example 1: Get Recommendations
  You: I have $10,000 and I'm a conservative investor
  Assistant: [Analyzes and recommends safe stocks]

Example 2: Analyze Specific Stock
  You: What about Tesla?
  Assistant: [Provides analysis, asks for budget]

Example 3: Learn About Investing
  You: What is a P/E ratio?
  Assistant: [Explains the concept clearly]

Example 4: Diversified Portfolio
  You: I want to invest $50,000 across different sectors
  Assistant: [Suggests a diversified portfolio]

📊 WHAT I CAN DO:
──────────────────
✓ Analyze any stock you mention
✓ Recommend stocks based on your budget
✓ Explain investment concepts
✓ Help build your investment strategy
✓ Answer questions about risk and returns
✓ Suggest diversification strategies

⚠️  IMPORTANT:
───────────────
• This is AI-generated advice, not professional financial counsel
• Always do your own research
• Consult with a qualified financial advisor
• Past performance doesn't guarantee future results
        """)

    def _print_profile(self):
        """Print user profile."""
        print("\n" + "╔" + "═" * 78 + "╗")
        print("║" + "YOUR INVESTMENT PROFILE".center(78) + "║")
        print("╚" + "═" * 78 + "╝\n")
        
        if self.user_profile['budget']:
            print(f"💰 Budget: ${self.user_profile['budget']:,.2f}")
        else:
            print("💰 Budget: Not specified yet")
        
        if self.user_profile['risk_tolerance']:
            print(f"⚠️  Risk Tolerance: {self.user_profile['risk_tolerance']}")
        else:
            print("⚠️  Risk Tolerance: Not specified yet")
        
        if self.user_profile['interested_stocks']:
            print(f"💎 Interested Stocks: {', '.join(self.user_profile['interested_stocks'])}")
        else:
            print("💎 Interested Stocks: None mentioned yet")
        
        print()

    def _print_history(self):
        """Print conversation history."""
        if not self.conversation_history:
            print("\n📭 No conversation history yet.\n")
            return
        
        print("\n" + "╔" + "═" * 78 + "╗")
        print("║" + "CONVERSATION HISTORY".center(78) + "║")
        print("╚" + "═" * 78 + "╝\n")
        
        for i, entry in enumerate(self.conversation_history, 1):
            user_msg = entry['user'][:60] + "..." if len(entry['user']) > 60 else entry['user']
            timestamp = entry['timestamp'].split('T')[1][:8]
            print(f"{i}. [{timestamp}] You: {user_msg}")
        
        print()


def main():
    """Main entry point."""
    chatbot = ConversationalFinancialChatbot()
    chatbot.run()


if __name__ == "__main__":
    main()
