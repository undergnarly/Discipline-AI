#!/bin/bash

# 🔧 Backend Initialization Script
# Run this on the server after cloning the repository

set -e

echo "🔧 Initializing backend..."

cd /var/www/discipline-ai/backend

# Create virtual environment
echo "📦 Creating virtual environment..."
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file
echo "🔐 Creating .env file..."
cat > .env << 'EOF'
# Database
DATABASE_URL=sqlite+aiosqlite:///./discipline_ai.db

# JWT
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
FRONTEND_URL=http://64.225.113.174/discipline

# Google OAuth
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=http://64.225.113.174/api/auth/google/callback

# OpenAI
OPENAI_API_KEY=

# Anthropic
ANTHROPIC_API_KEY=

# Supabase
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
EOF

# Run migrations
echo "🗄️  Running database migrations..."
alembic upgrade head || echo "⚠️  No migrations to run"

# Create systemd service
echo "⚙️  Creating systemd service..."
cat > /etc/systemd/system/discipline-ai-backend.service << 'EOF'
[Unit]
Description=Discipline AI Backend FastAPI
After=network.target

[Service]
Type=notify
User=root
WorkingDirectory=/var/www/discipline-ai/backend
Environment="PATH=/var/www/discipline-ai/backend/venv/bin"
ExecStart=/var/www/discipline-ai/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
systemctl daemon-reload
systemctl enable discipline-ai-backend
systemctl start discipline-ai-backend

echo "✅ Backend initialized!"
echo "🔍 Check status: systemctl status discipline-ai-backend"
