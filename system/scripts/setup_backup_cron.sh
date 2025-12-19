#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FreelancerOS: Setup Automated Backups via Cron
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BACKUP_SCRIPT="${PROJECT_DIR}/system/scripts/backup.sh"

echo "🔄 FreelancerOS - Setup Automated Backups"
echo "=========================================="
echo ""

# Check if backup script exists
if [ ! -f "$BACKUP_SCRIPT" ]; then
    echo "❌ Backup script not found: $BACKUP_SCRIPT"
    exit 1
fi

# Make sure script is executable
chmod +x "$BACKUP_SCRIPT"

echo "📅 Choose backup frequency:"
echo "  1) Daily at 2:00 AM"
echo "  2) Every 12 hours"
echo "  3) Every 6 hours"
echo "  4) Custom cron expression"
echo "  5) Cancel"
echo ""
read -p "Select option [1-5]: " choice

case $choice in
    1)
        CRON_EXPR="0 2 * * *"
        DESC="Daily at 2:00 AM"
        ;;
    2)
        CRON_EXPR="0 */12 * * *"
        DESC="Every 12 hours"
        ;;
    3)
        CRON_EXPR="0 */6 * * *"
        DESC="Every 6 hours"
        ;;
    4)
        echo ""
        echo "Enter custom cron expression (e.g., '0 3 * * 1' for every Monday at 3 AM):"
        read -p "> " CRON_EXPR
        DESC="Custom: $CRON_EXPR"
        ;;
    5)
        echo "❌ Cancelled"
        exit 0
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""
echo "Setting up backup schedule: $DESC"
echo "Cron expression: $CRON_EXPR"
echo ""

# Create cron job
CRON_JOB="$CRON_EXPR $BACKUP_SCRIPT >> ${PROJECT_DIR}/logs/backup.log 2>&1"

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "$BACKUP_SCRIPT"; then
    echo "⚠️  A cron job for this backup script already exists."
    read -p "Replace it? [y/N]: " replace
    if [[ ! "$replace" =~ ^[Yy]$ ]]; then
        echo "❌ Cancelled"
        exit 0
    fi
    # Remove existing job
    crontab -l | grep -v "$BACKUP_SCRIPT" | crontab -
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo ""
echo "✅ Backup cron job added successfully!"
echo ""
echo "📊 Current crontab:"
crontab -l | grep "$BACKUP_SCRIPT" || echo "  (no entries)"
echo ""
echo "📝 Backup logs will be written to: ${PROJECT_DIR}/logs/backup.log"
echo ""
echo "🔧 To manage cron jobs:"
echo "   List:   crontab -l"
echo "   Edit:   crontab -e"
echo "   Remove: crontab -r"
