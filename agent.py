"""
Daily AI Article Texter Agent (100% Free Stack)
=================================================
- Serper.dev     → search Google News for AI articles (2,500 free/month)
- Google Gemini  → write baseball-flavored commentary (free tier)
- TextBelt       → send 1 free SMS per day (no credit card)

Run manually:
    pip install requests python-dotenv
    python agent.py

Schedule for free via GitHub Actions — see README.md
"""

import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ── Config ───────────────────────────────────────────────────────────────────
GEMINI_API_KEY      = os.getenv("GEMINI_API_KEY")       # aistudio.google.com
SERPER_API_KEY      = os.getenv("SERPER_API_KEY")       # serper.dev
FRIEND_PHONE_NUMBER = os.getenv("FRIEND_PHONE_NUMBER")  # e.g. +15559876543
# ─────────────────────────────────────────────────────────────────────────────


def search_ai_article() -> dict:
    """Search for a fresh AI news article using Serper (Google News)."""
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
    """Use Gemini (free) to write a short baseball-flavored text message."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    prompt = f"""You are texting your friend who is a huge baseball fan about a cool AI news article.
Write a SHORT (2-3 sentences max) fun text message that:
- Uses a baseball analogy, metaphor, or reference to explain why this AI news is interesting
- Sounds casual and friendly, like a text from a buddy
- Ends with the article link on its own line
- Does NOT start with "Hey" (mix it up)

Article title: {article['title']}
Article snippet: {article['snippet']}
Article link: {article['link']}

Write only the text message, nothing else."""

    body = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(url, json=body)
    response.raise_for_status()
    return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()


def send_text(message: str) -> None:
    """Send SMS via TextBelt (1 free text/day, no account needed)."""
    response = requests.post("https://textbelt.com/text", data={
        "phone": FRIEND_PHONE_NUMBER,
        "message": message,
        "key": "textbelt",   # magic key for 1 free SMS/day
    })
    result = response.json()
    if result.get("success"):
        print(f"[{datetime.now()}] Message sent! ID: {result.get('textId')}")
    else:
        raise RuntimeError(f"TextBelt error: {result.get('error')}")


def run():
    print(f"[{datetime.now()}] Running daily AI article agent...")
    article    = search_ai_article()
    print(f"  Found: {article['title']}")
    commentary = generate_commentary(article)
    print(f"  Message:\n{commentary}\n")
    send_text(commentary)


if __name__ == "__main__":
    run()
