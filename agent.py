import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY        = os.getenv("GROQ_API_KEY")
SERPER_API_KEY      = os.getenv("SERPER_API_KEY")
FRIEND_PHONE_NUMBER = os.getenv("FRIEND_PHONE_NUMBER")


def search_ai_article():
    url = "https://google.serper.dev/news"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": "artificial intelligence news", "num": 5, "tbs": "qdr:d"}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    results = response.json().get("news", [])
    if not results:
        raise ValueError("No AI articles found today.")
    article = results[0]
    return {
        "title": article.get("title", ""),
        "link": article.get("link", ""),
        "snippet": article.get("snippet", ""),
    }


def generate_commentary(article):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": "Bearer " + GROQ_API_KEY,
        "Content-Type": "application/json"
    }
    prompt = (
        "You are texting your friend who is a huge baseball fan about a cool AI news article. "
        "Write a SHORT (2-3 sentences max) fun text message that uses a baseball analogy or
