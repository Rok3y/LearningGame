#!/bin/bash

# Create a date-stamped directory path
backup_path="/var/backups/mongodb_backups/$(date +'%m-%d-%y')"

# Dump the MongoDB database
mongodump --db prod_db --out "$backup_path"

# Upload to Google Drive
rclone copy "$backup_path" googledrive:db_backup --progress

# Optional: clean up local backup files if you don't want to keep them
# rm -r "$backup_path"
