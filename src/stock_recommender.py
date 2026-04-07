"""
Stock Recommender - Suggests the best stocks to invest in based on various criteria.

This module provides functionality to recommend top stocks for a given investment amount
using multiple analysis strategies.
"""

import pandas as pd
from typing import List, Dict, Tuple
from src.financial_advisor import FinancialAdvisor
from src.config import NEWSAPI_API_KEY


class StockRecommender:
    """Recommends best stocks for investment."""
    
    # Popular stocks for recommendation
    POPULAR_STOCKS = [
        "AAPL",  # Apple
        "MSFT",  # Microsoft
        "GOOGL", # Google
        "AMZN",  # Amazon
        "TSLA",  # Tesla
        "NVDA",  # Nvidia
        "META",  # Meta
        "NFLX",  # Netflix
        "JPM",   # JPMorgan Chase
        "V",     # Visa
        "JNJ",   # Johnson & Johnson
        "PG",    # Procter & Gamble
        "UNH",   # UnitedHealth
        "HD",    # Home Depot
        "DIS",   # Disney
    ]
    
    def __init__(self):
        """Initialize the stock recommender."""
        self.advisor = FinancialAdvisor()
        self.recommendations_cache = {}
    
    def get_stock_recommendations(self, investment_amount: float, 
                                  num_recommendations: int = 5,
                                  risk_tolerance: str = 'MEDIUM') -> Dict:
        """
        Get top stock recommendations for the given investment amount.
        
        Args:
            investment_amount: Amount to invest
            num_recommendations: Number of stocks to recommend (default: 5)
            risk_tolerance: Risk tolerance level - 'LOW', 'MEDIUM', or 'HIGH' (default: 'MEDIUM')
            
        Returns:
            Dictionary with recommended stocks and analysis
        """
        print(f"\n🔍 Analyzing {len(self.POPULAR_STOCKS)} popular stocks...")
        print("   This may take a moment...\n")
        
        analyses = []
        strong_buys = []
        buys = []
        holds = []
        
        for i, ticker in enumerate(self.POPULAR_STOCKS, 1):
            print(f"   [{i}/{len(self.POPULAR_STOCKS)}] Analyzing {ticker}...", end="\r")
            
            try:
                # Analyze each stock
                analysis = self.advisor.analyze_investment_opportunity(
                    ticker, 
                    investment_amount
                )
                
                # Extract key data
                recommendation = analysis['recommendation']
                risk = analysis['risk_assessment']
                sentiment = analysis['sentiment']
                metrics = analysis['financial_metrics']
                
                # Score the stock for ranking
                score = self._calculate_investment_score(
                    recommendation, 
                    risk, 
                    sentiment, 
                    metrics,
                    risk_tolerance  # Pass risk tolerance to scorer
                )
                
                stock_data = {
                    'ticker': ticker,
                    'score': score,
                    'sentiment': sentiment,
                    'risk': risk,
                    'pe_ratio': metrics.get('pe_ratio', 'N/A'),
                    'price': metrics.get('current_price', 'N/A'),
                    'recommendation': analysis['recommendation'],
                    'full_analysis': analysis
                }
                
                analyses.append(stock_data)
                
                # Categorize by recommendation level
                if 'STRONG BUY' in recommendation:
                    strong_buys.append(stock_data)
                elif 'BUY' in recommendation:
                    buys.append(stock_data)
                else:
                    holds.append(stock_data)
                    
            except Exception as e:
                print(f"   Error analyzing {ticker}: {e}", end="\r")
                continue
        
        print(" " * 60, end="\r")  # Clear the line
        
        # Sort by score
        analyses.sort(key=lambda x: x['score'], reverse=True)
        
        # Get top recommendations
        top_recommendations = analyses[:num_recommendations]
        
        return {
            'investment_amount': investment_amount,
            'risk_tolerance': risk_tolerance,
            'timestamp': pd.Timestamp.now().isoformat(),
            'top_recommendations': top_recommendations,
            'strong_buys': strong_buys,
            'buys': buys,
            'holds': holds,
            'all_analyses': analyses,
            'summary': self._generate_recommendation_summary(
                top_recommendations,
                investment_amount,
                risk_tolerance
            )
        }
    
    def _calculate_investment_score(self, recommendation: str, risk: str, 
                                   sentiment: str, metrics: Dict, 
                                   user_risk_tolerance: str = 'MEDIUM') -> float:
        """
        Calculate an investment score for ranking based on user's risk tolerance.
        
        Args:
            recommendation: Recommendation text
            risk: Stock's risk level
            sentiment: Market sentiment
            metrics: Financial metrics
            user_risk_tolerance: User's risk tolerance - 'LOW', 'MEDIUM', or 'HIGH'
            
        Returns:
            Score between 0-100
        """
        score = 0
        
        # Recommendation score (0-50 points)
        if 'STRONG BUY' in recommendation:
            score += 50
        elif 'BUY' in recommendation:
            score += 35
        elif 'HOLD' in recommendation:
            score += 15
        else:
            score += 0
        
        # Risk matching score (0-30 points) - Match user preference to stock risk
        # Conservative investors prefer LOW risk stocks
        # Moderate investors are OK with MEDIUM risk
        # Aggressive investors prefer HIGH risk for growth
        
        if user_risk_tolerance == 'LOW':
            # Conservative investor - penalize high-risk stocks
            if risk == 'LOW':
                score += 30  # Perfect match
            elif risk == 'MEDIUM':
                score += 15  # Acceptable
            else:
                score += 0   # Too risky
                
        elif user_risk_tolerance == 'HIGH':
            # Aggressive investor - prefer growth/high-risk stocks
            if risk == 'HIGH':
                score += 30  # Perfect match for growth
            elif risk == 'MEDIUM':
                score += 15  # Acceptable
            else:
                score += 5   # Too conservative/stable
                
        else:  # MEDIUM
            # Moderate investor - balanced approach
            if risk == 'MEDIUM':
                score += 30  # Perfect match
            elif risk in ['LOW', 'HIGH']:
                score += 15  # Acceptable on either side
            else:
                score += 10
        
        # Sentiment score (0-20 points)
        if sentiment == 'POSITIVE':
            score += 20
        elif sentiment == 'NEUTRAL':
            score += 10
        else:
            score += 0
        
        # Valuation bonus (0-10 points) - Lower P/E is better
        pe_ratio = metrics.get('pe_ratio')
        if pe_ratio and isinstance(pe_ratio, (int, float)):
            if pe_ratio < 20:
                score += 10
            elif pe_ratio < 30:
                score += 5
        
        return min(score, 100)  # Cap at 100
    
    def _generate_recommendation_summary(self, top_stocks: List[Dict], 
                                        investment_amount: float,
                                        risk_tolerance: str = 'MEDIUM') -> str:
        """
        Generate a summary of recommendations.
        
        Args:
            top_stocks: List of top recommended stocks
            investment_amount: Investment amount
            risk_tolerance: User's risk tolerance level
            
        Returns:
            Formatted summary string
        """
        # Map risk tolerance to display name
        risk_names = {
            'LOW': '🟢 Conservative',
            'MEDIUM': '🟡 Moderate',
            'HIGH': '🔴 Aggressive'
        }
        
        summary = f"""
╔══════════════════════════════════════════════════════════════════════════╗
║                    TOP STOCK RECOMMENDATIONS                            ║
╚══════════════════════════════════════════════════════════════════════════╝

💰 INVESTMENT AMOUNT: ${investment_amount:,.2f}
⚠️  RISK TOLERANCE: {risk_names.get(risk_tolerance, risk_tolerance)}

🏆 TOP {len(top_stocks)} RECOMMENDED STOCKS:
{'─' * 76}

"""
        for i, stock in enumerate(top_stocks, 1):
            summary += f"""
{i}. {stock['ticker'].upper()}
   • Score: {stock['score']:.1f}/100
   • Sentiment: {stock['sentiment']} {'📈' if stock['sentiment'] == 'POSITIVE' else '📉' if stock['sentiment'] == 'NEGATIVE' else '➡️'}
   • Risk Level: {stock['risk']}
   • P/E Ratio: {stock['pe_ratio']}
   • Current Price: ${stock['price']}
"""
        
        summary += f"""
{'─' * 76}

⚠️  IMPORTANT DISCLAIMERS:
──────────────────────────
1. This is AI-generated analysis, NOT financial advice
2. Past performance does not guarantee future results
3. Always consult with a qualified financial advisor
4. Consider your risk tolerance and investment timeline
5. Diversify your portfolio across multiple stocks

📌 NEXT STEPS:
───────────────
1. Review each recommendation in detail
2. Compare the stocks based on your preferences
3. Consider how they fit into your portfolio
4. Make investment decisions only after careful consideration
5. Monitor your investments regularly

╚══════════════════════════════════════════════════════════════════════════╝
"""
        return summary
    
    def print_detailed_recommendation(self, stock_data: Dict):
        """
        Print detailed analysis for a recommended stock.
        
        Args:
            stock_data: Stock analysis data
        """
        print(stock_data['recommendation'])
        print(f"\n📊 INVESTMENT SCORE: {stock_data['score']:.1f}/100")
