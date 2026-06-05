#!/bin/bash
set -e

BACKUP_DIR="/home/richie/db_backups"
KEEP=20

echo "[BACKUP CLEANUP] Running..."

if [ ! -d "$BACKUP_DIR" ]; then
  echo "[BACKUP CLEANUP] Directory not found: $BACKUP_DIR"
  exit 0
fi

COUNT=$(ls -1 "$BACKUP_DIR"/mysql_*.sql 2>/dev/null | wc -l)

if [ "$COUNT" -le "$KEEP" ]; then
  echo "[BACKUP CLEANUP] Nothing to delete ($COUNT files)"
  exit 0
fi

ls -1t "$BACKUP_DIR"/mysql_*.sql | tail -n +$((KEEP+1)) | while read f; do
  echo "[BACKUP CLEANUP] Removing $f"
  rm -f "$f"
done

echo "[BACKUP CLEANUP] Done."

exit 0
