#!/bin/bash

# Stop MongoDB service to avoid any access issues or conflicts

sudo systemctl stop mongod

# --drop flag will drop the database before restoring it. This is useful if you want to restore a backup to a new database.
sudo mongorestore --db prod_db /var/backups/mongodb_backups/$(ls -t /var/backups/mongodb_backups | head -n1)

sudo systemctl start mongod