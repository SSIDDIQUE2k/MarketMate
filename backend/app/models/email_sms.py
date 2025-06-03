from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, JSON, ForeignKey, Float, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class CampaignStatus(enum.Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    SENDING = "sending"
    SENT = "sent"
    PAUSED = "paused"
    CANCELLED = "cancelled"

class EmailTemplate(Base):
    __tablename__ = "email_templates"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    
    # Template Information
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100))  # welcome, promotional, transactional, etc.
    
    # Email Content
    subject = Column(String(255), nullable=False)
    html_content = Column(Text)
    text_content = Column(Text)
    
    # Template Variables
    variables = Column(JSON)  # List of variables like {{name}}, {{company}}
    
    # Design Settings
    design_data = Column(JSON)  # Template design configuration
    thumbnail_url = Column(String(500))
    
    # Performance
    usage_count = Column(Integer, default=0)
    avg_open_rate = Column(Float, default=0.0)
    avg_click_rate = Column(Float, default=0.0)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    business = relationship("Business")
    email_campaigns = relationship("EmailCampaign", back_populates="template")

class SMSTemplate(Base):
    __tablename__ = "sms_templates"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    
    # Template Information
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100))  # welcome, promotional, reminder, etc.
    
    # SMS Content
    message = Column(Text, nullable=False)  # Max 160 characters for standard SMS
    
    # Template Variables
    variables = Column(JSON)  # List of variables like {{name}}, {{code}}
    
    # Performance
    usage_count = Column(Integer, default=0)
    avg_delivery_rate = Column(Float, default=0.0)
    avg_response_rate = Column(Float, default=0.0)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_default = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    business = relationship("Business")
    sms_campaigns = relationship("SMSCampaign", back_populates="template")

class EmailCampaign(Base):
    __tablename__ = "email_campaigns"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    template_id = Column(Integer, ForeignKey("email_templates.id"))
    
    # Campaign Information
    name = Column(String(255), nullable=False)
    description = Column(Text)
    campaign_type = Column(String(50))  # newsletter, promotional, drip, etc.
    
    # Content (can override template)
    subject = Column(String(255), nullable=False)
    html_content = Column(Text)
    text_content = Column(Text)
    
    # Recipients
    recipient_list = Column(JSON)  # List of email addresses
    segment_criteria = Column(JSON)  # Dynamic segmentation rules
    total_recipients = Column(Integer, default=0)
    
    # Scheduling
    send_immediately = Column(Boolean, default=True)
    scheduled_for = Column(DateTime(timezone=True))
    timezone = Column(String(50))
    
    # A/B Testing
    is_ab_test = Column(Boolean, default=False)
    ab_test_variants = Column(JSON)  # Different subject lines, content, etc.
    ab_test_percentage = Column(Float, default=100.0)
    
    # Status
    status = Column(Enum(CampaignStatus), default=CampaignStatus.DRAFT)
    
    # Performance Metrics
    sent_count = Column(Integer, default=0)
    delivered_count = Column(Integer, default=0)
    opened_count = Column(Integer, default=0)
    clicked_count = Column(Integer, default=0)
    unsubscribed_count = Column(Integer, default=0)
    bounced_count = Column(Integer, default=0)
    
    # Calculated Rates
    delivery_rate = Column(Float, default=0.0)
    open_rate = Column(Float, default=0.0)
    click_rate = Column(Float, default=0.0)
    unsubscribe_rate = Column(Float, default=0.0)
    bounce_rate = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    sent_at = Column(DateTime(timezone=True))
    
    # Relationships
    business = relationship("Business", back_populates="email_campaigns")
    template = relationship("EmailTemplate", back_populates="email_campaigns")

class SMSCampaign(Base):
    __tablename__ = "sms_campaigns"

    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    template_id = Column(Integer, ForeignKey("sms_templates.id"))
    
    # Campaign Information
    name = Column(String(255), nullable=False)
    description = Column(Text)
    campaign_type = Column(String(50))  # promotional, reminder, otp, etc.
    
    # Content (can override template)
    message = Column(Text, nullable=False)
    
    # Recipients
    recipient_list = Column(JSON)  # List of phone numbers
    segment_criteria = Column(JSON)  # Dynamic segmentation rules
    total_recipients = Column(Integer, default=0)
    
    # Scheduling
    send_immediately = Column(Boolean, default=True)
    scheduled_for = Column(DateTime(timezone=True))
    timezone = Column(String(50))
    
    # Status
    status = Column(Enum(CampaignStatus), default=CampaignStatus.DRAFT)
    
    # Performance Metrics
    sent_count = Column(Integer, default=0)
    delivered_count = Column(Integer, default=0)
    clicked_count = Column(Integer, default=0)  # For SMS with links
    replied_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)
    
    # Calculated Rates
    delivery_rate = Column(Float, default=0.0)
    click_rate = Column(Float, default=0.0)
    reply_rate = Column(Float, default=0.0)
    
    # Costs
    cost_per_sms = Column(Float, default=0.0)
    total_cost = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    sent_at = Column(DateTime(timezone=True))
    
    # Relationships
    business = relationship("Business", back_populates="sms_campaigns")
    template = relationship("SMSTemplate", back_populates="sms_campaigns") 