from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class WebsiteVisitor(Base):
    __tablename__ = "website_visitors"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    
    # Visitor Identification
    visitor_id = Column(String(100), unique=True, index=True)  # Unique tracking ID
    ip_address = Column(String(45))
    user_agent = Column(Text)
    
    # Geographic Information
    country = Column(String(100))
    city = Column(String(100))
    region = Column(String(100))
    
    # Traffic Source
    referrer = Column(String(500))
    utm_source = Column(String(100))
    utm_medium = Column(String(100))
    utm_campaign = Column(String(100))
    utm_content = Column(String(100))
    utm_term = Column(String(100))
    
    # Device Information
    device_type = Column(String(50))  # desktop, mobile, tablet
    browser = Column(String(100))
    os = Column(String(100))
    screen_resolution = Column(String(20))
    
    # Behavior Metrics
    first_visit = Column(DateTime(timezone=True), server_default=func.now())
    last_visit = Column(DateTime(timezone=True), onupdate=func.now())
    total_visits = Column(Integer, default=1)
    total_page_views = Column(Integer, default=0)
    total_time_spent = Column(Float, default=0.0)  # in minutes
    
    # Lead Status
    is_lead = Column(Boolean, default=False)
    lead_score = Column(Integer, default=0)
    lead_converted_at = Column(DateTime(timezone=True))
    
    # Contact Information (if captured)
    email = Column(String(255))
    phone = Column(String(50))
    name = Column(String(255))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    business = relationship("Business", back_populates="website_visitors")
    events = relationship("WebsiteEvent", back_populates="visitor")

class WebsiteEvent(Base):
    __tablename__ = "website_events"

    id = Column(Integer, primary_key=True, index=True)
    visitor_id = Column(Integer, ForeignKey("website_visitors.id"), nullable=False)
    
    # Event Information
    event_type = Column(String(50))  # page_view, form_submit, button_click, download, etc.
    page_url = Column(String(500))
    page_title = Column(String(255))
    
    # Event Details
    event_data = Column(JSON)  # Additional event-specific data
    duration = Column(Float)  # Time spent on page in seconds
    
    # Form Data (if applicable)
    form_fields = Column(JSON)  # Captured form data
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    visitor = relationship("WebsiteVisitor", back_populates="events") 