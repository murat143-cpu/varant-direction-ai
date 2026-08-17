import os, requests

class YahooProvider:
    def quote(self, symbol):
        url="https://query1.finance.yahoo.com/v8/finance/chart/"+symbol
        r=requests.get(url, params={"range":"1d","interval":"5m"}, timeout=10)
        r.raise_for_status()
        return r.json()

class FinnhubProvider:
    def __init__(self, api_key=None):
        self.api_key=api_key or os.getenv("FINNHUB_API_KEY")
    def quote(self, symbol):
        if not self.api_key:
            raise RuntimeError("FINNHUB_API_KEY is not configured")
        r=requests.get("https://finnhub.io/api/v1/quote",
                       params={"symbol":symbol,"token":self.api_key}, timeout=10)
        r.raise_for_status()
        return r.json()
