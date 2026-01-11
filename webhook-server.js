#!/usr/bin/env node

/**
 * Simple GitHub Webhook Server for Auto-Deployment
 *
 * Setup:
 * 1. Install: npm install -g express body-parser
 * 2. Run with PM2: pm2 start webhook-server.js --name discipline-webhook
 * 3. Configure GitHub webhook: http://YOUR_SERVER_IP:9000/webhook
 * 4. Set webhook secret in GitHub settings
 */

const express = require('express');
const bodyParser = require('body-parser');
const { execSync } = require('child_process');
const crypto = require('crypto');

const app = express();
const PORT = 9000;
const WEBHOOK_SECRET = process.env.WEBHOOK_SECRET || 'change_this_secret';
const DEPLOY_SCRIPT = '/root/deploy-discipline.sh';

app.use(bodyParser.json());

// Verify GitHub webhook signature
function verifySignature(req) {
  const signature = req.headers['x-hub-signature-256'];
  if (!signature) return false;

  const hmac = crypto.createHmac('sha256', WEBHOOK_SECRET);
  const digest = 'sha256=' + hmac.update(JSON.stringify(req.body)).digest('hex');

  return crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(digest));
}

// Webhook endpoint
app.post('/webhook', (req, res) => {
  console.log('📨 Webhook received');

  // Verify signature
  if (!verifySignature(req)) {
    console.log('❌ Invalid signature');
    return res.status(401).send('Unauthorized');
  }

  const event = req.headers['x-github-event'];
  const branch = req.body.ref;

  console.log(`Event: ${event}, Branch: ${branch}`);

  // Only deploy on push to main branch
  if (event === 'push' && branch === 'refs/heads/main') {
    console.log('🚀 Triggering deployment...');

    try {
      const output = execSync(DEPLOY_SCRIPT, { encoding: 'utf-8' });
      console.log(output);
      res.status(200).send('Deployment triggered successfully');
    } catch (error) {
      console.error('❌ Deployment failed:', error.message);
      res.status(500).send('Deployment failed');
    }
  } else {
    res.status(200).send('No deployment triggered');
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(200).send('OK');
});

app.listen(PORT, () => {
  console.log(`🎯 Webhook server listening on port ${PORT}`);
  console.log(`📍 Webhook URL: http://YOUR_SERVER_IP:${PORT}/webhook`);
  console.log(`🔐 Secret: ${WEBHOOK_SECRET}`);
});
