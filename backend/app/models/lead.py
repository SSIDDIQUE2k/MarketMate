from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    
    # Contact Information
    email = Column(String(255), index=True)
    phone = Column(String(50))
    full_name = Column(String(255))
    company = Column(String(255))
    job_title = Column(String(255))
    
    # Lead Source
    source = Column(String(100))  # website, social_media, referral, etc.
    utm_source = Column(String(100))
    utm_medium = Column(String(100))
    utm_campaign = Column(String(100))
    referrer_url = Column(String(500))
    
    # Lead Status
    status = Column(String(50), default="new")  # new, contacted, qualified, proposal, negotiation, closed, lost
    stage = Column(String(50))  # awareness, consideration, decision
    
    # Lead Scoring
    lead_score = Column(Integer, default=0)
    quality_score = Column(Float, default=0.0)  # 0-100
    
    # Engagement Data
    total_page_views = Column(Integer, default=0)
    total_time_spent = Column(Float, default=0.0)  # in minutes
    last_activity = Column(DateTime(timezone=True))
    
    # Custom Fields
    custom_fields = Column(JSON)  # Flexible storage for additional data
    tags = Column(JSON)  # List of tags
    notes = Column(Text)
    
    # Assignment
    assigned_to = Column(Integer)  # User ID
    
    # Lead Value
    estimated_value = Column(Float)
    actual_value = Column(Float)
    
    # Communication Preferences
    email_opt_in = Column(Boolean, default=True)
    sms_opt_in = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    first_contact_date = Column(DateTime(timezone=True))
    last_contact_date = Column(DateTime(timezone=True))
    converted_at = Column(DateTime(timezone=True))
    
    # Relationships
    business = relationship("Business", back_populates="leads") 