#!/bin/bash
set -e

echo "[DB BACKUP] Starting..."

ENV_DIR="/home/richie/env"
BACKUP_DIR="/home/richie/db_backups"
CONTAINER_NAME="common-infra"

# rclone remote
RCLONE_REMOTE="master_rasp_node:pi-backups"

mkdir -p "$BACKUP_DIR"

# Load env files
for f in "$ENV_DIR"/*.env; do
  [ -f "$f" ] && source "$f"
done

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="$BACKUP_DIR/mysql_${TIMESTAMP}.sql"

echo "[DB BACKUP] Dumping MySQL → $BACKUP_FILE"

docker exec "$CONTAINER_NAME" \
  mysqldump -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" \
  > "$BACKUP_FILE"

echo "[DB BACKUP] Backup created successfully"

# ---- Sync to Google Drive ----
echo "[DB BACKUP] Syncing to Google Drive..."

rclone sync "$BACKUP_DIR" "$RCLONE_REMOTE"

echo "[DB BACKUP] Google Drive sync complete"

exit 0
