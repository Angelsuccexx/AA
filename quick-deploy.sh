#!/bin/bash
# quick-deploy.sh - Quick deployment script

echo "🚀 Quick deploying changes..."

# Add all changes
git add .

# Commit with timestamp
git commit -m "Quick deploy: $(date +'%Y-%m-%d %H:%M:%S')"

# Push to main branch
git push origin main

echo "✅ Changes deployed!"