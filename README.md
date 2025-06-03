# 🚀 MarketMate - AI Marketing Automation Platform

> **Built for the NVIDIA Hackathon** 🎯

A comprehensive marketing automation platform that combines AI-powered content generation, website visitor tracking, social media management, and multi-channel campaign management.

## ✨ Features

### 🎯 Core Capabilities
- **Business Profile Management** - Complete business setup with brand guidelines and website integration
- **Website Visitor Tracking** - Real-time visitor analytics with lead scoring and behavioral tracking
- **AI Content Generation** - GPT-4 powered content creation for ads, emails, and social media posts
- **Social Media Management** - Multi-platform posting and ad campaign management
- **Email & SMS Marketing** - Automated campaigns with templates and analytics
- **Lead Management** - Comprehensive lead capture, scoring, and nurturing
- **Analytics Dashboard** - Real-time performance metrics and ROI tracking

### 🤖 AI-Powered Features
- **Smart Content Creation** - Generate marketing content based on business context
- **Lead Scoring Algorithm** - Automatically score leads based on behavior and engagement
- **Campaign Optimization** - AI-driven recommendations for better performance
- **Audience Targeting** - Intelligent audience segmentation and targeting suggestions

### 📊 Analytics & Tracking
- **Website Tracking Pixel** - JavaScript-based visitor tracking and event monitoring
- **Conversion Funnels** - Track user journey from visitor to customer
- **Performance Metrics** - CTR, conversion rates, ROI, and engagement analytics
- **Real-time Dashboards** - Live data visualization and reporting

## 🏗️ Architecture

### Backend (FastAPI)
```
backend/
├── app/
│   ├── api/                    # API endpoints
│   │   ├── ai_content.py      # AI content generation
│   │   ├── campaign_sender.py # Email/SMS campaigns
│   │   ├── chatbot.py         # AI chatbot
│   │   ├── dashboard.py       # Analytics dashboard
│   │   ├── lead_scoring.py    # Lead management
│   │   ├── social_media.py    # Social media management
│   │   ├── users.py           # User management
│   │   └── website_tracking.py # Website tracking
│   ├── core/
│   │   └── database.py        # Database configuration
│   └── models/                # SQLAlchemy models
├── main.py                    # FastAPI application
├── requirements.txt           # Python dependencies
└── create_db.py              # Database initialization
```

### Frontend (React + TypeScript)
```
frontend/
├── src/
│   ├── components/            # React components
│   ├── pages/                 # Page components
│   ├── store/                 # Redux store
│   ├── types/                 # TypeScript types
│   └── utils/                 # Utility functions
├── public/                    # Static assets
└── package.json              # Node.js dependencies
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 12+
- Git

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/SSIDDIQUE2k/MarketMate.git
cd MarketMate
```

2. **Set up the backend**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cp sample.env .env
# Edit .env with your API keys and database credentials
```

4. **Set up the database**
```bash
./setup_database.sh  # Creates PostgreSQL user and database
python create_db.py   # Creates all tables
```

5. **Start the backend server**
```bash
python main.py
# Server will be available at http://localhost:8000
# API Documentation: http://localhost:8000/docs
```

### Frontend Setup

1. **Install dependencies**
```bash
cd frontend
npm install
```

2. **Start the development server**
```bash
npm start
# Frontend will be available at http://localhost:3000
```

### Quick Start Script

For convenience, use the provided startup script:
```bash
./start_backend.sh
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql://marketinguser:marketing123@localhost:5432/marketing_automation

# AI Services
OPENAI_API_KEY=your_openai_api_key_here

# Email Marketing
SENDGRID_API_KEY=your_sendgrid_api_key_here

# SMS Marketing
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token

# Social Media APIs
FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_APP_SECRET=your_facebook_app_secret
LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret

# Security
JWT_SECRET_KEY=your_jwt_secret_key_here_make_it_long_and_random

# CORS Settings
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

## 📡 API Endpoints

### Business Management
- `POST /api/business/create` - Create business profile
- `GET /api/business/{id}` - Get business details
- `PUT /api/business/{id}` - Update business profile

### Website Tracking
- `GET /tracking-script/{business_id}` - Get tracking script for website
- `POST /api/tracking/track-event` - Track website events
- `POST /api/tracking/capture-lead` - Capture lead information
- `GET /api/tracking/visitors/{business_id}` - Get visitor analytics

### AI Content Generation
- `POST /api/ai/generate-content` - Generate marketing content
- `POST /api/ai/generate-ad` - Create ad copy and creative
- `POST /api/ai/generate-email` - Generate email campaigns
- `GET /api/ai/content-history/{business_id}` - Get content history

### Social Media Management
- `POST /api/social/connect-account` - Connect social media account
- `POST /api/social/create-post` - Create social media post
- `POST /api/social/launch-ad` - Launch ad campaign
- `GET /api/social/analytics/{business_id}` - Get social media analytics

