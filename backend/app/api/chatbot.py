from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
import openai
from datetime import datetime

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: datetime = datetime.now()

class ChatSession(BaseModel):
    session_id: str
    messages: List[ChatMessage]
    user_id: Optional[str] = None
    context: Optional[dict] = None

class ChatResponse(BaseModel):
    message: str
    session_id: str
    suggested_actions: List[str]
    confidence_score: float

# Initialize conversation history
conversation_history = {}

@router.post("/chat", response_model=ChatResponse)
async def chat_with_bot(session: ChatSession):
    """
    Handle a chat interaction with the AI chatbot
    """
    try:
        # Get or create conversation history
        if session.session_id not in conversation_history:
            conversation_history[session.session_id] = []

        # Add new message to history
        conversation_history[session.session_id].extend(session.messages)

        # Prepare conversation for OpenAI
        messages = [
            {"role": "system", "content": "You are a helpful marketing assistant. Your goal is to help users with their marketing needs, qualify leads, and provide relevant information."},
            *[{"role": msg.role, "content": msg.content} for msg in conversation_history[session.session_id]]
        ]

        # Get AI response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=150
        )

        ai_message = response.choices[0].message.content
        confidence_score = response.choices[0].finish_reason == "stop"

        # Generate suggested actions based on the conversation
        suggested_actions = generate_suggested_actions(ai_message, session.context)

        # Add AI response to history
        conversation_history[session.session_id].append(
            ChatMessage(role="assistant", content=ai_message)
        )

        return ChatResponse(
            message=ai_message,
            session_id=session.session_id,
            suggested_actions=suggested_actions,
            confidence_score=float(confidence_score)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def generate_suggested_actions(message: str, context: Optional[dict]) -> List[str]:
    """
    Generate suggested next actions based on the conversation
    """
    # Use OpenAI to analyze the conversation and suggest actions
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Based on the following message, suggest 3 relevant next actions for a marketing assistant."},
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=100
        )
        
        suggestions = response.choices[0].message.content.split("\n")
        return [s.strip() for s in suggestions if s.strip()]
    except:
        return [
            "Schedule a call",
            "Send more information",
            "Share case studies"
        ]

@router.get("/sessions/{session_id}", response_model=ChatSession)
async def get_chat_session(session_id: str):
    """
    Get chat history for a specific session
    """
    if session_id not in conversation_history:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return ChatSession(
        session_id=session_id,
        messages=conversation_history[session_id]
    )

@router.delete("/sessions/{session_id}")
async def delete_chat_session(session_id: str):
    """
    Delete a chat session
    """
    if session_id in conversation_history:
        del conversation_history[session_id]
    return {"status": "success"} 