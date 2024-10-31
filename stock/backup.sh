#!/bin/bash

# Create a date-stamped directory path
backup_path="/var/backups/mongodb_backups/$(date +'%m-%d-%y')"
backup_path_tar="/var/backups/mongodb_backups/$(date +'%m-%d-%y').tar.gz"

# Dump the MongoDB database
mongodump --db prod_db --out "$backup_path"

tar -zcvf "$backup_path_tar" "$backup_path"

# Upload to Google Drive
rclone copy "$backup_path_tar" googledrive:db_backup --progress

# Optional: clean up local backup files if you don't want to keep them
# rm -r "$backup_path"
