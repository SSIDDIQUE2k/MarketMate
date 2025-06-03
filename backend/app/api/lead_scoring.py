from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel
import openai
import numpy as np
from datetime import datetime

router = APIRouter()

class Lead(BaseModel):
    id: str
    name: str
    email: str
    company: Optional[str] = None
    interactions: List[dict]
    last_contact: datetime
    engagement_score: Optional[float] = None

class LeadScore(BaseModel):
    lead_id: str
    score: float
    factors: List[str]
    recommendations: List[str]

def analyze_lead_behavior(interactions: List[dict]) -> float:
    """
    Analyze lead behavior patterns using AI
    """
    # Convert interactions to a format suitable for analysis
    interaction_text = "\n".join([f"{i['type']}: {i['description']}" for i in interactions])
    
    # Use OpenAI to analyze the interactions
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Analyze the following lead interactions and provide a score from 0-100."},
            {"role": "user", "content": interaction_text}
        ]
    )
    
    # Extract score from AI response
    try:
        score = float(response.choices[0].message.content)
        return min(max(score, 0), 100)  # Ensure score is between 0 and 100
    except:
        return 50.0  # Default score if parsing fails

@router.post("/score", response_model=LeadScore)
async def score_lead(lead: Lead):
    """
    Score a lead based on their behavior and interactions
    """
    try:
        # Calculate engagement score
        engagement_score = analyze_lead_behavior(lead.interactions)
        
        # Generate recommendations
        recommendations = generate_recommendations(lead, engagement_score)
        
        return LeadScore(
            lead_id=lead.id,
            score=engagement_score,
            factors=[
                "Email engagement",
                "Website visits",
                "Content interaction",
                "Social media engagement"
            ],
            recommendations=recommendations
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def generate_recommendations(lead: Lead, score: float) -> List[str]:
    """
    Generate personalized recommendations based on lead score
    """
    if score >= 80:
        return [
            "Schedule a sales call",
            "Send personalized product demo",
            "Share case studies"
        ]
    elif score >= 50:
        return [
            "Send targeted content",
            "Invite to webinar",
            "Share industry insights"
        ]
    else:
        return [
            "Send educational content",
            "Share blog posts",
            "Invite to newsletter"
        ]

@router.get("/leads", response_model=List[Lead])
async def get_leads():
    """
    Get all leads with their scores
    """
    # This would typically fetch from a database
    return []

@router.get("/leads/{lead_id}", response_model=Lead)
async def get_lead(lead_id: str):
    """
    Get a specific lead by ID
    """
    # This would typically fetch from a database
    raise HTTPException(status_code=404, detail="Lead not found") 