#!/bin/bash

# 🎨 Frontend Initialization Script
# Run this on the server after cloning the repository

set -e

echo "🎨 Initializing frontend..."

cd /var/www/discipline-ai/frontend

# Install dependencies
echo "📥 Installing dependencies..."
npm install

# Build for production
echo "🏗️  Building for production..."
npm run build

# Create .env.local
echo "🔐 Creating .env.local..."
cat > .env.local << 'EOF'
NEXT_PUBLIC_API_URL=http://64.225.113.174/api
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
EOF

# Start with PM2
echo "⚡ Starting with PM2..."
pm2 start npm --name "discipline-ai-frontend" -- start

# Save PM2 configuration
pm2 save

# Setup PM2 startup script
echo "⚙️  Configuring PM2 startup..."
pm2 startup | tail -n 1 > /tmp/pm2_startup.sh
# Run the command manually: pm2 startup

echo "✅ Frontend initialized!"
echo "🔍 Check status: pm2 status"
echo "📋 View logs: pm2 logs discipline-ai-frontend"
