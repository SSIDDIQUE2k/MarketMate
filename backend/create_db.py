#!/usr/bin/env python3
"""
Database initialization script for the AI Marketing Automation Platform.
This script creates all database tables based on the SQLAlchemy models.
"""

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import Base, DATABASE_URL
from app.models import (
    Business, Lead, Campaign, WebsiteVisitor, WebsiteEvent,
    SocialMediaAccount, SocialMediaPost, AdCampaign,
    AIGeneratedContent, ContentAsset,
    EmailTemplate, SMSTemplate, EmailCampaign, SMSCampaign,
    User
)

def create_database():
    """Create all database tables"""
    try:
        # Create engine
        engine = create_engine(DATABASE_URL)
        
        # Create all tables
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        
        print("✅ Database tables created successfully!")
        print("\nCreated tables:")
        for table_name in Base.metadata.tables.keys():
            print(f"  - {table_name}")
            
    except OperationalError as e:
        print(f"❌ Database connection error: {e}")
        print("\nPlease make sure:")
        print("1. PostgreSQL is running")
        print("2. Database 'marketing_automation' exists")
        print("3. Database credentials in .env are correct")
        print("\nTo create the database:")
        print("  createdb marketing_automation")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_database() 