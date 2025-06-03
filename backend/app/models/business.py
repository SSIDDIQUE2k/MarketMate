from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    website_url = Column(String(500))
    logo_url = Column(String(500))
    industry = Column(String(100))
    
    # Contact Information
    email = Column(String(255))
    phone = Column(String(50))
    address = Column(Text)
    
    # Business Settings
    timezone = Column(String(50), default="UTC")
    currency = Column(String(10), default="USD")
    
    # Website Tracking
    tracking_pixel_id = Column(String(100), unique=True)
    is_tracking_enabled = Column(Boolean, default=True)
    
    # Social Media Settings
    social_media_config = Column(JSON)  # Store API keys and settings
    
    # AI Settings
    ai_voice_tone = Column(String(50), default="professional")
    brand_colors = Column(JSON)  # Store brand color palette
    brand_guidelines = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    leads = relationship("Lead", back_populates="business")
    campaigns = relationship("Campaign", back_populates="business")
    website_visitors = relationship("WebsiteVisitor", back_populates="business")
    social_media_accounts = relationship("SocialMediaAccount", back_populates="business")
    content_assets = relationship("ContentAsset", back_populates="business")
    email_campaigns = relationship("EmailCampaign", back_populates="business")
    sms_campaigns = relationship("SMSCampaign", back_populates="business") 