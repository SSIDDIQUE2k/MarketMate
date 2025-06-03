#!/bin/bash

echo "🚀 Setting up AI Marketing Automation Platform"
echo "================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL not found. Please install PostgreSQL first."
    echo "   Ubuntu/Debian: sudo apt-get install postgresql postgresql-contrib"
    echo "   macOS: brew install postgresql"
    echo "   Windows: Download from https://www.postgresql.org/download/"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Setup Backend
echo ""
echo "🔧 Setting up Backend..."
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create uploads directory
mkdir -p uploads

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cat > .env << EOL
DATABASE_URL=postgresql://user:password@localhost:5432/marketing_automation
OPENAI_API_KEY=your_openai_api_key_here
SENDGRID_API_KEY=your_sendgrid_api_key_here
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_APP_SECRET=your_facebook_app_secret
JWT_SECRET_KEY=your_jwt_secret_key_here
ALLOWED_ORIGINS=http://localhost:3000,http://192.168.4.42:3000
EOL
    echo "⚠️  Please update the .env file with your actual API keys!"
fi

# Setup database
echo "🗄️  Setting up database..."
echo "Please create a PostgreSQL database named 'marketing_automation'"
echo "You can do this by running: createdb marketing_automation"

cd ..

# Setup Frontend
echo ""
echo "🎨 Setting up Frontend..."
cd frontend

# Install dependencies
npm install

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Update backend/.env with your API keys"
echo "2. Create PostgreSQL database: createdb marketing_automation"
echo "3. Start the backend: cd backend && python main.py"
echo "4. Start the frontend: cd frontend && npm start"
echo ""
echo "🌐 Access the platform at:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📚 For tracking script: http://localhost:8000/tracking-script/{business_id}"
echo ""
echo "Happy marketing! 🚀" 