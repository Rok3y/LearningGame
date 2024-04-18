## Python env

Python version
> Python 3.12.2

Create virtual environment here in stock folder
> python3 -m venv .venv

Activate virtual environemtn
> source .venv/bin/activate

Install libraries
> pip3 install -r requirements.txt

## Database

Database service
> systemctl status mongod

Database shell
mongosh
> 

Database logs
> tail -n 15 /var/log/mongodb/mongod.log # for the last 15 lines

## Database backup

To make a backup run command:
> sudo mkdir /var/backups/mongodb_backups
> backup_path="/var/backups/mongodb_backups/$(date +'%m-%d-%y')"
> sudo mongodump --db prod_db --out "$backup_path"

### To automate 

Install 'rclone' that manage files on cloud storage
> rclone copy "$backup_path" googledrive:db_backup --progress

Since I cannot authenticate on no-gui machine (linux terminal) follow these steps:

* Install rclone.exe on windows
* Run: > .\rclone.exe config
* give name, then everything should be default
* Copy `C:\\Users\\rivancic\\AppData\\Roaming\\rclone\\rclone.conf` to linux VM `/home/roki/.config/rclone/rclone.conf`

> Run `backup.sh ` script

Next you can create scheduled job:

* Open the crontab editor:
* 0 3 * * * /path/to/backup_and_upload.sh (Schedule your script to run at your preferred time, for example, daily at 3 AM:)
* save and exit the editor
