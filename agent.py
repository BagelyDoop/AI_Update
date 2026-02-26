import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
FRIEND_PHONE_NUMBER = os.getenv("FRIEND_PHONE_NUMBER")
FRIEND_PHONE_NUMBER_2 = os.getenv("FRIEND_PHONE_NUMBER_2")
FRIEND_PHONE_NUMBER_3 = os.getenv("FRIEND_PHONE_NUMBER_3")
TEXTBELT_API_KEY = os.getenv("TEXTBELT_API_KEY")


def search_ai_articles():
    url = "https://google.serper.dev/news"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": "artificial intelligence news", "num": 5, "tbs": "qdr:d"}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    results = response.json().get("news", [])
    if not results:
        raise ValueError("No AI articles found today.")
    return results[:3]


def generate_commentary(articles):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": "Bearer " + str(GROQ_API_KEY),
        "Content-Type": "application/json"
    }
    stories = ""
    for i, a in enumerate(articles):
        stories = stories + str(i+1
