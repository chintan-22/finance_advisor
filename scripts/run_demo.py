"""
Demo script showing the end-to-end RAG pipeline for financial data.

This script demonstrates:
1. Fetching financial data and news
2. Preprocessing the data
3. Creating embeddings and vectorstore
4. Building and querying a RAG chain
"""

import sys
import os
from datetime import datetime, timedelta
import pandas as pd

# Add parent directory to path to import src module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import FMP_API_KEY, NEWSAPI_API_KEY, CHROMA_PERSIST_DIR_RAG
from src.data_fetch import get_company_quote
from src.news_fetch import fetch_news
from src.preprocess import preprocess_news_articles, preprocess_company_data, combine_datasets
from src.embeddings import build_vectorstore_from_dataframe
from src.rag import build_rag_chain, query_rag, format_result


def main():
    print("=" * 70)
    print("LLM + RAG for Finance - Demo Pipeline")
    print("=" * 70)
    
    # ========== Step 1: Fetch Data ==========
    print("\n[Step 1] Fetching financial data and news...")
    print("-" * 70)
    
    try:
        # Fetch company quote
        ticker = "AAPL"
        print(f"\nFetching quote for {ticker}...")
        
        df_quote = None
        try:
            if FMP_API_KEY and FMP_API_KEY != "your_financialmodelingprep_api_key":
                df_quote = get_company_quote(ticker, FMP_API_KEY)
            else:
                print(f"⚠️  FMP_API_KEY not configured or using placeholder")
        except Exception as fmp_error:
            print(f"⚠️  Could not fetch from FMP API: {fmp_error}")
        
        if df_quote is None or df_quote.empty:
            print(f"   Creating sample data for demo purposes...")
            # Create sample data for demo
            df_quote = pd.DataFrame({
                'symbol': [ticker],
                'price': [150.00],
                'marketCap': [2400000000000],
                'priceAvg50': [145.00],
                'priceAvg200': [140.00],
                'eps': [5.77],
                'pe': [26.0]
            })
        
        print(f"✓ Quote data ready for {ticker}")
        print(f"  Columns: {list(df_quote.columns)}")
        
        # Fetch news
        print(f"\nFetching news for '{ticker}'...")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        df_news = None
        try:
            if NEWSAPI_API_KEY and NEWSAPI_API_KEY != "your_newsapi_api_key":
                df_news = fetch_news(ticker, start_date, end_date, NEWSAPI_API_KEY, page_size=10)
            else:
                print(f"⚠️  NEWSAPI_API_KEY not configured or using placeholder")
        except Exception as news_error:
            print(f"⚠️  Could not fetch from NewsAPI: {news_error}")
        
        if df_news is None or df_news.empty:
            print(f"   Creating sample news data for demo purposes...")
            # Create sample news data
            df_news = pd.DataFrame({
                'title': [
                    f'{ticker} stock rallies on strong earnings',
                    f'{ticker} announces new product line',
                    f'{ticker} expands into emerging markets'
                ],
                'description': [
                    f'{ticker} posted better-than-expected earnings',
                    f'New innovation drives growth prospects',
                    f'Strategic expansion to boost revenues'
                ],
                'content': [
                    f'{ticker} exceeded analyst expectations with strong Q1 results',
                    f'The company unveiled innovative solutions',
                    f'New markets offer growth opportunities'
                ]
            })
        else:
            print(f"✓ Successfully fetched {len(df_news)} news articles")
            print(f"  Columns: {list(df_news.columns)}")
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        print("\nMake sure your API keys are set in the .env file:")
        print("  - FMP_API_KEY (from financialmodelingprep.com)")
        print("  - NEWSAPI_API_KEY (from newsapi.org)")
        return
    
    # ========== Step 2: Preprocess Data ==========
    print("\n[Step 2] Preprocessing data...")
    print("-" * 70)
    
    # Preprocess company data
    df_quote_processed = preprocess_company_data(df_quote)
    print(f"✓ Preprocessed company quote data")
    
    # Preprocess news articles
    if not df_news.empty:
        df_news_processed = preprocess_news_articles(df_news)
        print(f"✓ Preprocessed {len(df_news_processed)} news articles")
        
        # Combine datasets
        df_combined = combine_datasets(df_quote_processed, df_news_processed)
        print(f"✓ Combined datasets: {len(df_combined)} records total")
    else:
        df_combined = df_quote_processed
        print(f"✓ Using company data only: {len(df_combined)} records")
    
    # ========== Step 3: Create Embeddings & Vectorstore ==========
    print("\n[Step 3] Creating embeddings and vectorstore...")
    print("-" * 70)
    
    try:
        # Determine content column
        if "combined_text" in df_combined.columns:
            content_col = "combined_text"
        elif "title" in df_combined.columns:
            content_col = "title"
        else:
            # Create a combined text column from available columns
            df_combined["combined_text"] = df_combined.astype(str).agg(" ".join, axis=1)
            content_col = "combined_text"
        
        # Build vectorstore
        print(f"\nBuilding vectorstore (using '{content_col}' as content)...")
        vectorstore, embeddings = build_vectorstore_from_dataframe(
            df=df_combined,
            content_column=content_col,
            metadata_columns=["title", "symbol"] if "title" in df_combined.columns else [],
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            persist_directory=CHROMA_PERSIST_DIR_RAG,
            collection_name="financial_docs"
        )
        
        print(f"✓ Created vectorstore with {len(df_combined)} documents")
        print(f"✓ Persisted to: {CHROMA_PERSIST_DIR_RAG}")
        
    except Exception as e:
        print(f"Error creating vectorstore: {e}")
        return
    
    # ========== Step 4: Build RAG Chain ==========
    print("\n[Step 4] Building RAG chain...")
    print("-" * 70)
    
    try:
        print("\nBuilding RetrievalQA chain...")
        qa_chain = build_rag_chain(
            vectorstore=vectorstore,
            model_id="mistralai/Mistral-7B-Instruct-v0.1",
            temperature=0.3,
            max_length=512,
            k=4
        )
        print("✓ RAG chain built successfully")
        
    except Exception as e:
        print(f"Error building RAG chain: {e}")
        print("\nMake sure your HUGGINGFACEHUB_API_TOKEN is set in the .env file")
        return
    
    # ========== Step 5: Query the RAG Chain ==========
    print("\n[Step 5] Querying the RAG chain...")
    print("-" * 70)
    
    # Run example queries
    print("\n📌 Running example queries:")
    example_queries = [
        f"What is the current price of {ticker}?",
        f"Tell me about recent news for {ticker}",
        f"What is the market cap of {ticker}?"
    ]
    
    for i, query in enumerate(example_queries, 1):
        print(f"\nExample Query {i}: {query}")
        print("-" * 50)
        
        try:
            result = query_rag(qa_chain, query)
            formatted_result = format_result(result)
            print(formatted_result)
            
        except Exception as e:
            print(f"Error querying RAG chain: {e}")
    
    # Interactive query mode
    print("\n" + "=" * 70)
    print("Interactive Query Mode")
    print("=" * 70)
    print("\n✨ You can now ask your own questions about the data!")
    print("💡 Ask about stock prices, news, market cap, or any financial metric")
    print("   Type 'exit' or 'quit' to end\n")
    
    while True:
        try:
            user_query = input("🤖 Ask a question: ").strip()
            
            if user_query.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Thanks for using the demo! Exiting...")
                break
            
            if not user_query:
                print("⚠️  Please enter a question.\n")
                continue
            
            print(f"\n🔍 Processing: {user_query}")
            print("-" * 50)
            
            result = query_rag(qa_chain, user_query)
            formatted_result = format_result(result)
            print(formatted_result)
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Exiting...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("   Try rephrasing your question or asking about the fetched data.\n")
    
    print("\n" + "=" * 70)
    print("Demo completed!")
    print("=" * 70)
    print("\nℹ️  For interactive investment advice, use the chatbot:")
    print("   python scripts/chatbot.py")


if __name__ == "__main__":
    main()
