#!/bin/bash
set -eo pipefail  # Better error catching for piped commands
echo "[DB BACKUP] Starting..."

ENV_DIR="/home/richie/env/common_infra"
BACKUP_DIR="/home/richie/pi-backups"
CONTAINER_NAME="mysql"

# rclone remote
RCLONE_REMOTE="master_rasp_node:pi-backups"

# Load env files
set -a
source /home/richie/env/common_infra/.env
set +a

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="$BACKUP_DIR/mysql_${TIMESTAMP}.sql"


# ... [Your existing variables] ...

# FIX 1: Use a safer way to pass the password
# This uses the container's internal environment variable directly
DOCKER_CMD="mysqldump -u root -p\"\$MYSQL_ROOT_PASSWORD\" mysql"
echo "[DB BACKUP] Executing dump..."
# FIX 2: pipefail ensures if mysqldump fails, the script stops
docker exec $CONTAINER_NAME sh -c "$DOCKER_CMD" > "$BACKUP_FILE"

# FIX 3: Use 'copy' instead of 'sync' to prevent accidental remote deletions
echo "[DB BACKUP] Copying to Google Drive..."
rclone copy "$BACKUP_DIR" "$RCLONE_REMOTE" --progress

# Optional: Add local cleanup so your disk doesn't fill up
# find "$BACKUP_DIR" -type f -mtime +7 -delete

echo "[DB BACKUP] Complete"