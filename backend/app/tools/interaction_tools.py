"""
AI Tools for HCP Interaction CRM

This module contains 5 LangGraph tools:
1. Log Interaction - Extract and save interaction from natural language
2. Edit Interaction - Update existing interaction from natural language
3. Search Interaction - Search interactions using semantic understanding
4. Generate Follow-up - Create follow-up email from interaction data
5. Summarize Interaction - Create concise summary of interaction
"""

from typing import Any, Dict, List
from sqlalchemy.orm import Session
from app.models.interaction import Interaction
from app.models.schemas import InteractionCreate, InteractionUpdate

class InteractionTools:
    """Tools for HCP interaction management"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def log_interaction(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Tool 1: Create a new interaction from extracted data
        
        Args:
            extracted_data: Dictionary with keys:
                - hcp_name: str
                - date: str
                - time: str
                - interaction_type: str
                - attendees: str
                - topics_discussed: str
                - materials_shared: str
                - samples_distributed: str
                - sentiment: str (Positive/Negative/Neutral)
                - outcomes: str
                - followup: str
        
        Returns:
            Created interaction object or error
        """
        try:
            interaction_data = InteractionCreate(**extracted_data)
            db_interaction = Interaction(**interaction_data.dict())
            self.db.add(db_interaction)
            self.db.commit()
            self.db.refresh(db_interaction)
            
            return {
                "success": True,
                "message": "Interaction logged successfully",
                "interaction_id": db_interaction.id,
                "data": {
                    "hcp_name": db_interaction.hcp_name,
                    "date": db_interaction.date,
                    "sentiment": db_interaction.sentiment
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error logging interaction: {str(e)}"
            }
    
    def edit_interaction(self, interaction_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """
        Tool 2: Update existing interaction
        
        Args:
            interaction_id: ID of interaction to update
            updates: Dictionary of fields to update
        
        Returns:
            Updated interaction or error
        """
        try:
            db_interaction = self.db.query(Interaction).filter(
                Interaction.id == interaction_id
            ).first()
            
            if not db_interaction:
                return {"success": False, "message": "Interaction not found"}
            
            # Update fields
            for key, value in updates.items():
                if hasattr(db_interaction, key) and value is not None:
                    setattr(db_interaction, key, value)
            
            self.db.commit()
            self.db.refresh(db_interaction)
            
            return {
                "success": True,
                "message": "Interaction updated successfully",
                "interaction_id": db_interaction.id
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error updating interaction: {str(e)}"
            }
    
    def search_interactions(self, query: str, field: str = "hcp_name") -> Dict[str, Any]:
        """
        Tool 3: Search interactions
        
        Args:
            query: Search query
            field: Field to search in (hcp_name, topics_discussed, etc)
        
        Returns:
            List of matching interactions
        """
        try:
            if field == "hcp_name":
                results = self.db.query(Interaction).filter(
                    Interaction.hcp_name.ilike(f"%{query}%")
                ).all()
            elif field == "topics":
                results = self.db.query(Interaction).filter(
                    Interaction.topics_discussed.ilike(f"%{query}%")
                ).all()
            else:
                results = self.db.query(Interaction).filter(
                    Interaction.hcp_name.ilike(f"%{query}%")
                ).all()
            
            return {
                "success": True,
                "message": f"Found {len(results)} interactions",
                "results": [
                    {
                        "id": r.id,
                        "hcp_name": r.hcp_name,
                        "date": r.date,
                        "sentiment": r.sentiment,
                        "topics": r.topics_discussed
                    } for r in results
                ]
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error searching interactions: {str(e)}"
            }
    
    def generate_followup(self, interaction_id: int) -> Dict[str, Any]:
        """
        Tool 4: Generate follow-up communication
        
        Args:
            interaction_id: ID of interaction to follow up on
        
        Returns:
            Generated follow-up email and suggested date
        """
        try:
            db_interaction = self.db.query(Interaction).filter(
                Interaction.id == interaction_id
            ).first()
            
            if not db_interaction:
                return {"success": False, "message": "Interaction not found"}
            
            # Generate follow-up email
            followup_email = self._generate_followup_email(db_interaction)
            
            return {
                "success": True,
                "message": "Follow-up email generated",
                "email": followup_email,
                "suggested_date": db_interaction.followup
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error generating follow-up: {str(e)}"
            }
    
    def summarize_interaction(self, interaction_id: int) -> Dict[str, Any]:
        """
        Tool 5: Summarize interaction
        
        Args:
            interaction_id: ID of interaction to summarize
        
        Returns:
            Summary and key points
        """
        try:
            db_interaction = self.db.query(Interaction).filter(
                Interaction.id == interaction_id
            ).first()
            
            if not db_interaction:
                return {"success": False, "message": "Interaction not found"}
            
            summary = self._create_summary(db_interaction)
            key_points = self._extract_key_points(db_interaction)
            
            return {
                "success": True,
                "message": "Interaction summarized",
                "summary": summary,
                "key_points": key_points
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error summarizing interaction: {str(e)}"
            }
    
    def _generate_followup_email(self, interaction: Interaction) -> str:
        """Generate professional follow-up email"""
        email = f"""Dear {interaction.hcp_name},

Thank you for taking the time to meet with me on {interaction.date}.

During our discussion, we covered the following topics:
{interaction.topics_discussed}

As discussed, I'm sending you:
{interaction.materials_shared}

Based on our conversation, the next steps are:
{interaction.outcomes}

I look forward to following up with you on {interaction.followup}.

Best regards,
Your Sales Team"""
        return email
    
    def _create_summary(self, interaction: Interaction) -> str:
        """Create concise summary of interaction"""
        sentiment_emoji = {
            "Positive": "✓",
            "Negative": "✗",
            "Neutral": "→",
            "Very Positive": "✓✓"
        }
        emoji = sentiment_emoji.get(interaction.sentiment, "•")
        
        summary = f"{emoji} {interaction.hcp_name} | {interaction.date}\n"
        summary += f"Type: {interaction.interaction_type}\n"
        summary += f"Topics: {interaction.topics_discussed}\n"
        summary += f"Sentiment: {interaction.sentiment}\n"
        summary += f"Outcomes: {interaction.outcomes}"
        
        return summary
    
    def _extract_key_points(self, interaction: Interaction) -> List[str]:
        """Extract key points from interaction"""
        return [
            f"Doctor: {interaction.hcp_name}",
            f"Type: {interaction.interaction_type}",
            f"Sentiment: {interaction.sentiment}",
            f"Materials Shared: {interaction.materials_shared}",
            f"Follow-up: {interaction.followup}"
        ]
