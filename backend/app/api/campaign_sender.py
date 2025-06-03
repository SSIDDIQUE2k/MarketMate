from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client
import os

router = APIRouter()

class Campaign(BaseModel):
    id: str
    name: str
    type: str  # "email" or "sms"
    content: str
    schedule_time: Optional[datetime] = None
    target_audience: List[str]
    status: str = "draft"

class CampaignResponse(BaseModel):
    campaign_id: str
    status: str
    sent_count: int
    failed_count: int
    scheduled_time: Optional[datetime]

# Initialize SendGrid client
sendgrid_client = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))

# Initialize Twilio client
twilio_client = Client(
    os.getenv('TWILIO_ACCOUNT_SID'),
    os.getenv('TWILIO_AUTH_TOKEN')
)

@router.post("/campaigns", response_model=CampaignResponse)
async def create_campaign(campaign: Campaign):
    """
    Create and schedule a new campaign
    """
    try:
        if campaign.type == "email":
            return await send_email_campaign(campaign)
        elif campaign.type == "sms":
            return await send_sms_campaign(campaign)
        else:
            raise HTTPException(status_code=400, detail="Invalid campaign type")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def send_email_campaign(campaign: Campaign) -> CampaignResponse:
    """
    Send an email campaign using SendGrid
    """
    sent_count = 0
    failed_count = 0

    for recipient in campaign.target_audience:
        try:
            message = Mail(
                from_email=os.getenv('SENDER_EMAIL'),
                to_emails=recipient,
                subject=campaign.name,
                html_content=campaign.content
            )
            
            response = sendgrid_client.send(message)
            if response.status_code == 202:
                sent_count += 1
            else:
                failed_count += 1
        except Exception:
            failed_count += 1

    return CampaignResponse(
        campaign_id=campaign.id,
        status="completed",
        sent_count=sent_count,
        failed_count=failed_count,
        scheduled_time=campaign.schedule_time
    )

async def send_sms_campaign(campaign: Campaign) -> CampaignResponse:
    """
    Send an SMS campaign using Twilio
    """
    sent_count = 0
    failed_count = 0

    for recipient in campaign.target_audience:
        try:
            message = twilio_client.messages.create(
                body=campaign.content,
                from_=os.getenv('TWILIO_PHONE_NUMBER'),
                to=recipient
            )
            if message.status == 'queued':
                sent_count += 1
            else:
                failed_count += 1
        except Exception:
            failed_count += 1

    return CampaignResponse(
        campaign_id=campaign.id,
        status="completed",
        sent_count=sent_count,
        failed_count=failed_count,
        scheduled_time=campaign.schedule_time
    )

@router.get("/campaigns", response_model=List[Campaign])
async def get_campaigns():
    """
    Get all campaigns
    """
    # This would typically fetch from a database
    return []

@router.get("/campaigns/{campaign_id}", response_model=Campaign)
async def get_campaign(campaign_id: str):
    """
    Get a specific campaign by ID
    """
    # This would typically fetch from a database
    raise HTTPException(status_code=404, detail="Campaign not found") 