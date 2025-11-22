from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import random
from datetime import datetime, timedelta
from models import db_models  # ensures Content & Event are registered

# ✅ New imports
import os
from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

from db import SessionLocal, init_db, Base, engine
from models.db_models import Content, Event
from services.content_service import fetch_news, save_content
from services.event_service import log_event

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Lockscreen Personalization API")

# Allow local development origins (adjust as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Then mount static folder
app.mount("/static", StaticFiles(directory="static"), name="static")


# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    init_db()
    from models import db_models  # <-- ensure models are registered
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if db.query(Content).count() == 0:
            print("⚡ No content found in DB, fetching fresh news...")
            articles = fetch_news()
            save_content(db, articles)
            print(f"✅ Saved {len(articles)} articles to DB")
    finally:
        db.close()


@app.get("/")
def root():
    # ✅ Example check: confirm environment variables loaded
    return {
        "message": "Backend is alive! 🚀",
        "news_api_key_loaded": os.getenv("NEWS_API_KEY") is not None,
        "unsplash_key_loaded": os.getenv("UNSPLASH_KEY") is not None,
    }

# --------------------------
# 🔹 Existing Endpoints
# --------------------------

@app.get("/feed")
def get_feed(db: Session = Depends(get_db)):
    content = db.query(Content).all()
    return {"feed": [c.__dict__ for c in content]}


@app.post("/fetch_news")
def update_content(db: Session = Depends(get_db)):
    articles = fetch_news()
    save_content(db, articles)
    return {"status": "ok", "fetched": len(articles)}


from pydantic import BaseModel

class EventIn(BaseModel):
    user_id: int
    content_id: int
    event_type: str

@app.post("/event")
def log_user_event(event: EventIn, db: Session = Depends(get_db)):
    e = log_event(db, event.user_id, event.content_id, event.event_type)
    return {"event": e.id, "status": "logged"}




# --------------------------
# 🔹 Phase 3: Recommendations
# --------------------------

# Candidate Generation (Rule-based)
@app.get("/recommendations")
def get_recommendations(limit: int = 10, db: Session = Depends(get_db)):
    recent_cutoff = datetime.utcnow() - timedelta(days=7)
    recent_content = db.query(Content).filter(Content.timestamp >= recent_cutoff).all()

    if len(recent_content) < limit:
        recent_content = db.query(Content).all()

    sampled = random.sample(recent_content, min(limit, len(recent_content)))
    return [
        {
            "id": c.id,
            "title": c.title,
            "category": c.category,
            "publisher": c.publisher,
            "timestamp": c.timestamp,
            "image": c.image,
            "why": c.why,
        }
        for c in sampled
    ]


# Ranking Baseline (epsilon-greedy)
@app.get("/recommendations/{user_id}")
def get_ranked_recommendations(user_id: int, limit: int = 10, epsilon: float = 0.2, db: Session = Depends(get_db)):
    liked_categories = (
        db.query(.Content.category)
        .join(Event, Event.content_id == Content.id)
        .filter(Event.user_id == user_id, Event.event_type == "like")
        .all()
    )
    liked_categories = [c[0] for c in liked_categories]

    if random.random() < epsilon or not liked_categories:
        candidates = (
            db.query(Content)
            .order_by(Content.timestamp.desc())
            .limit(limit)
            .all()
        )
    else:
        candidates = (
            db.query(Content)
            .filter(Content.category.in_(liked_categories))
            .order_by(Content.timestamp.desc())
            .limit(limit)
            .all()
        )

    return [
        {
            "id": c.id,
            "title": c.title,
            "category": c.category,
            "publisher": c.publisher,
            "timestamp": c.timestamp,
            "image": c.image,
            "why": c.why,
        }
        for c in candidates
    ]
