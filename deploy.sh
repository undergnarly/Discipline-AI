#!/bin/bash

# 🚀 Deployment Script for Discipline AI
# Server: 64.225.113.174

set -e  # Exit on error

# Configuration
SERVER_USER="root"
SERVER_HOST="64.225.113.174"
PROJECT_DIR="/var/www/discipline-ai"
FRONTEND_DIR="$PROJECT_DIR/frontend"
BACKEND_DIR="$PROJECT_DIR/backend"

echo "🚀 Starting deployment to $SERVER_HOST..."

# Step 1: Commit and push current changes
echo "📝 Committing changes..."
git add .
git commit -m "Deploy: $(date '+%Y-%m-%d %H:%M:%S')" || echo "No changes to commit"
git push origin main

# Step 2: Deploy to server
echo "🌐 Deploying to server..."

ssh "$SERVER_USER@$SERVER_HOST" << 'ENDSSH'
    set -e

    echo "📦 Pulling latest code..."
    cd /var/www/discipline-ai
    git pull origin main

    echo "🔧 Updating backend..."
    cd backend
    source venv/bin/activate
    pip install -r requirements.txt --quiet

    echo "🔄 Restarting backend service..."
    systemctl restart discipline-ai-backend

    echo "🎨 Updating frontend..."
    cd ../frontend
    npm install --silent
    npm run build

    echo "🔄 Restarting frontend service..."
    pm2 restart discipline-ai-frontend

    echo "✅ Deployment completed successfully!"
ENDSSH

echo "✨ Deployment finished!"
echo "🌐 Check your app at: http://64.225.113.174"
