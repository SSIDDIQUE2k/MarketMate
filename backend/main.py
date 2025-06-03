from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
import uvicorn

app = FastAPI(title="AI Marketing Automation Platform")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploads
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Import routers
from app.api import (
    lead_scoring,
    campaign_sender,
    chatbot,
    dashboard,
    social_media
)
from app.api.website_tracking import router as website_tracking_router
from app.api.ai_content import router as ai_content_router

# Include routers
app.include_router(lead_scoring.router, prefix="/api/leads", tags=["Lead Scoring"])
app.include_router(campaign_sender.router, prefix="/api/campaigns", tags=["Campaigns"])
app.include_router(chatbot.router, prefix="/api/chatbot", tags=["Chatbot"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(social_media.router, prefix="/api/social", tags=["Social Media"])
app.include_router(website_tracking_router, prefix="/api/tracking", tags=["Website Tracking"])
app.include_router(ai_content_router, prefix="/api/ai", tags=["AI Content Generation"])

@app.get("/")
async def root():
    return {"message": "Welcome to AI Marketing Automation Platform"}

@app.get("/tracking-script/{business_id}")
async def get_tracking_script(business_id: int):
    """Serve the JavaScript tracking script for businesses to embed on their websites"""
    
    script = f"""
(function() {{
    var businessId = {business_id};
    var apiUrl = 'http://localhost:8000/api/tracking';
    
    // Generate or get visitor ID
    var visitorId = getCookie('visitor_id') || generateUUID();
    setCookie('visitor_id', visitorId, 365);
    
    // Load tracking pixel
    var img = new Image();
    img.src = apiUrl + '/pixel/' + businessId;
    
    // Track page view
    trackEvent('page_view', {{
        url: window.location.href,
        title: document.title,
        referrer: document.referrer
    }});
    
    // Track time on page
    var startTime = Date.now();
    window.addEventListener('beforeunload', function() {{
        var timeSpent = (Date.now() - startTime) / 1000;
        trackEvent('page_exit', {{
            url: window.location.href,
            duration: timeSpent
        }});
    }});
    
    // Track form submissions
    document.addEventListener('submit', function(e) {{
        var form = e.target;
        var formData = new FormData(form);
        var fields = {{}};
        
        for (var pair of formData.entries()) {{
            fields[pair[0]] = pair[1];
        }}
        
        // Check if email or phone is captured
        var email = fields.email || fields.Email || fields.EMAIL;
        var phone = fields.phone || fields.Phone || fields.PHONE || fields.tel;
        var name = fields.name || fields.Name || fields.NAME || fields.full_name;
        
        if (email || phone) {{
            // This is a lead capture
            captureLeadData({{
                email: email,
                phone: phone,
                name: name,
                form_fields: fields
            }});
        }}
        
        trackEvent('form_submit', {{
            url: window.location.href,
            form_fields: fields
        }});
    }});
    
    // Track clicks on important elements
    document.addEventListener('click', function(e) {{
        var element = e.target;
        var tagName = element.tagName.toLowerCase();
        
        if (tagName === 'a' || tagName === 'button' || element.getAttribute('data-track')) {{
            trackEvent('element_click', {{
                url: window.location.href,
                element_type: tagName,
                element_text: element.textContent.trim(),
                element_id: element.id,
                element_class: element.className
            }});
        }}
    }});
    
    function trackEvent(eventType, eventData) {{
        fetch(apiUrl + '/track-event', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json'
            }},
            body: JSON.stringify({{
                business_id: businessId,
                visitor_id: visitorId,
                event_type: eventType,
                page_url: window.location.href,
                page_title: document.title,
                event_data: eventData
            }})
        }}).catch(function(error) {{
            console.log('Tracking error:', error);
        }});
    }}
    
    function captureLeadData(leadData) {{
        fetch(apiUrl + '/capture-lead', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json'
            }},
            body: JSON.stringify({{
                business_id: businessId,
                visitor_id: visitorId,
                email: leadData.email,
                phone: leadData.phone,
                name: leadData.name,
                form_fields: leadData.form_fields
            }})
        }}).catch(function(error) {{
            console.log('Lead capture error:', error);
        }});
    }}
    
    function generateUUID() {{
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {{
            var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        }});
    }}
    
    function getCookie(name) {{
        var value = "; " + document.cookie;
        var parts = value.split("; " + name + "=");
        if (parts.length == 2) return parts.pop().split(";").shift();
    }}
    
    function setCookie(name, value, days) {{
        var expires = "";
        if (days) {{
            var date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
            expires = "; expires=" + date.toUTCString();
        }}
        document.cookie = name + "=" + (value || "") + expires + "; path=/";
    }}
    
    // Expose lead capture function globally for manual use
    window.captureLeadData = captureLeadData;
    window.trackEvent = trackEvent;
}})();
"""
    
    return {
        "script": script,
        "instructions": f"""
To install this tracking script on your website:

1. Copy the script below and paste it before the closing </body> tag on every page:

<script>
{script}
</script>

2. Alternative: Include it as an external script:
<script src="http://localhost:8000/tracking-script/{business_id}"></script>

Features:
- Automatic visitor tracking and lead scoring
- Form submission monitoring and lead capture
- Page view and engagement tracking
- Click tracking on important elements
- Automatic email/phone capture from forms

The script will automatically:
- Track all page views and visitor behavior
- Capture leads when forms with email/phone are submitted
- Score leads based on engagement
- Send data to your marketing automation dashboard
"""
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 