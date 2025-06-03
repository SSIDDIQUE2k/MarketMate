from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional, Dict
from pydantic import BaseModel
from datetime import datetime, timedelta
import numpy as np

router = APIRouter()

class Metric(BaseModel):
    name: str
    value: float
    change: float
    trend: str  # "up", "down", "stable"

class CampaignMetrics(BaseModel):
    campaign_id: str
    name: str
    sent_count: int
    open_rate: float
    click_rate: float
    conversion_rate: float
    revenue: float

class SocialMetrics(BaseModel):
    platform: str
    followers: int
    engagement_rate: float
    post_count: int
    top_performing_post: str

class DashboardData(BaseModel):
    leads: Dict[str, Metric]
    campaigns: List[CampaignMetrics]
    social: List[SocialMetrics]
    revenue: Metric
    engagement: Metric

@router.get("/metrics", response_model=DashboardData)
async def get_dashboard_metrics(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """
    Get real-time dashboard metrics
    """
    try:
        # In a real application, these would be fetched from a database
        # and calculated based on actual data
        return generate_mock_metrics(start_date, end_date)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def generate_mock_metrics(
    start_date: Optional[datetime],
    end_date: Optional[datetime]
) -> DashboardData:
    """
    Generate mock metrics for demonstration
    """
    if not start_date:
        start_date = datetime.now() - timedelta(days=30)
    if not end_date:
        end_date = datetime.now()

    # Generate mock lead metrics
    leads = {
        "total": Metric(
            name="Total Leads",
            value=1250,
            change=12.5,
            trend="up"
        ),
        "qualified": Metric(
            name="Qualified Leads",
            value=450,
            change=8.3,
            trend="up"
        ),
        "conversion": Metric(
            name="Conversion Rate",
            value=3.2,
            change=-0.5,
            trend="down"
        )
    }

    # Generate mock campaign metrics
    campaigns = [
        CampaignMetrics(
            campaign_id="1",
            name="Q4 Product Launch",
            sent_count=5000,
            open_rate=45.2,
            click_rate=12.8,
            conversion_rate=3.5,
            revenue=25000.0
        ),
        CampaignMetrics(
            campaign_id="2",
            name="Holiday Special",
            sent_count=3000,
            open_rate=52.1,
            click_rate=15.3,
            conversion_rate=4.2,
            revenue=18000.0
        )
    ]

    # Generate mock social metrics
    social = [
        SocialMetrics(
            platform="Instagram",
            followers=25000,
            engagement_rate=4.2,
            post_count=45,
            top_performing_post="Product showcase"
        ),
        SocialMetrics(
            platform="LinkedIn",
            followers=12000,
            engagement_rate=3.8,
            post_count=30,
            top_performing_post="Industry insights"
        )
    ]

    # Generate overall metrics
    revenue = Metric(
        name="Total Revenue",
        value=43000.0,
        change=15.3,
        trend="up"
    )

    engagement = Metric(
        name="Overall Engagement",
        value=4.0,
        change=0.8,
        trend="up"
    )

    return DashboardData(
        leads=leads,
        campaigns=campaigns,
        social=social,
        revenue=revenue,
        engagement=engagement
    )

@router.get("/campaigns/{campaign_id}/metrics", response_model=CampaignMetrics)
async def get_campaign_metrics(campaign_id: str):
    """
    Get detailed metrics for a specific campaign
    """
    # This would typically fetch from a database
    raise HTTPException(status_code=404, detail="Campaign not found")

@router.get("/social/{platform}/metrics", response_model=SocialMetrics)
async def get_social_metrics(platform: str):
    """
    Get detailed metrics for a specific social platform
    """
    # This would typically fetch from a database
    raise HTTPException(status_code=404, detail="Platform not found") 