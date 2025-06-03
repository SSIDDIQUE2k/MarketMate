from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.ai_content import AIGeneratedContent, ContentAsset, ContentType, AssetType
from app.models.business import Business
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import openai
import os
from datetime import datetime
import uuid

router = APIRouter()

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

class AIContentRequest(BaseModel):
    business_id: int
    content_type: ContentType
    prompt: str
    target_audience: Optional[str] = None
    tone: Optional[str] = "professional"
    keywords: Optional[List[str]] = None
    additional_context: Optional[str] = None

class AdCreationRequest(BaseModel):
    business_id: int
    ad_objective: str  # awareness, traffic, conversions, etc.
    target_audience: str
    budget: float
    platform: str  # facebook, instagram, google, etc.
    business_description: str
    product_service: str
    special_offers: Optional[str] = None
    brand_voice: Optional[str] = "professional"
    asset_ids: Optional[List[int]] = None  # Images/videos to use

class ContentAssetUpload(BaseModel):
    business_id: int
    name: str
    description: Optional[str] = None
    asset_type: AssetType
    tags: Optional[List[str]] = None

@router.post("/generate-content")
async def generate_ai_content(
    request: AIContentRequest,
    db: Session = Depends(get_db)
):
    """Generate AI content for various marketing purposes"""
    
    # Get business info for context
    business = db.query(Business).filter(Business.id == request.business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    # Build prompt based on content type and business context
    enhanced_prompt = build_enhanced_prompt(request, business)
    
    try:
        # Generate content using OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": get_system_prompt(request.content_type, business)},
                {"role": "user", "content": enhanced_prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        generated_content = response.choices[0].message.content
        
        # Save to database
        ai_content = AIGeneratedContent(
            business_id=request.business_id,
            content_type=request.content_type,
            content=generated_content,
            prompt=request.prompt,
            ai_model="gpt-4",
            target_audience=request.target_audience,
            tone=request.tone,
            keywords=request.keywords,
            generation_settings={
                "temperature": 0.7,
                "max_tokens": 1000,
                "model": "gpt-4"
            }
        )
        
        db.add(ai_content)
        db.commit()
        
        return {
            "content_id": ai_content.id,
            "content": generated_content,
            "content_type": request.content_type.value,
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content generation failed: {str(e)}")

@router.post("/create-ad-campaign")
async def create_ai_ad_campaign(
    request: AdCreationRequest,
    db: Session = Depends(get_db)
):
    """Generate complete ad campaign with AI including copy, targeting, and creative suggestions"""
    
    business = db.query(Business).filter(Business.id == request.business_id).first()
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    
    # Get business assets if specified
    assets = []
    if request.asset_ids:
        assets = db.query(ContentAsset).filter(
            ContentAsset.id.in_(request.asset_ids),
            ContentAsset.business_id == request.business_id
        ).all()
    
    # Generate ad copy
    ad_copy_prompt = f"""
    Create compelling ad copy for a {request.platform} ad campaign.
    
    Business: {business.name}
    Industry: {business.industry}
    Product/Service: {request.product_service}
    Target Audience: {request.target_audience}
    Objective: {request.ad_objective}
    Budget: ${request.budget}
    Brand Voice: {request.brand_voice}
    Special Offers: {request.special_offers or 'None'}
    
    Generate multiple variations of:
    1. Headlines (5 options)
    2. Primary text (3 options)
    3. Call-to-action suggestions
    4. Hashtag recommendations (if applicable)
    """
    
    try:
        # Generate ad copy
        copy_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are an expert {request.platform} ads copywriter."},
                {"role": "user", "content": ad_copy_prompt}
            ],
            max_tokens=1500,
            temperature=0.8
        )
        
        ad_copy = copy_response.choices[0].message.content
        
        # Generate targeting suggestions
        targeting_prompt = f"""
        Create detailed targeting recommendations for a {request.platform} ad campaign:
        
        Business: {business.name}
        Target Audience: {request.target_audience}
        Objective: {request.ad_objective}
        Location: Based on business location
        
        Provide:
        1. Demographic targeting (age, gender, education, income)
        2. Interest targeting
        3. Behavior targeting
        4. Custom audience suggestions
        5. Lookalike audience recommendations
        """
        
        targeting_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a digital marketing expert specializing in ad targeting."},
                {"role": "user", "content": targeting_prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        targeting_suggestions = targeting_response.choices[0].message.content
        
        # Save ad campaign content
        ad_content = AIGeneratedContent(
            business_id=request.business_id,
            content_type=ContentType.AD_COPY,
            title=f"AI Ad Campaign - {request.platform}",
            content=ad_copy,
            prompt=ad_copy_prompt,
            ai_model="gpt-4",
            target_audience=request.target_audience,
            tone=request.brand_voice,
            generation_settings={
                "platform": request.platform,
                "objective": request.ad_objective,
                "budget": request.budget,
                "targeting": targeting_suggestions
            }
        )
        
        db.add(ad_content)
        db.commit()
        
        return {
            "campaign_id": ad_content.id,
            "ad_copy": ad_copy,
            "targeting_suggestions": targeting_suggestions,
            "recommended_assets": [{"id": asset.id, "name": asset.name, "url": asset.file_url} for asset in assets],
            "platform": request.platform,
            "estimated_reach": calculate_estimated_reach(request.budget, request.platform),
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ad campaign creation failed: {str(e)}")

@router.post("/upload-asset")
async def upload_content_asset(
    file: UploadFile = File(...),
    business_id: int = None,
    name: str = None,
    description: str = None,
    asset_type: str = None,
    db: Session = Depends(get_db)
):
    """Upload business assets (images, videos, documents) for AI to use in content creation"""
    
    if not business_id or not name or not asset_type:
        raise HTTPException(status_code=400, detail="Missing required fields")
    
    try:
        # Generate unique filename
        file_extension = file.filename.split('.')[-1]
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        
        # Save file (in production, this would be to S3 or similar)
        file_path = f"uploads/{business_id}/{unique_filename}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Create asset record
        asset = ContentAsset(
            business_id=business_id,
            name=name,
            description=description,
            asset_type=AssetType(asset_type),
            file_url=file_path,
            file_size=len(content),
            mime_type=file.content_type
        )
        
        db.add(asset)
        db.commit()
        
        return {
            "asset_id": asset.id,
            "name": asset.name,
            "file_url": asset.file_url,
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Asset upload failed: {str(e)}")

@router.get("/content/{business_id}")
async def get_ai_content(
    business_id: int,
    content_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all AI-generated content for a business"""
    
    query = db.query(AIGeneratedContent).filter(AIGeneratedContent.business_id == business_id)
    
    if content_type:
        query = query.filter(AIGeneratedContent.content_type == content_type)
    
    content = query.order_by(AIGeneratedContent.created_at.desc()).all()
    
    return {"content": content}

@router.get("/assets/{business_id}")
async def get_business_assets(
    business_id: int,
    asset_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all assets for a business"""
    
    query = db.query(ContentAsset).filter(ContentAsset.business_id == business_id)
    
    if asset_type:
        query = query.filter(ContentAsset.asset_type == asset_type)
    
    assets = query.order_by(ContentAsset.created_at.desc()).all()
    
    return {"assets": assets}

def build_enhanced_prompt(request: AIContentRequest, business: Business) -> str:
    """Build enhanced prompt with business context"""
    
    context = f"""
    Business Context:
    - Company: {business.name}
    - Industry: {business.industry or 'Not specified'}
    - Website: {business.website_url or 'Not provided'}
    - Brand Guidelines: {business.brand_guidelines or 'None specified'}
    
    Content Requirements:
    - Target Audience: {request.target_audience or 'General audience'}
    - Tone: {request.tone}
    - Keywords: {', '.join(request.keywords) if request.keywords else 'None'}
    
    Original Request: {request.prompt}
    
    Additional Context: {request.additional_context or 'None'}
    """
    
    return context

def get_system_prompt(content_type: ContentType, business: Business) -> str:
    """Get system prompt based on content type"""
    
    base_prompt = f"You are an expert marketing copywriter for {business.name}, a {business.industry} company."
    
    if content_type == ContentType.AD_COPY:
        return f"{base_prompt} Create compelling, conversion-focused ad copy that drives action."
    elif content_type == ContentType.SOCIAL_POST:
        return f"{base_prompt} Create engaging social media content that builds community and drives engagement."
    elif content_type == ContentType.EMAIL_TEMPLATE:
        return f"{base_prompt} Create professional email marketing content that nurtures leads and drives conversions."
    elif content_type == ContentType.SMS_TEMPLATE:
        return f"{base_prompt} Create concise, actionable SMS marketing messages under 160 characters."
    else:
        return f"{base_prompt} Create high-quality marketing content that aligns with the brand voice and objectives."

def calculate_estimated_reach(budget: float, platform: str) -> dict:
    """Calculate estimated reach based on budget and platform"""
    
    # Simplified reach calculation (in production, use actual platform APIs)
    cpm_rates = {
        "facebook": 7.19,
        "instagram": 7.91,
        "google": 2.80,
        "linkedin": 33.80,
        "twitter": 6.46
    }
    
    cpm = cpm_rates.get(platform.lower(), 10.0)
    estimated_impressions = int((budget / cpm) * 1000)
    estimated_reach = int(estimated_impressions * 0.3)  # Assuming 30% unique reach
    
    return {
        "estimated_impressions": estimated_impressions,
        "estimated_reach": estimated_reach,
        "estimated_cpm": cpm
    } 