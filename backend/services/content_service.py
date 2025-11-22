# backend/services/content_service.py
import os

import requests
from dotenv import load_dotenv
from models.db_models import Content
from sqlalchemy.orm import Session

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


NEWS_API_KEY = os.getenv("NEWS_API_KEY")
UNSPLASH_KEY = os.getenv("UNSPLASH_KEY")


def fetch_news():
    """
    Fetch articles from NewsAPI (top headlines). Requires NEWS_API_KEY env var.
    Returns a list of dicts with keys: title, category, publisher, image, why
    """
    if not NEWS_API_KEY:
        raise RuntimeError("NEWS_API_KEY not set in environment")

    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"
    resp = requests.get(url)
    resp.raise_for_status()
    articles = resp.json().get("articles", [])
    results = []
    for a in articles:
        title = a.get("title")
        publisher = a.get("source", {}).get("name", "Unknown")
        image = a.get("urlToImage")
        # placeholder "why" if none
        why = a.get("description") or "Recommended for you"
        results.append(
            {
                "title": title,
                "category": "General",
                "publisher": publisher,
                "image": image,
                "why": why,
            }
        )
    return results


def save_content(db: Session, content_list):
    for item in content_list:
        # optional: check duplicates by title/publisher
        content = Content(
            title=item.get("title"),
            category=item.get("category"),
            publisher=item.get("publisher"),
            image=item.get("image"),
            why=item.get("why"),
        )
        db.add(content)
    db.commit()
