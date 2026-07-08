from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InteractionCreate(BaseModel):
    hcp_name: str
    date: str
    time: str
    interaction_type: str
    attendees: str
    topics_discussed: str
    materials_shared: str
    samples_distributed: str
    sentiment: str
    outcomes: str
    followup: str

class InteractionUpdate(BaseModel):
    hcp_name: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    interaction_type: Optional[str] = None
    attendees: Optional[str] = None
    topics_discussed: Optional[str] = None
    materials_shared: Optional[str] = None
    samples_distributed: Optional[str] = None
    sentiment: Optional[str] = None
    outcomes: Optional[str] = None
    followup: Optional[str] = None

class InteractionResponse(BaseModel):
    id: int
    hcp_name: str
    date: str
    time: str
    interaction_type: str
    attendees: str
    topics_discussed: str
    materials_shared: str
    samples_distributed: str
    sentiment: str
    outcomes: str
    followup: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
