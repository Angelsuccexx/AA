#!/bin/bash

# deploy.sh - Automated deployment script for Cybersecurity Dashboard

echo "🚀 Starting deployment process..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[$(date +'%T')]${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    print_status "Initializing git repository..."
    git init
    print_success "Git repository initialized"
fi

# Check if remote origin is set
if ! git remote get-url origin > /dev/null 2>&1; then
    print_warning "No remote origin set. Please set it with:"
    echo "git remote add origin https://github.com/yourusername/cybersecurity-dashboard.git"
    exit 1
fi

# Get commit message from user or use default
if [ -z "$1" ]; then
    COMMIT_MSG="Update: $(date +'%Y-%m-%d %H:%M:%S')"
else
    COMMIT_MSG="$1"
fi

print_status "Starting deployment with commit: $COMMIT_MSG"

# Check for changes
if git diff-index --quiet HEAD --; then
    print_warning "No changes to deploy"
    exit 0
fi

print_status "Staging changes..."
git add .

print_status "Creating commit..."
git commit -m "$COMMIT_MSG"

print_status "Pushing to remote repository..."
if git push origin main; then
    print_success "Successfully deployed to repository!"
    print_success "Your dashboard is now live on Railway!"
else
    print_error "Failed to push to repository"
    exit 1
fi

echo ""
print_success "🎉 Deployment complete!"
print_status "Next steps:"
echo "  1. Check Railway dashboard for build status"
echo "  2. Visit your live application URL"
echo "  3. Test all functionality"