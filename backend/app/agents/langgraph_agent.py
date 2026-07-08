"""
LangGraph Agent for HCP Interaction CRM - Phase 7: Groq LLM Integration

This agent orchestrates the following workflow:
1. User Chat Input -> 2. Groq LLM Understanding -> 3. Intent Detection
4. Tool Selection -> 5. Tool Execution -> 6. Database Update -> 7. Response

The agent uses Groq LLM for semantic understanding and field extraction.
Groq provides fast, intelligent processing for HCP interactions.

Phase 7 Features:
- Groq LLM-based intent detection (no more pattern matching)
- Intelligent field extraction using semantic understanding
- Natural language processing for all 5 tools
- Context-aware responses
"""

import json
import os
import logging
from typing import Any, Dict, List, TypedDict
from enum import Enum
from datetime import datetime
from sqlalchemy.orm import Session
from app.tools.interaction_tools import InteractionTools
from config import GROQ_API_KEY, GROQ_MODEL

# Setup logging
logger = logging.getLogger(__name__)

try:
    from groq import Groq
except ImportError:
    Groq = None
    logger.error("Groq package not installed. Install with: pip install groq")

# Define state structure
class AgentState(TypedDict):
    """State passed through agent graph"""
    user_input: str
    intent: str
    tool_to_use: str
    extracted_data: Dict[str, Any]
    tool_result: Dict[str, Any]
    response: str
    interaction_id: int | None

class Intent(Enum):
    """Supported intents"""
    LOG_INTERACTION = "log_interaction"
    EDIT_INTERACTION = "edit_interaction"
    SEARCH_INTERACTION = "search_interaction"
    GENERATE_FOLLOWUP = "generate_followup"
    SUMMARIZE_INTERACTION = "summarize_interaction"
    UNKNOWN = "unknown"

