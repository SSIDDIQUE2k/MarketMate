from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime
import openai
import tweepy
import facebook
from instagrapi import Client
import os
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.social_media import SocialMediaAccount, SocialMediaPost, AdCampaign, PlatformType
from app.models.business import Business
import requests

# Social media imports with error handling
try:
    import tweepy
    TWITTER_AVAILABLE = True
except ImportError:
    TWITTER_AVAILABLE = False

try:
    import facebook
    FACEBOOK_AVAILABLE = True
except ImportError:
    FACEBOOK_AVAILABLE = False

try:
    from linkedin_api import Linkedin
    LINKEDIN_AVAILABLE = True
except ImportError:
    LINKEDIN_AVAILABLE = False

try:
    from instagrapi import Client
    INSTAGRAM_AVAILABLE = True
except ImportError:
    INSTAGRAM_AVAILABLE = False

router = APIRouter()

class SocialPost(BaseModel):
    id: str
    platform: str  # "twitter", "facebook", "linkedin", "instagram"
    content: str
    media_url: Optional[str] = None
    schedule_time: Optional[datetime] = None
    status: str = "draft"

class PostAnalytics(BaseModel):
    post_id: str
    platform: str
    likes: int
    comments: int
    shares: int
    reach: int
    engagement_rate: float

class SocialMediaAccountCreate(BaseModel):
    business_id: int
    platform: str
    username: str
    access_token: str
    refresh_token: Optional[str] = None

class PostCreate(BaseModel):
    account_id: int
    content: str
    hashtags: Optional[List[str]] = None
    scheduled_for: Optional[str] = None

class AdCampaignCreate(BaseModel):
    account_id: int
    name: str
    description: str
    objective: str
    budget_amount: float
    target_audience: Dict[str, Any]
    ad_creative: Dict[str, Any]

def get_twitter_client():
    """Get Twitter client when needed"""
    if not TWITTER_AVAILABLE:
        raise HTTPException(status_code=400, detail="Twitter API not available")
    
    api_key = os.getenv('TWITTER_API_KEY')
    api_secret = os.getenv('TWITTER_API_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    
    if not all([api_key, api_secret, access_token, access_token_secret]):
        raise HTTPException(status_code=400, detail="Twitter credentials not configured")
    
    return tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

def get_facebook_client():
    """Get Facebook client when needed"""
    if not FACEBOOK_AVAILABLE:
        raise HTTPException(status_code=400, detail="Facebook API not available")
    
    access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
    if not access_token:
        raise HTTPException(status_code=400, detail="Facebook access token not configured")
    
    return facebook.GraphAPI(access_token=access_token)

def get_instagram_client(username: str, password: str):
    """Get Instagram client when needed"""
    if not INSTAGRAM_AVAILABLE:
        raise HTTPException(status_code=400, detail="Instagram API not available")
    
    try:
        client = Client()
        client.login(username, password)
        return client
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Instagram authentication failed: {str(e)}")

def get_linkedin_client(username: str, password: str):
    """Get LinkedIn client when needed"""
    if not LINKEDIN_AVAILABLE:
        raise HTTPException(status_code=400, detail="LinkedIn API not available")
    
    try:
        return Linkedin(username, password)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"LinkedIn authentication failed: {str(e)}")

