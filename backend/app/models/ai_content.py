from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON, ForeignKey, Float, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class ContentType(enum.Enum):
    AD_COPY = "ad_copy"
    SOCIAL_POST = "social_post"
    EMAIL_TEMPLATE = "email_template"
    SMS_TEMPLATE = "sms_template"
    BLOG_POST = "blog_post"
    PRODUCT_DESCRIPTION = "product_description"
    LANDING_PAGE = "landing_page"

class AssetType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    LOGO = "logo"
    BRANDING = "branding"

class AIGeneratedContent(Base):
    __tablename__ = "ai_generated_content"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    
    # Content Information
    content_type = Column(Enum(ContentType), nullable=False)
    title = Column(String(255))
    content = Column(Text, nullable=False)
    summary = Column(Text)
    
    # Generation Parameters
    prompt = Column(Text)  # Original prompt used
    ai_model = Column(String(50))  # GPT-4, Claude, etc.
    generation_settings = Column(JSON)  # Temperature, max_tokens, etc.
    
    # Content Metadata
    target_audience = Column(String(255))
    tone = Column(String(50))  # professional, casual, friendly, etc.
    language = Column(String(10), default="en")
    keywords = Column(JSON)  # SEO keywords
    
    # Performance Tracking
    usage_count = Column(Integer, default=0)
    last_used = Column(DateTime(timezone=True))
    effectiveness_score = Column(Float)  # 0-100 based on performance
    
    # Version Control
    version = Column(Integer, default=1)
    parent_content_id = Column(Integer, ForeignKey("ai_generated_content.id"))
    
    # Status
    is_approved = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    business = relationship("Business")
    variations = relationship("AIGeneratedContent", backref="parent_content", remote_side=[id])

class ContentAsset(Base):
    __tablename__ = "content_assets"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    
    # Asset Information
    name = Column(String(255), nullable=False)
    description = Column(Text)
    asset_type = Column(Enum(AssetType), nullable=False)
    
    # File Information
    file_url = Column(String(500), nullable=False)
    file_size = Column(Integer)  # Size in bytes
    mime_type = Column(String(100))
    dimensions = Column(String(20))  # For images/videos: "1920x1080"
    duration = Column(Float)  # For videos/audio in seconds
    
    # Asset Metadata
    tags = Column(JSON)  # List of tags for organization
    alt_text = Column(String(255))  # For accessibility
    
    # Usage Tracking
    usage_count = Column(Integer, default=0)
    last_used = Column(DateTime(timezone=True))
    
    # AI Enhancement
    ai_generated = Column(Boolean, default=False)
    ai_prompt = Column(Text)  # If AI generated
    original_asset_id = Column(Integer, ForeignKey("content_assets.id"))  # If enhanced version
    
    # Status
    is_active = Column(Boolean, default=True)
    is_approved = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    business = relationship("Business", back_populates="content_assets")
    enhanced_versions = relationship("ContentAsset", backref="original_asset", remote_side=[id]) 