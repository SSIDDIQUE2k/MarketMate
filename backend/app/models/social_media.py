from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON, ForeignKey, Float, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class PlatformType(enum.Enum):
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    WHATSAPP = "whatsapp"
    MESSENGER = "messenger"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    TIKTOK = "tiktok"

class AdStatus(enum.Enum):
    DRAFT = "draft"
    PENDING = "pending"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    REJECTED = "rejected"

class SocialMediaAccount(Base):
    __tablename__ = "social_media_accounts"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    
    # Platform Information
    platform = Column(Enum(PlatformType), nullable=False)
    account_id = Column(String(100))  # Platform-specific account ID
    account_name = Column(String(255))
    username = Column(String(100))
    
    # Authentication
    access_token = Column(Text)  # Encrypted access token
    refresh_token = Column(Text)  # Encrypted refresh token
    token_expires_at = Column(DateTime(timezone=True))
    
    # Account Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    last_sync = Column(DateTime(timezone=True))
    
    # Account Metrics
    followers_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    posts_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    business = relationship("Business", back_populates="social_media_accounts")
    posts = relationship("SocialMediaPost", back_populates="account")
    ad_campaigns = relationship("AdCampaign", back_populates="account")

class SocialMediaPost(Base):
    __tablename__ = "social_media_posts"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("social_media_accounts.id"), nullable=False)
    
    # Post Content
    content = Column(Text)
    hashtags = Column(JSON)  # List of hashtags
    mentions = Column(JSON)  # List of mentions
    
    # Media
    media_urls = Column(JSON)  # List of image/video URLs
    media_type = Column(String(20))  # photo, video, carousel, story
    
    # Scheduling
    scheduled_for = Column(DateTime(timezone=True))
    published_at = Column(DateTime(timezone=True))
    is_published = Column(Boolean, default=False)
    
    # Platform-specific IDs
    platform_post_id = Column(String(100))  # ID from the social platform
    
    # Engagement Metrics
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    reach = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    account = relationship("SocialMediaAccount", back_populates="posts")

class AdCampaign(Base):
    __tablename__ = "ad_campaigns"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("social_media_accounts.id"), nullable=False)
    
    # Campaign Information
    name = Column(String(255), nullable=False)
    description = Column(Text)
    objective = Column(String(50))  # awareness, traffic, engagement, conversions, etc.
    
    # Targeting
    target_audience = Column(JSON)  # Age, gender, interests, location, etc.
    budget_type = Column(String(20))  # daily, lifetime
    budget_amount = Column(Float)
    bid_strategy = Column(String(50))
    
    # Creative Content
    ad_creative = Column(JSON)  # Text, images, videos, CTAs
    landing_page_url = Column(String(500))
    
    # Campaign Dates
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    
    # Status and Platform IDs
    status = Column(Enum(AdStatus), default=AdStatus.DRAFT)
    platform_campaign_id = Column(String(100))  # ID from the platform
    platform_adset_id = Column(String(100))
    platform_ad_id = Column(String(100))
    
    # Performance Metrics
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    spend = Column(Float, default=0.0)
    ctr = Column(Float, default=0.0)  # Click-through rate
    cpc = Column(Float, default=0.0)  # Cost per click
    cpm = Column(Float, default=0.0)  # Cost per thousand impressions
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    account = relationship("SocialMediaAccount", back_populates="ad_campaigns") 