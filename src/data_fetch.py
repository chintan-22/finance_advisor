import certifi
import json
from urllib.request import urlopen
import pandas as pd

# Financial Modeling Prep helpers

def get_company_quote(ticker: str, api_key: str):
    """Fetch company quote from Financial Modeling Prep."""
    url = f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={api_key}"
    resp = urlopen(url, cafile=certifi.where()).read().decode("utf-8")
    data = json.loads(resp)
    return pd.DataFrame(data)


def search_company(ticker: str, api_key: str, exchange: str = "US"):
    """Search a company (example implementation)."""
    if exchange == "NSE":
        url = f"https://financialmodelingprep.com/api/v3/search?query={ticker}&exchange=NSE&apikey={api_key}"
    else:
        url = f"https://financialmodelingprep.com/api/v3/search?query={ticker}&exchange=US&apikey={api_key}"
    resp = urlopen(url, cafile=certifi.where()).read().decode("utf-8")
    data = json.loads(resp)
    return pd.DataFrame(data)
