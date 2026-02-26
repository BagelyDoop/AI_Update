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
        "Authorization": "Bearer " + str(GROQ_API_KEY),
        "Content-Type": "application/json"
    }
    content = "You are texting your friend who loves baseball about an AI article. Write 2-3 casual sentences using a baseball analogy. End with the link on its own line. Do not start with Hey. Article: " + str(article["title"]) + ". Link: " + str(article["link"])
    body = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": content}],
        "max_tokens": 200
    }
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def send_text(phone, message):
    response = requests.post("https://textbelt.com/text", data={
        "phone": phone,
        "message": message,
        "key": TEXTBELT_API_KEY,
    })
    result = response.json()
    if result.get("success"):
        print("Message sent to " + phone + "!")
    else:
        raise RuntimeError("TextBelt error for " + phone + ": " + str(result.get("error")))


def run():
    print("Running daily AI article agent...")
    article = search_ai_article()
    print("Found: " + article["title"])
    commentary = generate_commentary(article)
    print("Message: " + commentary)
    numbers = [FRIEND_PHONE_NUMBER, FRIEND_PHONE_NUMBER_2, FRIEND_PHONE_NUMBER_3]
    for number in numbers:
        if number:
            send_text(number, commentary)


if __name__ == "__main__":
    run()
