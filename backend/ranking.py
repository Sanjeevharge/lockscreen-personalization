# backend/ranking.py
import random
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.models.db_models import Content, Event

def epsilon_greedy_recommend(user_id: int, db: Session, limit: int = 10, epsilon: float = 0.2) -> List[Content]:
    """
    A simple epsilon-greedy recommender:
     - with probability epsilon: return random content (explore)
     - else: return items from categories the user liked (exploit)
     - fallback: return latest content
    """
    # get liked categories by user
    liked_q = (
        db.query(Content.category)
        .join(Event, Event.content_id == Content.id)
        .filter(Event.user_id == user_id, Event.event_type == "like")
        .distinct()
    )
    liked_categories = [r[0] for r in liked_q.all() if r[0]]

    # explore
    if random.random() < epsilon:
        # random sampling - use SQL random function (works for sqlite and postgres via SQLAlchemy func.random)
        candidates = db.query(Content).order_by(func.random()).limit(limit).all()
        return candidates

    # exploit: if user has liked categories
    if liked_categories:
        candidates = db.query(Content).filter(Content.category.in_(liked_categories)).limit(limit).all()
        if candidates:
            return candidates

    # fallback: latest content by timestamp
    return db.query(Content).order_by(Content.timestamp.desc()).limit(limit).all()
