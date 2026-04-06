import pandas as pd
from newsapi import NewsApiClient
from datetime import datetime


def fetch_news(query: str, from_date, to_date, api_key: str, language: str = "en", page_size: int = 100):
    """Fetch news using NewsAPI and return a DataFrame."""
    client = NewsApiClient(api_key=api_key)
    
    # Format dates properly
    if hasattr(from_date, 'date'):
        from_date_str = from_date.date().isoformat()
    else:
        from_date_str = from_date.isoformat() if hasattr(from_date, 'isoformat') else str(from_date)
    
    if hasattr(to_date, 'date'):
        to_date_str = to_date.date().isoformat()
    else:
        to_date_str = to_date.isoformat() if hasattr(to_date, 'isoformat') else str(to_date)
    
    res = client.get_everything(q=query, from_param=from_date_str, to=to_date_str, language=language, page_size=page_size)
    articles = res.get("articles", [])
    if not articles:
        return pd.DataFrame()
    df = pd.DataFrame(articles)
    return df
