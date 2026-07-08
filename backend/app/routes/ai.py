from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.interaction import Interaction
from app.agents.langgraph_agent import create_agent

router = APIRouter(prefix="/api/ai", tags=["ai"])

# Schemas for AI operations
class LogInteractionRequest(BaseModel):
    text: str

class EditInteractionRequest(BaseModel):
    text: str

class SearchRequest(BaseModel):
    query: str

# Tool 1: Log Interaction
@router.post("/log-interaction")
def log_interaction_ai(request: LogInteractionRequest, db: Session = Depends(get_db)):
    """
    AI processes natural language text and automatically logs interaction
    
    Example input:
    "Met Dr. Sharma today. Discussed Diabetes medicine. Doctor was interested. 
     Shared brochure. Need follow-up after 2 weeks."
    
    Returns: Created interaction record
    """
    agent = create_agent(db)
    result = agent.process(request.text)
    return result

# Tool 2: Edit Interaction
@router.post("/edit-interaction/{interaction_id}")
def edit_interaction_ai(
    interaction_id: int,
    request: EditInteractionRequest,
    db: Session = Depends(get_db)
):
    """
    AI processes natural language text and updates interaction fields
    
    Example input:
    "Change follow-up to next Monday"
    
    Returns: Updated interaction record
    """
    agent = create_agent(db)
    result = agent.process(request.text, interaction_id=interaction_id)
    return result

# Tool 3: Search Interaction
@router.post("/search")
def search_ai(request: SearchRequest, db: Session = Depends(get_db)):
    """
    AI-powered search across interactions
    
    Example input:
    "Show all meetings with Dr Sharma"
    
    Returns: List of matching interactions
    """
    agent = create_agent(db)
    result = agent.process(request.query)
    return result

# Tool 4: Generate Follow-up
@router.post("/generate-followup/{interaction_id}")
def generate_followup(interaction_id: int, db: Session = Depends(get_db)):
    """
    Generate follow-up email/message based on interaction
    
    Returns: Generated follow-up email and suggested date
    """
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    
    agent = create_agent(db)
    result = agent.process("Generate follow-up", interaction_id=interaction_id)
    return result

# Tool 5: Summarize Interaction
@router.get("/summarize/{interaction_id}")
def summarize_interaction(interaction_id: int, db: Session = Depends(get_db)):
    """
    Summarize an interaction using LLM
    
    Returns: Summary and key points
    """
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    
    agent = create_agent(db)
    result = agent.process("Summarize this interaction", interaction_id=interaction_id)
    return result
