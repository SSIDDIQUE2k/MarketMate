from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON, ForeignKey, Float, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class CampaignType(enum.Enum):
    EMAIL = "email"
    SMS = "sms"
    SOCIAL_MEDIA = "social_media"
    DISPLAY_ADS = "display_ads"
    SEARCH_ADS = "search_ads"
    CONTENT_MARKETING = "content_marketing"
    INFLUENCER = "influencer"

class CampaignStatus(enum.Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    
    # Campaign Basic Info
    name = Column(String(255), nullable=False)
    description = Column(Text)
    campaign_type = Column(Enum(CampaignType), nullable=False)
    status = Column(Enum(CampaignStatus), default=CampaignStatus.DRAFT)
    
    # Campaign Objectives
    objective = Column(String(100))  # awareness, traffic, leads, sales, etc.
    target_audience = Column(Text)
    
    # Budget and Timeline
    budget = Column(Float)
    budget_type = Column(String(20))  # total, daily, weekly, monthly
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    
    # Content
    content = Column(Text)
    subject_line = Column(String(255))  # For email campaigns
    call_to_action = Column(String(255))
    landing_page_url = Column(String(500))
    
    # Targeting
    targeting_criteria = Column(JSON)  # Age, location, interests, etc.
    audience_size = Column(Integer)
    
    # Creative Assets
    creative_assets = Column(JSON)  # List of asset IDs
    
    # Performance Metrics
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    leads_generated = Column(Integer, default=0)
    revenue_generated = Column(Float, default=0.0)
    
    # Calculated Metrics
    click_through_rate = Column(Float, default=0.0)
    conversion_rate = Column(Float, default=0.0)
    cost_per_click = Column(Float, default=0.0)
    cost_per_conversion = Column(Float, default=0.0)
    return_on_ad_spend = Column(Float, default=0.0)
    
    # Spend Tracking
    amount_spent = Column(Float, default=0.0)
    remaining_budget = Column(Float, default=0.0)
    
    # A/B Testing
    is_ab_test = Column(Boolean, default=False)
    ab_test_variants = Column(JSON)
    
    # Campaign Settings
    frequency_cap = Column(Integer)  # Max times to show to same person
    delivery_optimization = Column(String(50))  # reach, impressions, clicks, etc.
    
    # External Platform IDs
    platform_campaign_id = Column(String(100))
    platform_name = Column(String(50))  # facebook, google, etc.
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    launched_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    business = relationship("Business", back_populates="campaigns") 