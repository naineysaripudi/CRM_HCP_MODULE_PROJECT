from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.database import Base

class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_name = Column(String(255), index=True)
    date = Column(String(10))
    time = Column(String(5))
    interaction_type = Column(String(50))
    attendees = Column(String(500))
    topics_discussed = Column(Text)
    materials_shared = Column(Text)
    samples_distributed = Column(String(500))
    sentiment = Column(String(50))
    outcomes = Column(Text)
    followup = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    class Config:
        from_attributes = True
