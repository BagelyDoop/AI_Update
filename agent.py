import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
TEXTBELT_API_KEY = os.getenv("TEXTBELT_API_KEY")

FRIEND_PHONE_NUMBER = os.getenv("FRIEND_PHONE_NUMBER")
FRIEND_PHONE_NUMBER_2 = os.getenv("FRIEND_PHONE_NUMBER_2")
FRIEND_PHONE_NUMBER_3 = os.getenv("FRIEND_PHONE_NUMBER_3")


def require_env(name: str, value: str | None) -> str:
    if not value or not value.strip():
        raise ValueError(f"Missing required env var: {name}")
    return value.strip()


def search_ai_articles():
    """Pull recent AI news from Serper."""
    serper_key = require_env("SERPER_API_KEY", SERPER_API_KEY)

    url = "https://google.serper.dev/news"
    headers = {"X-API-KEY": serper_key, "Content-Type": "application/json"}
    payload = {"q": "artificial intelligence news", "num": 5, "tbs": "qdr:d"}  # last day
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()

    results = response.json().get("news", []) or []
    if len(results) < 3:
        raise ValueError("Not enough AI articles found today (need at least 3).")

    return results[:3]


def generate_commentary(articles):
    """Use Groq OpenAI-compatible endpoint to generate a short baseball-analogy text."""
    groq_key = require_env("GROQ_API_KEY", GROQ_API_KEY)

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {groq_key}",
        "Content-Type": "application/json",
    }

    a1 = f"{articles[0].get('title','')}: {articles[0].get('snippet','')}"
    a2 = f"{articles[1].get('title','')}: {articles[1].get('snippet','')}"
    a3 = f"{articles[2].get('title','')}: {articles[2].get('snippet','')}"

    content = (
        "You are texting your friend who loves baseball about 3 AI news stories. "
        "For each story write exactly 2 casual sentences using a baseball analogy. "
        "Number each story 1, 2, 3. No links. Keep the whole message under 300 characters total. "
        f"Stories: 1. {a1} 2. {a2} 3. {a3}"
    )

    body = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": content}],
        "max_tokens": 120,  # tokens != chars; keep small to encourage brevity
        "temperature": 0.7,
    }

    response = requests.post(url, headers=headers, json=body, timeout=45)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"].strip()


def send_text(phone: str, message: str):
    """Send SMS via Textbelt."""
    textbelt_key = require_env("TEXTBELT_API_KEY", TEXTBELT_API_KEY)

    url = "https://textbelt.com/text"
    payload = {"phone": phone, "message": message, "key": textbelt_key}
    response = requests.post(url, data=payload, timeout=30)
    response.raise_for_status()

    data = response.json()
    if not data.get("success"):
        raise RuntimeError(f"Textbelt failed: {data}")
    return data


def main():
    # Collect phone numbers that are set
    phones = [p for p in [FRIEND_PHONE_NUMBER, FRIEND_PHONE_NUMBER_2, FRIEND_PHONE_NUMBER_3] if p and p.strip()]
    if not phones:
        raise ValueError("No friend phone numbers set. Add FRIEND_PHONE_NUMBER env vars.")

    articles = search_ai_articles()
    message = generate_commentary(articles)

    for phone in phones:
        send_text(phone.strip(), message)

    print("✅ Sent message to:", ", ".join([p.strip() for p in phones]))
    print("Message:\n", message)


if __name__ == "__main__":
    main()
