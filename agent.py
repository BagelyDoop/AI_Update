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
        "Write a SHORT (2-3 sentences max) fun text message that uses a baseball analogy or reference, "
        "sounds casual and friendly like a text from a buddy, ends with the article link on its own line, "
        "and does NOT start with Hey.\n\n"
        "Article title: " + article["title"] + "\n"
        "Article snippet: " + article["snippet"] + "\n"
        "Article link: " + article["link"] + "\n\n"
        "Write only the text message, nothing else."
    )
    body = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200
    }
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()


def send_text(message):
    response = requests.post("https://textbelt.com/text", data={
        "phone": FRIEND_PHONE_NUMBER,
        "message": message,
        "key": "textbelt",
    })
    result = response.json()
    if result.get("success"):
        print("Message sent! ID: " + str(result.get("textId")))
    else:
        raise RuntimeError("TextBelt error: " + str(result.get("error")))


def run():
    print("Running daily AI article agent...")
    article = search_ai_article()
    print("Found: " + article["title"])
    commentary = generate_commentary(article)
    print("Message:\n" + commentary)
    send_text(commentary)


if __name__ == "__main__":
    run()
