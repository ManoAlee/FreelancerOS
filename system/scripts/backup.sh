#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FreelancerOS: Automated Backup Script
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

set -e

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BACKUP_DIR="${PROJECT_DIR}/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_NAME="freelanceros_backup_${TIMESTAMP}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔄 FreelancerOS Backup Script"
echo "============================="
echo ""

# Create backup directory
mkdir -p "${BACKUP_DIR}"

# Create temporary backup location
TEMP_BACKUP="${BACKUP_DIR}/${BACKUP_NAME}"
mkdir -p "${TEMP_BACKUP}"

echo "📦 Backing up to: ${TEMP_BACKUP}"
echo ""

# Backup database
if [ -f "${PROJECT_DIR}/data/agent_memory.db" ]; then
    echo -e "${GREEN}✓${NC} Backing up database..."
    cp "${PROJECT_DIR}/data/agent_memory.db" "${TEMP_BACKUP}/"
else
    echo -e "${YELLOW}⚠${NC} Database not found, skipping..."
fi

# Backup logs (last 7 days)
if [ -d "${PROJECT_DIR}/logs" ]; then
    echo -e "${GREEN}✓${NC} Backing up logs..."
    mkdir -p "${TEMP_BACKUP}/logs"
    find "${PROJECT_DIR}/logs" -type f -mtime -7 -exec cp {} "${TEMP_BACKUP}/logs/" \;
else
    echo -e "${YELLOW}⚠${NC} Logs directory not found, skipping..."
fi

# Backup configuration (excluding sensitive data)
if [ -f "${PROJECT_DIR}/.env.example" ]; then
    echo -e "${GREEN}✓${NC} Backing up configuration template..."
    cp "${PROJECT_DIR}/.env.example" "${TEMP_BACKUP}/"
fi

if [ -f "${PROJECT_DIR}/projects/auto_agent/config.yaml" ]; then
    echo -e "${GREEN}✓${NC} Backing up agent config..."
    cp "${PROJECT_DIR}/projects/auto_agent/config.yaml" "${TEMP_BACKUP}/"
fi

# Create backup metadata
echo -e "${GREEN}✓${NC} Creating backup metadata..."
cat > "${TEMP_BACKUP}/backup_info.txt" << EOF
FreelancerOS Backup
===================
Date: $(date)
Hostname: $(hostname)
Project: FreelancerOS
EOF

# Add git info only if .git directory exists
if [ -d "${PROJECT_DIR}/.git" ]; then
    if cd "${PROJECT_DIR}" 2>/dev/null; then
        cat >> "${TEMP_BACKUP}/backup_info.txt" << EOF
Version: $(git describe --tags --always 2>/dev/null || echo "unknown")
Commit: $(git rev-parse HEAD 2>/dev/null || echo "unknown")
EOF
        cd - > /dev/null
    else
        echo -e "${YELLOW}⚠${NC} Could not access project directory for git info"
    fi
fi

cat >> "${TEMP_BACKUP}/backup_info.txt" << EOF

Contents:
- Database (agent_memory.db)
- Logs (last 7 days)
- Configuration files

Restore Instructions:
1. Extract this backup to your FreelancerOS directory
2. Copy agent_memory.db to data/
3. Copy logs to logs/
4. Reconfigure .env with your credentials
EOF

# Compress backup
echo ""
echo "🗜️  Compressing backup..."
cd "${BACKUP_DIR}"
tar -czf "${BACKUP_NAME}.tar.gz" "${BACKUP_NAME}"
rm -rf "${BACKUP_NAME}"

# Get backup size
BACKUP_SIZE=$(du -h "${BACKUP_NAME}.tar.gz" | cut -f1)

echo ""
echo -e "${GREEN}✅ Backup completed successfully!${NC}"
echo ""
echo "📊 Backup Details:"
echo "   File: ${BACKUP_NAME}.tar.gz"
echo "   Size: ${BACKUP_SIZE}"
echo "   Location: ${BACKUP_DIR}"
echo ""

# Cleanup old backups (keep last 30 days)
echo "🧹 Cleaning up old backups (keeping last 30 days)..."
find "${BACKUP_DIR}" -name "freelanceros_backup_*.tar.gz" -mtime +30 -delete
REMAINING=$(find "${BACKUP_DIR}" -name "freelanceros_backup_*.tar.gz" | wc -l)
echo "   Remaining backups: ${REMAINING}"

echo ""
echo "✅ Done!"
