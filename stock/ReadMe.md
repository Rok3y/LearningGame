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