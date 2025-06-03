#!/bin/bash

echo "🚀 Starting AI Marketing Automation Backend"
echo "============================================"

# Navigate to backend directory
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/upgrade dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create uploads directory if it doesn't exist
mkdir -p uploads

# Check if .env exists, if not copy from sample
if [ ! -f .env ]; then
    if [ -f sample.env ]; then
        echo "Creating .env file from sample..."
        cp sample.env .env
        echo "⚠️  Please update the .env file with your actual API keys!"
    else
        echo "❌ .env file not found!"
        echo "Please create a .env file with your configuration."
        echo "See the README.md for required environment variables."
        exit 1
    fi
fi

# Check if database tables exist, create if not
echo "Setting up database..."
python create_db.py

# Start the server
echo "🎉 Starting FastAPI server..."
echo "Backend will be available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
python main.py 