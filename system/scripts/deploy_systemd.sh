#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FreelancerOS: Systemd Deployment Script
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

set -e

echo "🚀 FreelancerOS Systemd Deployment Script"
echo "=========================================="

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run as root (use sudo)"
    exit 1
fi

# Get the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
echo "📁 Project directory: $PROJECT_DIR"

# Check if .env exists
if [ ! -f "$PROJECT_DIR/.env" ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    if [ -f "$PROJECT_DIR/.env.example" ]; then
        cp "$PROJECT_DIR/.env.example" "$PROJECT_DIR/.env"
        echo "✅ Created .env file. Please edit it with your credentials."
        echo "   Location: $PROJECT_DIR/.env"
        echo "   Then run this script again."
        exit 0
    else
        echo "❌ .env.example not found. Cannot continue."
        exit 1
    fi
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p "$PROJECT_DIR/data" "$PROJECT_DIR/logs"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r "$PROJECT_DIR/system/requirements.txt"

# Create systemd service file
SERVICE_FILE="/etc/systemd/system/freelanceros-agent.service"
echo "📝 Creating systemd service file..."

cat > "$SERVICE_FILE" << EOF
[Unit]
Description=FreelancerOS Autonomous Agent
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=$SUDO_USER
Group=$SUDO_USER
WorkingDirectory=$PROJECT_DIR
Environment="PYTHONUNBUFFERED=1"
Environment="PYTHONPATH=$PROJECT_DIR"
EnvironmentFile=$PROJECT_DIR/.env

ExecStart=/usr/bin/python3 $PROJECT_DIR/projects/auto_agent/auto_main.py

Restart=always
RestartSec=10
StartLimitInterval=60
StartLimitBurst=5

StandardOutput=journal
StandardError=journal
SyslogIdentifier=freelanceros-agent

NoNewPrivileges=true
PrivateTmp=true
ReadWritePaths=$PROJECT_DIR/data $PROJECT_DIR/logs

[Install]
WantedBy=multi-user.target
EOF

echo "✅ Service file created: $SERVICE_FILE"

# Reload systemd
echo "🔄 Reloading systemd..."
systemctl daemon-reload

# Enable service
echo "✅ Enabling service..."
systemctl enable freelanceros-agent

# Start service
echo "🚀 Starting service..."
systemctl start freelanceros-agent

# Show status
echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Service Status:"
systemctl status freelanceros-agent --no-pager

echo ""
echo "📝 Useful commands:"
echo "   View logs:    sudo journalctl -u freelanceros-agent -f"
echo "   Stop:         sudo systemctl stop freelanceros-agent"
echo "   Start:        sudo systemctl start freelanceros-agent"
echo "   Restart:      sudo systemctl restart freelanceros-agent"
echo "   Disable:      sudo systemctl disable freelanceros-agent"
