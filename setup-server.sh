#!/bin/bash

# 🛠️ Initial Server Setup Script
# Run this ONCE on the server (64.225.113.174)

set -e

echo "🛠️ Starting server setup for Discipline AI..."

# Update system
echo "📦 Updating system..."
apt update && apt upgrade -y

# Install Python 3.11
echo "🐍 Installing Python 3.11..."
apt install -y python3.11 python3.11-venv python3-pip python3-dev

# Install Node.js 20
echo "📦 Installing Node.js 20..."
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs

# Install Nginx
echo "🌐 Installing Nginx..."
apt install -y nginx

# Install PM2
echo "⚡ Installing PM2..."
npm install -g pm2

# Install Git
echo "📚 Installing Git..."
apt install -y git

# Install Certbot for SSL
echo "🔒 Installing Certbot..."
apt install -y certbot python3-certbot-nginx

# Create project directory
echo "📁 Creating project directory..."
mkdir -p /var/www
cd /var/www

# Clone repository (TODO: Replace with actual GitHub URL)
echo "📥 Cloning repository..."
# git clone https://github.com/YOUR_USERNAME/discipline-ai.git
echo "⚠️  Please clone repository manually:"
echo "   cd /var/www"
echo "   git clone https://github.com/YOUR_USERNAME/discipline-ai.git"

# Setup firewall
echo "🔥 Configuring firewall..."
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

echo "✅ Server setup completed!"
echo ""
echo "Next steps:"
echo "1. Clone the repository: cd /var/www && git clone https://github.com/YOUR_USERNAME/discipline-ai.git"
echo "2. Run: cd /var/www/discipline-ai && chmod +x init-backend.sh && ./init-backend.sh"
echo "3. Run: cd /var/www/discipline-ai && chmod +x init-frontend.sh && ./init-frontend.sh"
echo "4. Run: chmod +x setup-nginx.sh && ./setup-nginx.sh"
echo "5. Setup SSL: certbot --nginx -d yourdomain.com"
