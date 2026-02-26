import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY        = os.getenv("GROQ_API_KEY")
SERPER_API_KEY      = os.getenv("SERPER_API_KEY")
FRIEND_PHONE_NUMBER = os.getenv("FRIEND_PHONE_NUMBER")


def search_ai_article() -> dict:
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
        "title":   article.get("title", ""),
        "link":    article.get("link", ""),
        "snippet": article.get("snippet", ""),
    }


def generate_commentary(article: dict) -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    prompt = f"""You are texting your friend who is a huge baseball fan about a cool AI news article.
Write a SHORT (2-3 sentences max) fun text message that:
- Uses a baseball analogy, metaphor, or reference
- Sounds casual and friendly, like a text from a buddy
- Ends with the article link on its own line
- Does NOT start with "Hey"

Article title: {article['title']}
Article snippet: {article['snippet']}
Article link: {article['link']}

Write only the text message, nothing else."""

    body = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "​​​​​​​​​​​​​​​​
