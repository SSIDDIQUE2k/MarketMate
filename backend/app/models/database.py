from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, JSON, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# Association tables for many-to-many relationships
campaign_leads = Table(
    'campaign_leads',
    Base.metadata,
    Column('campaign_id', Integer, ForeignKey('campaigns.id')),
    Column('lead_id', Integer, ForeignKey('leads.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    campaigns = relationship("Campaign", back_populates="owner")
    leads = relationship("Lead", back_populates="owner")

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, index=True)
    company = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    interactions = Column(JSON, default=list)
    engagement_score = Column(Float, default=0.0)
    status = Column(String, default="new")
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_contact = Column(DateTime, nullable=True)

    # Relationships
    owner = relationship("User", back_populates="leads")
    campaigns = relationship("Campaign", secondary=campaign_leads, back_populates="leads")

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)  # email or sms
    content = Column(String)
    schedule_time = Column(DateTime, nullable=True)
    status = Column(String, default="draft")
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Metrics
    sent_count = Column(Integer, default=0)
    open_rate = Column(Float, default=0.0)
    click_rate = Column(Float, default=0.0)
    conversion_rate = Column(Float, default=0.0)
    revenue = Column(Float, default=0.0)

    # Relationships
    owner = relationship("User", back_populates="campaigns")
    leads = relationship("Lead", secondary=campaign_leads, back_populates="campaigns")

class SocialPost(Base):
    __tablename__ = "social_posts"

    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String)  # twitter, facebook, linkedin, instagram
    content = Column(String)
    media_url = Column(String, nullable=True)
    schedule_time = Column(DateTime, nullable=True)
    status = Column(String, default="draft")
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Metrics
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    reach = Column(Integer, default=0)
    engagement_rate = Column(Float, default=0.0)

    # Relationships
    owner = relationship("User")

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    messages = Column(JSON, default=list)
    context = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User") 