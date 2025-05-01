# newsapi/fetch_articles.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

def fetch_articles(query="tariffs", from_date=None, to_date=None):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": API_KEY
    }
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date

    response = requests.get(url, params=params)
    return response.json().get("articles", [])
