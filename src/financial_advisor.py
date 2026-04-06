"""
Financial Advisor - AI-powered investment recommendation engine.

This module provides an intelligent financial advisor that analyzes stock data,
news, and market information to provide investment recommendations.
"""

import re
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional
import pandas as pd
from src.config import FMP_API_KEY, NEWSAPI_API_KEY, CHROMA_PERSIST_DIR_RAG
from src.data_fetch import get_company_quote, search_company
from src.news_fetch import fetch_news
from src.preprocess import preprocess_news_articles, preprocess_company_data, combine_datasets
from src.embeddings import build_vectorstore_from_dataframe, load_vectorstore, create_embeddings
from src.rag import build_rag_chain, query_rag, format_result


class FinancialAdvisor:
    """AI-powered financial advisor for investment recommendations."""
    
    def __init__(self):
        """Initialize the financial advisor."""
        self.qa_chain = None
        self.current_ticker = None
        self.current_investment_amount = None
        self.analysis_data = {}
        
    def analyze_investment_opportunity(self, ticker: str, investment_amount: float) -> Dict:
        """
        Analyze a stock and provide investment recommendation.
        
        Args:
            ticker: Stock ticker symbol (e.g., "AAPL")
            investment_amount: Amount user wants to invest in dollars
            
        Returns:
            Dictionary with analysis results and recommendation
        """
        print(f"\n📊 Analyzing {ticker.upper()} for ${investment_amount:,.2f} investment...")
        print("-" * 70)
        
        self.current_ticker = ticker.upper()
        self.current_investment_amount = investment_amount
        self.analysis_data = {}
        
        # Step 1: Fetch company data
        print("\n[Step 1/5] Fetching company financial data...")
        df_quote = self._fetch_company_data(ticker)
        if df_quote is None or df_quote.empty:
            return {"error": "Could not fetch company data", "recommendation": "Unable to analyze"}
        
        # Step 2: Fetch news
        print("[Step 2/5] Fetching recent news and market sentiment...")
        df_news = self._fetch_news_data(ticker)
        
        # Step 3: Preprocess data
        print("[Step 3/5] Preprocessing and analyzing data...")
        df_combined = self._preprocess_data(df_quote, df_news)
        
        # Step 4: Build knowledge base
        print("[Step 4/5] Building AI knowledge base...")
        vectorstore = self._build_vectorstore(df_combined)
        
        # Step 5: Generate recommendation
        print("[Step 5/5] Generating investment recommendation...")
        recommendation = self._generate_recommendation(ticker, investment_amount, df_quote, df_news, vectorstore)
        
        self.analysis_data = recommendation
        return recommendation
    
    def _fetch_company_data(self, ticker: str) -> Optional[pd.DataFrame]:
        """Fetch company financial data."""
        try:
            df_quote = get_company_quote(ticker, FMP_API_KEY)
            if not df_quote.empty:
                print(f"✓ Successfully fetched {ticker} financial data")
                return df_quote
        except Exception as e:
            print(f"⚠️  Could not fetch from FMP API: {str(e)[:80]}")
        
        # Fallback to sample data
        print("   Using sample data for demo purposes...")
        return pd.DataFrame({
            'symbol': [ticker],
            'price': [150.00],
            'marketCap': [2400000000000],
            'priceAvg50': [145.00],
            'priceAvg200': [140.00],
            'eps': [5.77],
            'pe': [26.0],
            'dividend': [0.93],
            'dividendYield': [0.62]
        })
    
    def _fetch_news_data(self, ticker: str) -> pd.DataFrame:
        """Fetch news data for sentiment analysis."""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            
            df_news = fetch_news(ticker, start_date, end_date, NEWSAPI_API_KEY, page_size=15)
            if not df_news.empty:
                print(f"✓ Successfully fetched {len(df_news)} news articles")
                return df_news
        except Exception as e:
            print(f"⚠️  Could not fetch news: {str(e)[:80]}")
        
        # Fallback to sample news
        print("   Using sample news data for demo purposes...")
        return pd.DataFrame({
            'title': [
                f'{ticker} beats Q1 earnings estimates',
                f'{ticker} announces new product innovation',
                f'{ticker} expands market share in key regions',
                f'{ticker} strengthens supply chain partnerships',
                f'{ticker} receives positive analyst upgrade'
            ],
            'description': [
                'Strong quarterly performance drives growth',
                'New technology adoption increases demand',
                'Market expansion shows strong potential',
                'Strategic partnerships boost efficiency',
                'Analysts bullish on future prospects'
            ],
            'content': [
                f'{ticker} exceeded expectations in quarterly earnings',
                f'New product launch receives market acclaim',
                f'{ticker} gains competitive advantage',
                f'Supply chain improvements reduce costs',
                f'Multiple analyst firms upgrade to buy rating'
            ]
        })
    
    def _preprocess_data(self, df_quote: pd.DataFrame, df_news: pd.DataFrame) -> pd.DataFrame:
        """Preprocess financial and news data."""
        df_quote_processed = preprocess_company_data(df_quote)
        
        if not df_news.empty:
            df_news_processed = preprocess_news_articles(df_news)
            df_combined = combine_datasets(df_quote_processed, df_news_processed)
        else:
            df_combined = df_quote_processed
        
        print(f"✓ Processed {len(df_combined)} data records")
        return df_combined
    
    def _build_vectorstore(self, df_combined: pd.DataFrame):
        """Build vectorstore from combined data."""
        try:
            if "combined_text" in df_combined.columns:
                content_col = "combined_text"
            elif "title" in df_combined.columns:
                content_col = "title"
            else:
                df_combined["combined_text"] = df_combined.astype(str).agg(" ".join, axis=1)
                content_col = "combined_text"
            
            vectorstore, _ = build_vectorstore_from_dataframe(
                df=df_combined,
                content_column=content_col,
                metadata_columns=["title"] if "title" in df_combined.columns else [],
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                persist_directory=CHROMA_PERSIST_DIR_RAG,
                collection_name="financial_advisor"
            )
            
            print("✓ Knowledge base built successfully")
            return vectorstore
        except Exception as e:
            print(f"⚠️  Error building vectorstore: {e}")
            return None
    
    def _generate_recommendation(self, ticker: str, investment_amount: float, 
                                 df_quote: pd.DataFrame, df_news: pd.DataFrame,
                                 vectorstore) -> Dict:
        """Generate investment recommendation based on analysis."""
        
        recommendation = {
            "ticker": ticker,
            "investment_amount": investment_amount,
            "timestamp": datetime.now().isoformat(),
            "financial_metrics": {},
            "sentiment": "",
            "risk_assessment": "",
            "recommendation": "",
            "detailed_analysis": ""
        }
        
        # Extract financial metrics
        if not df_quote.empty:
            quote = df_quote.iloc[0]
            recommendation["financial_metrics"] = {
                "current_price": float(quote.get('price', 0)),
                "market_cap": float(quote.get('marketCap', 0)),
                "pe_ratio": float(quote.get('pe', 0)),
                "eps": float(quote.get('eps', 0)),
                "dividend_yield": float(quote.get('dividendYield', 0)),
                "52week_avg_50": float(quote.get('priceAvg50', 0)),
                "52week_avg_200": float(quote.get('priceAvg200', 0))
            }
        
        # Analyze sentiment from news
        sentiment_score = self._analyze_news_sentiment(df_news)
        recommendation["sentiment"] = sentiment_score
        
        # Calculate risk assessment
        risk_level = self._calculate_risk_level(recommendation["financial_metrics"])
        recommendation["risk_assessment"] = risk_level
        
        # Generate recommendation
        recommendation_text = self._generate_recommendation_text(
            ticker, investment_amount, recommendation["financial_metrics"], 
            sentiment_score, risk_level
        )
        recommendation["recommendation"] = recommendation_text
        
        # Get detailed analysis from RAG
        if vectorstore:
            try:
                qa_chain = build_rag_chain(vectorstore=vectorstore)
                
                analysis_query = f"""
                Based on the available data, provide a comprehensive investment analysis for {ticker}.
                Consider the financial metrics, market sentiment, and recent news to support the investment decision.
                """
                
                result = query_rag(qa_chain, analysis_query)
                recommendation["detailed_analysis"] = result.get("result", "")
            except Exception as e:
                recommendation["detailed_analysis"] = f"Could not generate detailed analysis: {str(e)}"
        
        return recommendation
    
    def _analyze_news_sentiment(self, df_news: pd.DataFrame) -> str:
        """Analyze sentiment from news articles."""
        if df_news.empty:
            return "NEUTRAL"
        
        # Simple sentiment analysis based on keywords
        positive_keywords = ["beats", "surge", "rally", "upgrade", "growth", "strong", "positive", "profit"]
        negative_keywords = ["decline", "drop", "downgrade", "loss", "weak", "negative", "risk", "concern"]
        
        text = " ".join(df_news.get('title', []).astype(str).tolist()).lower()
        
        positive_count = sum(text.count(kw) for kw in positive_keywords)
        negative_count = sum(text.count(kw) for kw in negative_keywords)
        
        if positive_count > negative_count * 1.5:
            return "POSITIVE"
        elif negative_count > positive_count * 1.5:
            return "NEGATIVE"
        else:
            return "NEUTRAL"
    
    def _calculate_risk_level(self, metrics: Dict) -> str:
        """Calculate risk level based on financial metrics."""
        if not metrics:
            return "UNKNOWN"
        
        pe_ratio = metrics.get('pe_ratio', 0)
        market_cap = metrics.get('market_cap', 0)
        dividend_yield = metrics.get('dividend_yield', 0)
        
        risk_score = 0
        
        # High PE ratio increases risk
        if pe_ratio > 30:
            risk_score += 2
        elif pe_ratio > 20:
            risk_score += 1
        
        # Very small market cap increases risk
        if market_cap < 100000000:  # Less than $100M
            risk_score += 3
        elif market_cap < 1000000000:  # Less than $1B
            risk_score += 2
        
        # Low dividend yield (not paying dividends)
        if dividend_yield < 0.5:
            risk_score += 1
        
        if risk_score >= 4:
            return "HIGH"
        elif risk_score >= 2:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _generate_recommendation_text(self, ticker: str, amount: float, 
                                      metrics: Dict, sentiment: str, risk: str) -> str:
        """Generate recommendation text."""
        
        current_price = metrics.get('current_price', 0)
        shares_possible = amount / current_price if current_price > 0 else 0
        pe_ratio = metrics.get('pe_ratio', 0)
        
        # Base recommendation on multiple factors
        score = 0
        
        if sentiment == "POSITIVE":
            score += 2
        elif sentiment == "NEGATIVE":
            score -= 2
        
        if risk == "LOW":
            score += 2
        elif risk == "HIGH":
            score -= 2
        
        if pe_ratio > 0 and pe_ratio < 15:
            score += 1
        elif pe_ratio > 30:
            score -= 1
        
        if score >= 3:
            recommendation = "STRONG BUY"
        elif score >= 1:
            recommendation = "BUY"
        elif score <= -2:
            recommendation = "STRONG SELL"
        elif score <= -1:
            recommendation = "SELL"
        else:
            recommendation = "HOLD"
        
        text = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 INVESTMENT RECOMMENDATION: {recommendation}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 INVESTMENT SUMMARY
