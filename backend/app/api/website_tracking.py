from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.website_tracking import WebsiteVisitor, WebsiteEvent
from app.models.business import Business
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uuid
import json
from datetime import datetime
import geoip2.database
import user_agents

router = APIRouter()

class TrackingEvent(BaseModel):
    business_id: int
    visitor_id: Optional[str] = None
    event_type: str
    page_url: str
    page_title: Optional[str] = None
    event_data: Optional[Dict[str, Any]] = None
    duration: Optional[float] = None
    form_fields: Optional[Dict[str, Any]] = None

class LeadCaptureData(BaseModel):
    business_id: int
    visitor_id: str
    email: Optional[str] = None
    phone: Optional[str] = None
    name: Optional[str] = None
    form_fields: Optional[Dict[str, Any]] = None

@router.get("/pixel/{business_id}")
async def tracking_pixel(
    business_id: int,
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Serves a 1x1 pixel image for website tracking.
    This is loaded on client websites to track visitors.
    """
    # Check if business exists
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business or not business.is_tracking_enabled:
        raise HTTPException(status_code=404, detail="Tracking not found")
    
    # Get visitor information
    ip_address = request.client.host
    user_agent_string = request.headers.get("user-agent", "")
    referrer = request.headers.get("referer", "")
    
    # Parse user agent
    user_agent = user_agents.parse(user_agent_string)
    
    # Generate or get visitor ID
    visitor_id = request.cookies.get("visitor_id")
    if not visitor_id:
        visitor_id = str(uuid.uuid4())
        response.set_cookie("visitor_id", visitor_id, max_age=365*24*60*60)  # 1 year
    
    # Check if visitor exists
    visitor = db.query(WebsiteVisitor).filter(
        WebsiteVisitor.visitor_id == visitor_id,
        WebsiteVisitor.business_id == business_id
    ).first()
    
    if visitor:
        # Update existing visitor
        visitor.last_visit = datetime.utcnow()
        visitor.total_visits += 1
        visitor.user_agent = user_agent_string
        visitor.referrer = referrer
    else:
        # Create new visitor
        visitor = WebsiteVisitor(
            business_id=business_id,
            visitor_id=visitor_id,
            ip_address=ip_address,
            user_agent=user_agent_string,
            referrer=referrer,
            device_type=get_device_type(user_agent),
            browser=user_agent.browser.family,
            os=user_agent.os.family,
            # Geographic info would be added here with GeoIP
        )
        db.add(visitor)
    
    db.commit()
    
    # Return 1x1 transparent PNG
    pixel_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xdb\x00\x00\x00\x00IEND\xaeB`\x82'
    
    response.headers["Content-Type"] = "image/png"
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return Response(content=pixel_data, media_type="image/png")

@router.post("/track-event")
async def track_event(
    event: TrackingEvent,
    request: Request,
    db: Session = Depends(get_db)
):
    """Track specific events on the website"""
    
    # Get or create visitor
    visitor = db.query(WebsiteVisitor).filter(
        WebsiteVisitor.visitor_id == event.visitor_id,
        WebsiteVisitor.business_id == event.business_id
    ).first()
    
    if not visitor:
        # Create visitor if doesn't exist
        visitor = WebsiteVisitor(
            business_id=event.business_id,
            visitor_id=event.visitor_id,
            ip_address=request.client.host,
            user_agent=request.headers.get("user-agent", "")
        )
        db.add(visitor)
        db.commit()
    
    # Create event
    website_event = WebsiteEvent(
        visitor_id=visitor.id,
        event_type=event.event_type,
        page_url=event.page_url,
        page_title=event.page_title,
        event_data=event.event_data,
        duration=event.duration,
        form_fields=event.form_fields
    )
    
    db.add(website_event)
    
    # Update visitor metrics
    visitor.total_page_views += 1
    if event.duration:
        visitor.total_time_spent += event.duration / 60  # Convert to minutes
    
    db.commit()
    
    return {"status": "success", "event_id": website_event.id}

@router.post("/capture-lead")
async def capture_lead(
    lead_data: LeadCaptureData,
    db: Session = Depends(get_db)
):
    """Capture lead information from website forms"""
    
    # Get visitor
    visitor = db.query(WebsiteVisitor).filter(
        WebsiteVisitor.visitor_id == lead_data.visitor_id,
        WebsiteVisitor.business_id == lead_data.business_id
    ).first()
    
    if not visitor:
        raise HTTPException(status_code=404, detail="Visitor not found")
    
    # Update visitor with lead information
    if lead_data.email:
        visitor.email = lead_data.email
    if lead_data.phone:
        visitor.phone = lead_data.phone
    if lead_data.name:
        visitor.name = lead_data.name
    
    visitor.is_lead = True
    visitor.lead_converted_at = datetime.utcnow()
    
    # Calculate lead score based on behavior
    visitor.lead_score = calculate_lead_score(visitor)
    
    db.commit()
    
    return {"status": "success", "lead_id": visitor.id, "lead_score": visitor.lead_score}

@router.get("/leads/{business_id}")
async def get_website_leads(
    business_id: int,
    db: Session = Depends(get_db)
):
    """Get all leads captured from website"""
    
    leads = db.query(WebsiteVisitor).filter(
        WebsiteVisitor.business_id == business_id,
        WebsiteVisitor.is_lead == True
    ).all()
    
    return {"leads": leads}

@router.get("/visitors/{business_id}")
async def get_website_visitors(
    business_id: int,
    db: Session = Depends(get_db)
):
    """Get all website visitors with analytics"""
    
    visitors = db.query(WebsiteVisitor).filter(
        WebsiteVisitor.business_id == business_id
    ).all()
    
    return {"visitors": visitors}

@router.get("/analytics/{business_id}")
async def get_website_analytics(
    business_id: int,
    db: Session = Depends(get_db)
):
    """Get website analytics and metrics"""
    
    # Get total visitors
    total_visitors = db.query(WebsiteVisitor).filter(
        WebsiteVisitor.business_id == business_id
    ).count()
    
    # Get total leads
    total_leads = db.query(WebsiteVisitor).filter(
        WebsiteVisitor.business_id == business_id,
        WebsiteVisitor.is_lead == True
    ).count()
    
    # Calculate conversion rate
    conversion_rate = (total_leads / total_visitors * 100) if total_visitors > 0 else 0
    
    # Get top pages
    top_pages = db.query(WebsiteEvent.page_url).filter(
        WebsiteEvent.visitor.has(business_id=business_id),
        WebsiteEvent.event_type == "page_view"
    ).group_by(WebsiteEvent.page_url).limit(10).all()
    
    return {
        "total_visitors": total_visitors,
        "total_leads": total_leads,
        "conversion_rate": conversion_rate,
        "top_pages": [page[0] for page in top_pages]
    }

def get_device_type(user_agent):
    """Determine device type from user agent"""
    if user_agent.is_mobile:
        return "mobile"
    elif user_agent.is_tablet:
        return "tablet"
    else:
        return "desktop"

def calculate_lead_score(visitor: WebsiteVisitor) -> int:
    """Calculate lead score based on visitor behavior"""
    score = 0
    
    # Base score for becoming a lead
    score += 10
    
    # Points for multiple visits
    score += min(visitor.total_visits * 2, 20)
    
    # Points for time spent
    score += min(int(visitor.total_time_spent), 30)
    
    # Points for page views
    score += min(visitor.total_page_views, 25)
    
    # Points for providing contact info
    if visitor.email:
        score += 15
    if visitor.phone:
        score += 10
    if visitor.name:
        score += 5
    
    return min(score, 100)  # Cap at 100 