class HCPInteractionAgent:
    """
    LangGraph-based agent for HCP interaction management with Groq LLM Integration
    
    Implements 5 tools:
    1. Log Interaction - Save interaction from natural language (LLM-powered)
    2. Edit Interaction - Update interaction from natural language (LLM-powered)
    3. Search Interaction - Find interactions (semantic search)
    4. Generate Follow-up - Create follow-up communication (LLM-generated)
    5. Summarize Interaction - Summarize interaction details (LLM-summarized)
    
    Phase 7 Enhancement:
    - Uses Groq LLM for intelligent processing
    - Semantic understanding replaces pattern matching
    - Field extraction based on natural language
    """
    
    def __init__(self, db: Session, llm_provider=None):
        self.db = db
        self.tools = InteractionTools(db)
        
        # Initialize Groq client
        if GROQ_API_KEY and GROQ_API_KEY != 'your_groq_api_key_here':
            try:
                self.groq_client = Groq(api_key=GROQ_API_KEY)
                self.llm_available = True
                logger.info(f"✓ Groq LLM initialized successfully (Model: {GROQ_MODEL})")
            except Exception as e:
                logger.error(f"✗ Failed to initialize Groq: {str(e)}")
                self.groq_client = None
                self.llm_available = False
        else:
            logger.warning("⚠ GROQ_API_KEY not configured. Set it in .env file for AI features.")
            self.groq_client = None
            self.llm_available = False
        
        self.groq_model = GROQ_MODEL
    
    def detect_intent(self, user_input: str) -> Intent:
        """
        Phase 7: Groq-based intent detection
        Uses LLM to semantically understand user intent
        
        Args:
            user_input: User's natural language input
            
        Returns:
            Detected Intent enum
        """
        if not self.llm_available or not self.groq_client:
            # Fallback to pattern matching if LLM not available
            return self._detect_intent_pattern(user_input)
        
        try:
            prompt = f"""You are an intent detection expert for a CRM system managing Healthcare Professional (HCP) interactions.

Analyze the following user input and determine the intent. Respond ONLY with one of these exact values:
- log_interaction (user wants to record a new HCP meeting/interaction)
- edit_interaction (user wants to modify an existing interaction)
- search_interaction (user wants to find/search interactions)
- generate_followup (user wants to create a follow-up communication)
- summarize_interaction (user wants a summary of an interaction)
- unknown (none of the above)

User input: "{user_input}"

Intent:"""

            message = self.groq_client.messages.create(
                model=self.groq_model,
                max_tokens=50,
                messages=[{"role": "user", "content": prompt}]
            )
            
            intent_text = message.content[0].text.strip().lower()
            
            # Map response to Intent enum
            intent_map = {
                "log_interaction": Intent.LOG_INTERACTION,
                "edit_interaction": Intent.EDIT_INTERACTION,
                "search_interaction": Intent.SEARCH_INTERACTION,
                "generate_followup": Intent.GENERATE_FOLLOWUP,
                "summarize_interaction": Intent.SUMMARIZE_INTERACTION,
                "unknown": Intent.UNKNOWN
            }
            
            for key, value in intent_map.items():
                if key in intent_text:
                    logger.info(f"✓ Intent detected: {value.value}")
                    return value
            
            return Intent.UNKNOWN
            
        except Exception as e:
            logger.error(f"✗ Error in Groq intent detection: {str(e)}")
            # Fallback to pattern matching
            return self._detect_intent_pattern(user_input)
    
    def _detect_intent_pattern(self, user_input: str) -> Intent:
        """Fallback pattern-based intent detection"""
        user_input_lower = user_input.lower()
        
        if any(word in user_input_lower for word in ["met", "met with", "discussed", "talked", "called", "spoke"]):
            if any(word in user_input_lower for word in ["change", "update", "edit", "modify"]):
                return Intent.EDIT_INTERACTION
            return Intent.LOG_INTERACTION
        
        elif any(word in user_input_lower for word in ["find", "show", "search", "get", "list", "find all"]):
            return Intent.SEARCH_INTERACTION
        
        elif any(word in user_input_lower for word in ["generate", "create", "write", "followup", "follow-up", "email"]):
            return Intent.GENERATE_FOLLOWUP
        
        elif any(word in user_input_lower for word in ["summarize", "summary", "recap", "brief"]):
            return Intent.SUMMARIZE_INTERACTION
        
        return Intent.UNKNOWN
    
    def extract_fields(self, user_input: str, intent: Intent) -> Dict[str, Any]:
        """
        Phase 7: Groq-based field extraction
        Uses LLM to intelligently extract structured data from natural language
        
        Args:
            user_input: User's natural language input
            intent: Detected intent
            
        Returns:
            Dictionary with extracted fields
        """
        if not self.llm_available or not self.groq_client:
            # Fallback to basic extraction
            return self._extract_fields_basic(user_input, intent)
        
        try:
            prompt = f"""You are an expert at extracting structured information from healthcare conversations.

Extract information from the following HCP interaction text and return ONLY valid JSON (no other text).
Fill in available fields. Leave empty strings for unknown fields.

Fields to extract:
- hcp_name: Name of the healthcare professional
- date: Date of interaction (format: YYYY-MM-DD if possible)
- time: Time of interaction (format: HH:MM if possible)
- interaction_type: Type (e.g., "Meeting", "Call", "Email", "Visit")
- attendees: Other people present
- topics_discussed: What was discussed
- materials_shared: Materials/brochures shared
- samples_distributed: Any samples given
- sentiment: Overall sentiment (Positive, Negative, Neutral, Very Positive)
- outcomes: Results/outcomes of interaction
- followup: Suggested follow-up date/action

User text: "{user_input}"

Return ONLY JSON (no markdown, no explanation):"""

            message = self.groq_client.messages.create(
                model=self.groq_model,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text.strip()
            
            # Parse JSON from response
            try:
                extracted_data = json.loads(response_text)
                logger.info(f"✓ Fields extracted for HCP: {extracted_data.get('hcp_name', 'Unknown')}")
                return extracted_data
            except json.JSONDecodeError:
                logger.warning(f"⚠ Could not parse LLM response as JSON, using fallback")
                return self._extract_fields_basic(user_input, intent)
            
        except Exception as e:
            logger.error(f"✗ Error in Groq field extraction: {str(e)}")
            # Fallback to basic extraction
            return self._extract_fields_basic(user_input, intent)
    
    def _extract_fields_basic(self, user_input: str, intent: Intent) -> Dict[str, Any]:
        """Fallback basic field extraction"""
        extraction = {
            "hcp_name": "",
            "date": "",
            "time": "",
            "interaction_type": "Meeting",
            "attendees": "",
            "topics_discussed": user_input,
            "materials_shared": "",
            "samples_distributed": "",
            "sentiment": "Neutral",
            "outcomes": "",
            "followup": ""
        }
        return extraction
    
    def select_tool(self, intent: Intent) -> str:
        """Select appropriate tool based on intent"""
        tool_map = {
            Intent.LOG_INTERACTION: "log_interaction",
            Intent.EDIT_INTERACTION: "edit_interaction",
            Intent.SEARCH_INTERACTION: "search_interactions",
            Intent.GENERATE_FOLLOWUP: "generate_followup",
            Intent.SUMMARIZE_INTERACTION: "summarize_interaction",
            Intent.UNKNOWN: "none"
        }
        return tool_map.get(intent, "none")
    
    def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Execute selected tool"""
        if tool_name == "log_interaction":
            return self.tools.log_interaction(kwargs.get("data", {}))
        
        elif tool_name == "edit_interaction":
            return self.tools.edit_interaction(
                kwargs.get("interaction_id"),
                kwargs.get("updates", {})
            )
        
        elif tool_name == "search_interactions":
            return self.tools.search_interactions(
                kwargs.get("query", ""),
                kwargs.get("field", "hcp_name")
            )
        
        elif tool_name == "generate_followup":
            # Phase 7: Use Groq for follow-up generation
            return self._generate_followup_with_groq(kwargs.get("interaction_id"))
        
        elif tool_name == "summarize_interaction":
            # Phase 7: Use Groq for summarization
            return self._summarize_with_groq(kwargs.get("interaction_id"))
        
        else:
            return {"success": False, "message": "Tool not found"}
    
    def _generate_followup_with_groq(self, interaction_id: int) -> Dict[str, Any]:
        """
        Phase 7: Groq-powered follow-up generation
        Generate professional follow-up email using LLM
        """
        try:
            interaction = self.db.query(
                __import__('app.models.interaction', fromlist=['Interaction']).Interaction
            ).filter(
                __import__('app.models.interaction', fromlist=['Interaction']).Interaction.id == interaction_id
            ).first()
            
            if not interaction:
                return {"success": False, "message": "Interaction not found"}
            
            if not self.llm_available or not self.groq_client:
                # Fallback to basic follow-up
                return self.tools.generate_followup(interaction_id)
            
            prompt = f"""Generate a professional, personalized follow-up email based on this HCP interaction:

HCP Name: {interaction.hcp_name}
Type: {interaction.interaction_type}
Topics Discussed: {interaction.topics_discussed}
Materials Shared: {interaction.materials_shared}
Outcomes: {interaction.outcomes}
Sentiment: {interaction.sentiment}
Follow-up Date: {interaction.followup}

Generate a brief, professional follow-up email that:
1. Thanks them for the meeting
2. Summarizes key discussion points
3. Highlights next steps
4. Includes follow-up date

Email:"""

            message = self.groq_client.messages.create(
                model=self.groq_model,
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            
            email = message.content[0].text.strip()
            
            return {
                "success": True,
                "message": "Follow-up email generated with Groq AI",
                "email": email,
                "suggested_date": interaction.followup
            }
        except Exception as e:
            logger.error(f"✗ Error generating follow-up with Groq: {str(e)}")
            return self.tools.generate_followup(interaction_id)
    
    def _summarize_with_groq(self, interaction_id: int) -> Dict[str, Any]:
        """
        Phase 7: Groq-powered summarization
        Generate intelligent summary using LLM
        """
        try:
            interaction = self.db.query(
                __import__('app.models.interaction', fromlist=['Interaction']).Interaction
            ).filter(
                __import__('app.models.interaction', fromlist=['Interaction']).Interaction.id == interaction_id
            ).first()
            
            if not interaction:
                return {"success": False, "message": "Interaction not found"}
            
            if not self.llm_available or not self.groq_client:
                # Fallback to basic summary
                return self.tools.summarize_interaction(interaction_id)
            
            prompt = f"""Create a concise, professional summary of this HCP interaction:

HCP Name: {interaction.hcp_name}
Date: {interaction.date}
Type: {interaction.interaction_type}
Attendees: {interaction.attendees}
Topics: {interaction.topics_discussed}
Materials Shared: {interaction.materials_shared}
Samples: {interaction.samples_distributed}
Sentiment: {interaction.sentiment}
Outcomes: {interaction.outcomes}
Follow-up: {interaction.followup}

Provide a 2-3 sentence summary highlighting the most important points and next steps.

Summary:"""

            message = self.groq_client.messages.create(
                model=self.groq_model,
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )
            
            summary = message.content[0].text.strip()
            
            return {
                "success": True,
                "message": "Interaction summarized with Groq AI",
                "summary": summary,
                "key_points": [
                    f"Type: {interaction.interaction_type}",
                    f"Sentiment: {interaction.sentiment}",
                    f"Topics: {interaction.topics_discussed[:100]}...",
                    f"Next Steps: {interaction.outcomes[:100]}..."
                ]
            }
        except Exception as e:
            logger.error(f"✗ Error summarizing with Groq: {str(e)}")
            return self.tools.summarize_interaction(interaction_id)
    
    def process(self, user_input: str, interaction_id: int = None) -> Dict[str, Any]:
        """
        Phase 7: Main agent processing function with Groq LLM
        
        Workflow:
        1. Detect intent (Groq-powered)
        2. Extract fields (Groq-powered)
        3. Select tool
        4. Execute tool
        5. Return response
        """
        
        logger.info(f"🔄 Processing user input: '{user_input[:60]}...'")
        
        # Step 1: Detect Intent (Groq LLM)
        intent = self.detect_intent(user_input)
        
        if intent == Intent.UNKNOWN:
            return {
                "success": False,
                "message": "I couldn't understand your request. Try:\n• 'Met Dr. Sharma today, discussed diabetes'\n• 'Search for interactions with Dr. Smith'\n• 'Generate follow-up for the last meeting'\n• 'Summarize my interaction'",
                "intent": intent.value,
                "using_groq": self.llm_available
            }
        
        # Step 2: Extract Fields (Groq LLM)
        extracted_data = self.extract_fields(user_input, intent)
        
        # Step 3: Select Tool
        tool_name = self.select_tool(intent)
        
        # Step 4: Execute Tool
        if intent == Intent.LOG_INTERACTION:
            tool_result = self.execute_tool("log_interaction", data=extracted_data)
        
        elif intent == Intent.EDIT_INTERACTION:
            tool_result = self.execute_tool(
                "edit_interaction",
                interaction_id=interaction_id,
                updates=extracted_data
            )
        
        elif intent == Intent.SEARCH_INTERACTION:
            tool_result = self.execute_tool(
                "search_interactions",
                query=user_input,
                field="hcp_name"
            )
        
        elif intent == Intent.GENERATE_FOLLOWUP:
            tool_result = self.execute_tool(
                "generate_followup",
                interaction_id=interaction_id
            )
        
        elif intent == Intent.SUMMARIZE_INTERACTION:
            tool_result = self.execute_tool(
                "summarize_interaction",
                interaction_id=interaction_id
            )
        
        else:
            tool_result = {"success": False, "message": "Unknown intent"}
        
        # Step 5: Return Response
        return {
            "success": tool_result.get("success", False),
            "intent": intent.value,
            "tool_used": tool_name,
            "message": tool_result.get("message", ""),
            "data": tool_result,
            "using_groq": self.llm_available,
            "model": GROQ_MODEL if self.llm_available else "fallback_patterns"
        }


def create_agent(db: Session, llm_provider=None) -> HCPInteractionAgent:
    """
    Phase 7: Factory function to create agent instance
    Automatically initializes Groq LLM from environment variables
    
    Args:
        db: SQLAlchemy database session
        llm_provider: Optional custom LLM provider (for testing)
        
    Returns:
        Configured HCPInteractionAgent instance
    """
    return HCPInteractionAgent(db, llm_provider)

