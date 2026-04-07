import certifi
import json
from urllib.request import urlopen
import pandas as pd
import requests
from typing import Optional, Dict
import yfinance as yf

# ============================================================================
# ALPHA VANTAGE API (Real-time stock data)
# ============================================================================

def get_stock_data_alpha_vantage(ticker: str, api_key: str) -> Optional[Dict]:
    """Fetch real-time stock data from Alpha Vantage API."""
    try:
        # Get current quote
        url = f"https://www.alphavantage.co/query"
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': ticker,
            'apikey': api_key
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if 'Global Quote' in data and data['Global Quote']:
            quote = data['Global Quote']
            return {
                'price': float(quote.get('05. price', 0)),
                'change': float(quote.get('09. change', 0)),
                'changePercent': float(quote.get('10. change percent', '0').rstrip('%')),
                'bid': float(quote.get('08. bid', 0)),
                'ask': float(quote.get('07. ask', 0)),
                'timestamp': quote.get('07. latest trading day', ''),
            }
    except Exception as e:
        print(f"⚠️  Alpha Vantage API error: {str(e)[:80]}")
    
    return None


# ============================================================================
# YAHOO FINANCE (Historical data and detailed info)
# ============================================================================

def get_stock_data_yahoo(ticker: str) -> Optional[Dict]:
    """Fetch comprehensive stock data from Yahoo Finance."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Get historical data for 50-day and 200-day averages
        hist = stock.history(period="1y")
        
        if len(hist) < 1:
            return None
        
        current_price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        
        # Calculate moving averages
        ma50 = hist['Close'].tail(50).mean() if len(hist) >= 50 else current_price
        ma200 = hist['Close'].tail(200).mean() if len(hist) >= 200 else current_price
        
        return {
            'price': float(current_price),
            'pe_ratio': float(info.get('trailingPE', 0)),
            'market_cap': int(info.get('marketCap', 0)),
            'dividend_yield': float(info.get('dividendYield', 0)) * 100,
            'dividend_per_share': float(info.get('dividendRate', 0)),
            '52_week_high': float(info.get('fiftyTwoWeekHigh', 0)),
            '52_week_low': float(info.get('fiftyTwoWeekLow', 0)),
            'ma50': float(ma50),
            'ma200': float(ma200),
            'volume': int(info.get('volume', 0)),
            'avg_volume': int(info.get('averageVolume', 0)),
            'sector': info.get('sector', 'Unknown'),
            'industry': info.get('industry', 'Unknown'),
            'eps': float(info.get('trailingEps', 0)),
            'beta': float(info.get('beta', 0)),
            'name': info.get('longName', ticker),
        }
    except Exception as e:
        print(f"⚠️  Yahoo Finance error: {str(e)[:80]}")
    
    return None


# ============================================================================
# FINANCIAL MODELING PREP (Backup API)
# ============================================================================

def get_company_quote(ticker: str, api_key: str):
    """Fetch company quote from Financial Modeling Prep."""
    try:
        url = f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={api_key}"
        resp = urlopen(url, cafile=certifi.where()).read().decode("utf-8")
        data = json.loads(resp)
        return pd.DataFrame(data)
    except Exception as e:
        print(f"⚠️  FMP API error: {str(e)[:80]}")
        return pd.DataFrame()


def search_company(ticker: str, api_key: str, exchange: str = "US"):
    """Search a company (example implementation)."""
    try:
        if exchange == "NSE":
            url = f"https://financialmodelingprep.com/api/v3/search?query={ticker}&exchange=NSE&apikey={api_key}"
        else:
            url = f"https://financialmodelingprep.com/api/v3/search?query={ticker}&exchange=US&apikey={api_key}"
        resp = urlopen(url, cafile=certifi.where()).read().decode("utf-8")
        data = json.loads(resp)
        return pd.DataFrame(data)
    except Exception as e:
        print(f"⚠️  FMP search error: {str(e)[:80]}")
        return pd.DataFrame()


# ============================================================================
# UNIFIED STOCK DATA FETCHER
# ============================================================================

def fetch_stock_data(ticker: str, api_keys: Dict[str, str] = None) -> Dict:
    """
    Fetch stock data from multiple sources with fallback.
    
    Priority: Yahoo Finance > Alpha Vantage > Sample Data
    """
    ticker = ticker.upper()
    
    # Try Yahoo Finance first (most reliable for live data)
    data = get_stock_data_yahoo(ticker)
    if data:
        print(f"✓ Fetched live data from Yahoo Finance for {ticker}")
        return data
    
    # Try Alpha Vantage if API key provided
    if api_keys and 'alpha_vantage' in api_keys:
        data = get_stock_data_alpha_vantage(ticker, api_keys['alpha_vantage'])
        if data:
            print(f"✓ Fetched live data from Alpha Vantage for {ticker}")
            return data
    
    # Fallback to FMP if API key provided
    if api_keys and 'fmp' in api_keys:
        df = get_company_quote(ticker, api_keys['fmp'])
        if not df.empty:
            print(f"✓ Fetched data from FMP for {ticker}")
            return df.to_dict('records')[0] if len(df) > 0 else {}
    
    print(f"⚠️  No live data available for {ticker}")
    return {}
