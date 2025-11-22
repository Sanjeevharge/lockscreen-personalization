import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from backend.db import Base  # <-- import Base from db.py, do NOT redefine

class Content(Base):
    __tablename__ = "content"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    category = Column(String, nullable=True)
    publisher = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    image = Column(String, nullable=True)
    why = Column(Text, nullable=True)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content_id = Column(Integer, ForeignKey("content.id"))
    event_type = Column(String)  # impression, like, dislike, skip
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User")
    content = relationship("Content")