─────────────────────
• Ticker: {ticker}
• Investment Amount: ${amount:,.2f}
• Current Stock Price: ${current_price:.2f}
• Potential Shares: {shares_possible:.2f}
• Market Sentiment: {sentiment}
• Risk Level: {risk}
• P/E Ratio: {pe_ratio:.2f}x

🎯 KEY FACTORS
──────────────
1. SENTIMENT: {self._sentiment_explanation(sentiment)}
2. RISK: {self._risk_explanation(risk)}
3. VALUATION: {self._valuation_explanation(pe_ratio)}

⚠️  IMPORTANT DISCLAIMER
────────────────────────
This is an AI-generated recommendation based on available data. It is NOT 
financial advice. Always consult with a qualified financial advisor before 
making investment decisions. Past performance does not guarantee future results.

📋 NEXT STEPS
─────────────
1. Review the detailed analysis below
2. Consider your risk tolerance and investment timeline
3. Diversify your portfolio
4. Monitor the stock regularly
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return text
    
    def _sentiment_explanation(self, sentiment: str) -> str:
        """Get sentiment explanation."""
        explanations = {
            "POSITIVE": "Recent news shows bullish sentiment with positive developments",
            "NEGATIVE": "Recent news shows bearish sentiment with concerning developments",
            "NEUTRAL": "Mixed sentiment in recent news with no clear direction"
        }
        return explanations.get(sentiment, "Unknown sentiment")
    
    def _risk_explanation(self, risk: str) -> str:
        """Get risk explanation."""
        explanations = {
            "LOW": "Established company with strong financials (suitable for conservative investors)",
            "MEDIUM": "Moderate risk profile (suitable for balanced investors)",
            "HIGH": "Higher volatility and risk factors (suitable for aggressive investors)"
        }
        return explanations.get(risk, "Unknown risk level")
    
    def _valuation_explanation(self, pe_ratio: float) -> str:
        """Get valuation explanation."""
        if pe_ratio <= 0:
            return "Company is not profitable"
        elif pe_ratio < 15:
            return f"Undervalued (P/E: {pe_ratio:.1f}x - Below market average)"
        elif pe_ratio < 25:
            return f"Fairly valued (P/E: {pe_ratio:.1f}x - Market average)"
        else:
            return f"Overvalued (P/E: {pe_ratio:.1f}x - Above market average)"
    
    def get_recommendation_report(self) -> str:
        """Get formatted recommendation report."""
        if not self.analysis_data:
            return "No analysis data available. Please run analyze_investment_opportunity first."
        
        report = self.analysis_data.get("recommendation", "")
        
        if self.analysis_data.get("detailed_analysis"):
            report += "\n\n🔬 DETAILED ANALYSIS\n"
            report += "─" * 70 + "\n"
            report += self.analysis_data["detailed_analysis"]
        
        return report
