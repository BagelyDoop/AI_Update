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
    a1 = str(articles[0].get("title", "")) + ": " + str(articles[0].get("snippet", ""))
    a2 = str(articles[1].get("title", "")) + ": " + str(articles[1].get("snippet", ""))
    a3 = str(articles[2].get("title", "")) + ": " + str(articles[2].get("snippet", ""))
    content = "You are texting your friend who loves baseball about 3 AI news stories. For each story write exactly 2 casual sentences using a baseball analogy. Number each story 1, 2, 3. No links. Keep the whole message under 300 characters total. Stories: 1. " + a1 + " 2. " + a2 + " 3. " + a3
    body = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": content}],
        "max_tokens": 300
    }
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def send_text(phone, message):
    response = requests.post("https:/
