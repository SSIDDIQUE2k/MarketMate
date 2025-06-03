#!/bin/bash

echo "🗄️  Setting up PostgreSQL database for AI Marketing Automation Platform"
echo "======================================================================="

# Check if PostgreSQL is running
if ! pgrep -x "postgres" > /dev/null; then
    echo "Starting PostgreSQL..."
    brew services start postgresql || sudo service postgresql start || systemctl start postgresql
fi

# Wait a moment for PostgreSQL to start
sleep 2

# Create database user if it doesn't exist
echo "Creating database user 'marketinguser'..."
createuser -s marketinguser 2>/dev/null || echo "User already exists"

# Set password for the user
echo "Setting password for user..."
psql -c "ALTER USER marketinguser PASSWORD 'marketing123';" postgres 2>/dev/null || echo "Password set or user updated"

# Create database
echo "Creating database 'marketing_automation'..."
createdb -O marketinguser marketing_automation 2>/dev/null || echo "Database already exists"

# Update .env file with correct credentials
echo "Updating .env file..."
if [ -f .env ]; then
    # Update the DATABASE_URL in .env file
    sed -i.backup 's|DATABASE_URL=.*|DATABASE_URL=postgresql://marketinguser:marketing123@localhost:5432/marketing_automation|' .env
    echo "✅ Database setup complete!"
    echo ""
    echo "Database credentials:"
    echo "  User: marketinguser"
    echo "  Password: marketing123"
    echo "  Database: marketing_automation"
    echo "  URL: postgresql://marketinguser:marketing123@localhost:5432/marketing_automation"
else
    echo "❌ .env file not found. Please run the main setup script first."
    exit 1
fi 