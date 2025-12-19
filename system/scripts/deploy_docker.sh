#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FreelancerOS: Docker Deployment Script
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

set -e

echo "🚀 FreelancerOS Agent Deployment Script"
echo "========================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "⚠️  docker-compose not found. Using 'docker compose' instead."
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ Created .env file. Please edit it with your credentials."
        echo "   Then run this script again."
        exit 0
    else
        echo "❌ .env.example not found. Cannot continue."
        exit 1
    fi
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p data logs

# Build the Docker image
echo "🔨 Building Docker image..."
$DOCKER_COMPOSE build

# Start the service
echo "🚀 Starting FreelancerOS Agent..."
$DOCKER_COMPOSE up -d

# Show status
echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Service Status:"
$DOCKER_COMPOSE ps

echo ""
echo "📝 To view logs:"
echo "   $DOCKER_COMPOSE logs -f"
echo ""
echo "🛑 To stop the agent:"
echo "   $DOCKER_COMPOSE down"
echo ""
echo "🔄 To restart the agent:"
echo "   $DOCKER_COMPOSE restart"
