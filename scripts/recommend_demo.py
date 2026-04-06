#!/usr/bin/env python3
"""
Quick demo of stock recommendations without analyzing all 15 stocks.
This shows you the TOP recommendations for your investment amount.
"""

import sys
import os

sys.path.insert(0, os.getcwd())

from src.stock_recommender import StockRecommender

def main():
    print("\n" + "="*80)
    print("STOCK RECOMMENDATION ENGINE - QUICK DEMO")
    print("="*80)
    
    recommender = StockRecommender()
    
    # Get recommendations for $5000
    print("\n💰 Investment Amount: $5,000")
    print("\n🔍 Analyzing popular stocks (this may take 2-3 minutes)...\n")
    
    recommendations = recommender.get_stock_recommendations(5000, num_recommendations=5)
    
    # Print summary
    print(recommendations['summary'])
    
    # Print detailed table
    print("\n📊 TOP 5 STOCK RECOMMENDATIONS TABLE:")
    print("─" * 100)
    print(f"{'Rank':<6} {'Ticker':<10} {'Score':<10} {'Sentiment':<15} {'Risk Level':<12} {'P/E Ratio':<12} {'Price':<10}")
    print("─" * 100)
    
    for i, stock in enumerate(recommendations['top_recommendations'], 1):
        emoji = "🟢" if "STRONG BUY" in stock['recommendation'] else "🟢" if "BUY" in stock['recommendation'] else "🟡"
        sentiment_emoji = "📈" if stock['sentiment'] == "POSITIVE" else "📉" if stock['sentiment'] == "NEGATIVE" else "➡️"
        
        print(f"{i:<6} {stock['ticker']:<10} {stock['score']:<10.1f} {stock['sentiment'] + sentiment_emoji:<15} {stock['risk']:<12} {str(stock['pe_ratio']):<12} ${stock['price']:<9.2f}")
    
    print("─" * 100)
    
    print("\n✨ Summary of Categories:")
    print(f"   • STRONG BUY: {len(recommendations['strong_buys'])} stocks")
    print(f"   • BUY: {len(recommendations['buys'])} stocks")
    print(f"   • HOLD/OTHERS: {len(recommendations['holds'])} stocks")
    
    print("\n✅ Demo complete!")
    print("\n💡 To get personalized recommendations, run:")
    print("   python scripts/chatbot.py")
    print("   Then ask: 'Suggest best stocks to invest $5000'")

if __name__ == "__main__":
    main()