### Campaign Management
- `POST /api/campaigns/email/create` - Create email campaign
- `POST /api/campaigns/sms/create` - Create SMS campaign
- `GET /api/campaigns/analytics/{campaign_id}` - Get campaign performance

### Lead Management
- `GET /api/leads/{business_id}` - Get leads for business
- `POST /api/leads/score` - Calculate lead score
- `PUT /api/leads/{lead_id}` - Update lead information

### Dashboard & Analytics
- `GET /api/dashboard/overview/{business_id}` - Get dashboard overview
- `GET /api/dashboard/performance/{business_id}` - Get performance metrics
- `GET /api/dashboard/conversion-funnel/{business_id}` - Get conversion funnel data

## 🎯 Usage Examples

### 1. Setting Up Website Tracking

```javascript
// Get tracking script for your business
const response = await fetch('http://localhost:8000/tracking-script/1');
const data = await response.json();

// Add the script to your website's <head> or before </body>
// The script will automatically track:
// - Page views
// - Form submissions
// - Button clicks
// - Time spent on page
// - Lead capture
```

### 2. Generating AI Content

```python
import requests

# Generate ad copy
response = requests.post('http://localhost:8000/api/ai/generate-content', json={
    "business_id": 1,
    "content_type": "ad_copy",
    "platform": "facebook",
    "objective": "increase_sales",
    "target_audience": "small business owners",
    "additional_context": "promoting our new CRM software"
})

content = response.json()
print(content['generated_content'])
```

### 3. Creating Social Media Campaigns

```python
# Connect social media account
requests.post('http://localhost:8000/api/social/connect-account', json={
    "business_id": 1,
    "platform": "facebook",
    "username": "your_page_name",
    "access_token": "your_facebook_access_token"
})

# Create and schedule a post
requests.post('http://localhost:8000/api/social/create-post', json={
    "account_id": 1,
    "content": "Check out our latest product launch! 🚀",
    "hashtags": ["#innovation", "#technology", "#startup"],
    "scheduled_for": "2024-01-15T10:00:00Z"
})
```

### 4. Email Campaign Management

```python
# Create email campaign
requests.post('http://localhost:8000/api/campaigns/email/create', json={
    "business_id": 1,
    "name": "Product Launch Campaign",
    "subject_line": "Introducing Our Revolutionary New Product",
    "content": "HTML email content here...",
    "recipient_list": ["lead", "customer"],
    "send_time": "2024-01-15T09:00:00Z"
})
```

## 📊 Database Schema

### Core Tables
- **businesses** - Business profiles and settings
- **users** - User accounts and authentication
- **leads** - Lead information and scoring
- **campaigns** - Marketing campaigns across all channels

### Tracking Tables
- **website_visitors** - Visitor tracking and behavior
- **website_events** - Detailed event tracking

### Social Media Tables
- **social_media_accounts** - Connected social accounts
- **social_media_posts** - Posted content
- **ad_campaigns** - Social media advertising campaigns

### Content Tables
- **ai_generated_content** - AI-created content history
- **content_assets** - Business images, videos, and files
- **email_templates** - Email campaign templates
- **sms_templates** - SMS campaign templates

## 🔒 Security Features

- **JWT Authentication** - Secure API access
- **CORS Protection** - Cross-origin request security
- **Input Validation** - Pydantic model validation
- **SQL Injection Prevention** - SQLAlchemy ORM protection
- **Rate Limiting** - API endpoint protection
- **Environment Variables** - Secure credential management

## 🚀 Deployment

### Production Deployment

1. **Environment Setup**
```bash
# Set production environment variables
export ENVIRONMENT=production
export DEBUG=False
export DATABASE_URL=your_production_database_url
```

2. **Database Migration**
```bash
python create_db.py
```

3. **Start with Gunicorn**
```bash
pip install gunicorn
gunicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Deployment

```dockerfile
# Dockerfile example
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["gunicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🧪 Testing

### Run Backend Tests
```bash
cd backend
pytest
```

### Run Frontend Tests
```bash
cd frontend
npm test
```

## 📈 Performance Monitoring

The platform includes built-in analytics for:
- API response times
- Database query performance
- Campaign delivery rates
- User engagement metrics
- System resource usage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- 📧 Email: support@marketmate.com
- 📖 Documentation: [View API Docs](http://localhost:8000/docs)
- 🐛 Issues: [GitHub Issues](https://github.com/SSIDDIQUE2k/MarketMate/issues)

## 🎉 Acknowledgments

- **NVIDIA** for hosting the hackathon and providing the opportunity to build this platform
- **OpenAI** for GPT-4 API
- **FastAPI** for the excellent web framework
- **React** team for the frontend framework
- **PostgreSQL** for reliable data storage
- All the amazing open-source libraries that make this possible

---

**Built with ❤️ for the NVIDIA Hackathon by SSIDDIQUE2k**

*MarketMate - Empowering businesses with AI-driven marketing automation* 🚀
