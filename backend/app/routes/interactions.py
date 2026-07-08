from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database import get_db
from app.models.interaction import Interaction
from app.models.schemas import InteractionCreate, InteractionUpdate, InteractionResponse
from typing import List

router = APIRouter(prefix="/api/interactions", tags=["interactions"])

# GET all interactions
@router.get("", response_model=List[InteractionResponse])
def get_interactions(
    skip: int = 0,
    limit: int = 100,
    search: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Interaction)
    
    if search:
        query = query.filter(
            or_(
                Interaction.hcp_name.ilike(f"%{search}%"),
                Interaction.topics_discussed.ilike(f"%{search}%")
            )
        )
    
    interactions = query.offset(skip).limit(limit).all()
    return interactions

# GET single interaction
@router.get("/{interaction_id}", response_model=InteractionResponse)
def get_interaction(interaction_id: int, db: Session = Depends(get_db)):
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return interaction

# POST create interaction
@router.post("", response_model=InteractionResponse)
def create_interaction(interaction: InteractionCreate, db: Session = Depends(get_db)):
    db_interaction = Interaction(**interaction.dict())
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction

# PUT update interaction
@router.put("/{interaction_id}", response_model=InteractionResponse)
def update_interaction(
    interaction_id: int,
    interaction: InteractionUpdate,
    db: Session = Depends(get_db)
):
    db_interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not db_interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    
    for key, value in interaction.dict(exclude_unset=True).items():
        setattr(db_interaction, key, value)
    
    db.commit()
    db.refresh(db_interaction)
    return db_interaction

# DELETE interaction
@router.delete("/{interaction_id}")
def delete_interaction(interaction_id: int, db: Session = Depends(get_db)):
    db_interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not db_interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    
    db.delete(db_interaction)
    db.commit()
    return {"message": "Interaction deleted successfully", "id": interaction_id}

# Search interactions by doctor name
@router.get("/search/doctor")
def search_by_doctor(q: str, db: Session = Depends(get_db)):
    interactions = db.query(Interaction).filter(
        Interaction.hcp_name.ilike(f"%{q}%")
    ).all()
    return interactions
