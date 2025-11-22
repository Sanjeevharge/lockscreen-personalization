from sqlalchemy.orm import Session
from backend.models.db_models import Event

def log_event(db: Session, user_id: int, content_id: int, event_type: str):
    event = Event(user_id=user_id, content_id=content_id, event_type=event_type)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