@router.post("/posts", response_model=SocialPost)
async def create_social_post(post: SocialPost):
    """
    Create and schedule a social media post
    """
    try:
        # Generate AI-powered caption if not provided
        if not post.content:
            post.content = generate_caption(post.platform)

        # Schedule or post immediately based on schedule_time
        if post.schedule_time and post.schedule_time > datetime.now():
            # In a real application, this would be added to a queue
            return post
        else:
            return await publish_post(post)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def generate_caption(platform: str) -> str:
    """
    Generate AI-powered caption for social media post
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Generate an engaging social media caption for {platform}. Include relevant hashtags."},
                {"role": "user", "content": "Create a post about our new product launch"}
            ],
            temperature=0.7,
            max_tokens=100
        )
        return response.choices[0].message.content
    except:
        return "Check out our latest product! #marketing #innovation"

async def publish_post(post: SocialPost) -> SocialPost:
    """
    Publish post to the specified social media platform
    """
    try:
        if post.platform == "twitter":
            twitter_client = get_twitter_client()
            twitter_client.create_tweet(text=post.content)
        elif post.platform == "facebook":
            facebook_client = get_facebook_client()
            facebook_client.put_object(
                parent_object="me",
                connection_name="feed",
                message=post.content
            )
        elif post.platform == "linkedin":
            linkedin_client = get_linkedin_client(os.getenv('LINKEDIN_EMAIL'), os.getenv('LINKEDIN_PASSWORD'))
            linkedin_client.post(
                post.content,
                visibility="PUBLIC"
            )
        elif post.platform == "instagram":
            instagram_client = get_instagram_client(os.getenv('INSTAGRAM_USERNAME'), os.getenv('INSTAGRAM_PASSWORD'))
            if post.media_url:
                instagram_client.photo_upload(
                    post.media_url,
                    post.content
                )
            else:
                instagram_client.direct_send(
                    post.content,
                    user_ids=[os.getenv('INSTAGRAM_USER_ID')]
                )
        else:
            raise HTTPException(status_code=400, detail="Invalid platform")

        post.status = "published"
        return post
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/posts/{post_id}/analytics", response_model=PostAnalytics)
async def get_post_analytics(post_id: str, platform: str):
    """
    Get analytics for a specific social media post
    """
    try:
        # In a real application, this would fetch actual analytics from the platform
        return PostAnalytics(
            post_id=post_id,
            platform=platform,
            likes=100,
            comments=20,
            shares=15,
            reach=1000,
            engagement_rate=13.5
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/platforms/{platform}/analytics")
async def get_platform_analytics(platform: str):
    """
    Get overall analytics for a social media platform
    """
    try:
        # In a real application, this would fetch actual analytics from the platform
        return {
            "followers": 10000,
            "engagement_rate": 4.5,
            "total_posts": 100,
            "average_likes": 500,
            "average_comments": 50
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/connect-account")
async def connect_social_media_account(
    account: SocialMediaAccountCreate,
    db: Session = Depends(get_db)
):
    """Connect a social media account"""
    
    # Validate platform
    try:
        platform = PlatformType(account.platform.lower())
    except ValueError:
        raise HTTPException(status_code=400, detail="Unsupported platform")
    
    # Verify business exists
    business = db.query(Business).filter(Business.id == account.business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    # Create social media account
    social_account = SocialMediaAccount(
        business_id=account.business_id,
        platform=platform,
        username=account.username,
        access_token=account.access_token,
        refresh_token=account.refresh_token,
        is_active=True
    )
    
    db.add(social_account)
    db.commit()
    db.refresh(social_account)
    
    return {"message": "Account connected successfully", "account_id": social_account.id}

@router.get("/accounts/{business_id}")
async def get_social_media_accounts(
    business_id: int,
    db: Session = Depends(get_db)
):
    """Get all connected social media accounts for a business"""
    
    accounts = db.query(SocialMediaAccount).filter(
        SocialMediaAccount.business_id == business_id,
        SocialMediaAccount.is_active == True
    ).all()
    
    return {"accounts": accounts}

@router.post("/create-post")
async def create_social_media_post(
    post: PostCreate,
    db: Session = Depends(get_db)
):
    """Create a social media post"""
    
    # Get account
    account = db.query(SocialMediaAccount).filter(SocialMediaAccount.id == post.account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Social media account not found")
    
    # Create post
    social_post = SocialMediaPost(
        account_id=post.account_id,
        content=post.content,
        hashtags=post.hashtags or [],
        scheduled_for=post.scheduled_for
    )
    
    db.add(social_post)
    db.commit()
    db.refresh(social_post)
    
    # TODO: Implement actual posting to social platforms based on account.platform
    
    return {"message": "Post created successfully", "post_id": social_post.id}

@router.post("/launch-ad")
async def launch_ad_campaign(
    campaign: AdCampaignCreate,
    db: Session = Depends(get_db)
):
    """Launch an ad campaign on social media"""
    
    # Get account
    account = db.query(SocialMediaAccount).filter(SocialMediaAccount.id == campaign.account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Social media account not found")
    
    # Create ad campaign
    ad_campaign = AdCampaign(
        account_id=campaign.account_id,
        name=campaign.name,
        description=campaign.description,
        objective=campaign.objective,
        budget_amount=campaign.budget_amount,
        target_audience=campaign.target_audience,
        ad_creative=campaign.ad_creative
    )
    
    db.add(ad_campaign)
    db.commit()
    db.refresh(ad_campaign)
    
    # TODO: Implement actual ad campaign creation on platforms
    
    return {"message": "Ad campaign created successfully", "campaign_id": ad_campaign.id}

@router.get("/analytics/{business_id}")
async def get_social_media_analytics(
    business_id: int,
    db: Session = Depends(get_db)
):
    """Get social media analytics for a business"""
    
    # Get all accounts for business
    accounts = db.query(SocialMediaAccount).filter(
        SocialMediaAccount.business_id == business_id
    ).all()
    
    analytics = {}
    for account in accounts:
        # Get posts for this account
        posts = db.query(SocialMediaPost).filter(
            SocialMediaPost.account_id == account.id
        ).all()
        
        # Get ad campaigns for this account
        campaigns = db.query(AdCampaign).filter(
            AdCampaign.account_id == account.id
        ).all()
        
        analytics[account.platform.value] = {
            "account_id": account.id,
            "username": account.username,
            "followers": account.followers_count,
            "posts_count": len(posts),
            "campaigns_count": len(campaigns),
            "total_impressions": sum(c.impressions for c in campaigns),
            "total_clicks": sum(c.clicks for c in campaigns),
            "total_spend": sum(c.spend for c in campaigns)
        }
    
    return {"analytics": analytics}

@router.get("/platforms")
async def get_supported_platforms():
    """Get list of supported social media platforms and their availability"""
    
    platforms = {
        "facebook": {
            "available": FACEBOOK_AVAILABLE,
            "name": "Facebook"
        },
        "instagram": {
            "available": INSTAGRAM_AVAILABLE,
            "name": "Instagram"
        },
        "twitter": {
            "available": TWITTER_AVAILABLE,
            "name": "Twitter"
        },
        "linkedin": {
            "available": LINKEDIN_AVAILABLE,
            "name": "LinkedIn"
        }
    }
    
    return {"platforms": platforms} 