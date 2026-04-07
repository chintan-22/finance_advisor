#!/usr/bin/env python3
"""
Quick test script to verify Streamlit app setup
"""

import subprocess
import sys
import os

def print_header(text):
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80 + "\n")

def test_imports():
    print_header("Testing Required Imports")
    
    required = {
        'streamlit': 'Web app framework',
        'yfinance': 'Stock data provider',
        'plotly': 'Interactive charts',
        'langchain': 'LLM orchestration',
        'pandas': 'Data processing',
        'scipy': 'Scientific computing',
    }
    
    missing = []
    
    for module, description in required.items():
        try:
            __import__(module)
            print(f"✅ {module:<20} - {description}")
        except ImportError:
            print(f"❌ {module:<20} - {description}")
            missing.append(module)
    
    return len(missing) == 0

def test_data_fetching():
    print_header("Testing Live Data Fetching")
    
    try:
        import yfinance as yf
        
        tickers = ['AAPL', 'MSFT', 'GOOGL']
        
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                info = stock.info
                price = info.get('currentPrice')
                pe = info.get('trailingPE')
                
                if price:
                    print(f"✅ {ticker:<6} - Price: ${price:>8.2f}, P/E: {pe:>6.1f}x")
                else:
                    print(f"⚠️  {ticker:<6} - Could not fetch price")
            except Exception as e:
                print(f"❌ {ticker:<6} - Error: {str(e)[:50]}")
        
        return True
    except Exception as e:
        print(f"❌ Error testing data: {str(e)}")
        return False

def test_financial_advisor():
    print_header("Testing Financial Advisor Module")
    
    try:
        from src.financial_advisor import FinancialAdvisor
        from src.stock_recommender import StockRecommender
        
        print("✅ FinancialAdvisor imported successfully")
        print("✅ StockRecommender imported successfully")
        
        # Try to initialize
        advisor = FinancialAdvisor()
        recommender = StockRecommender()
        
        print("✅ FinancialAdvisor initialized successfully")
        print("✅ StockRecommender initialized successfully")
        
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)[:100]}")
        return False

def main():
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + "  🎯 AI FINANCIAL ADVISOR - STREAMLIT SETUP TEST".center(78) + "║")
    print("╚" + "="*78 + "╝")
    
    # Change to project directory
    os.chdir('/Users/chintanshah/Documents/llm_rag_finance')
    
    results = {
        'Imports': test_imports(),
        'Data Fetching': test_data_fetching(),
        'Financial Advisor': test_financial_advisor(),
    }
    
    print_header("📋 Test Summary")
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*80)
    
    if all_passed:
        print("\n🎉 All tests passed! Your setup is ready.\n")
        print("To launch the Streamlit app, run:")
        print("\n    ./run_streamlit.sh")
        print("\nOr manually:")
        print("\n    streamlit run app.py\n")
        print("The app will open at: http://localhost:8501\n")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the errors above.\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
