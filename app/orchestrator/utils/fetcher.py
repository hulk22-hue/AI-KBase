import requests
import json

def fetch_external_data(query: str) -> str:
    """
    Calls a trusted external API or search endpoint.
    For demo: uses DuckDuckGo search.
    """
    try:
        # Example: using DuckDuckGo answer API
        resp = requests.get(f"https://api.duckduckgo.com/?q={query}&format=json")
        data = resp.json()
        abstract = data.get("AbstractText", "")
        if not abstract:
            abstract = f"No direct info found online for '{query}'."
        return abstract
    except Exception as e:
        return f"Error fetching data: {e}"