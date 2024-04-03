# Instructions

### Python version: 3.12.1

python -m venv venv
.\venv\Scripts\Activate.ps1


### Deploy docker

#### Build docker

docker build -t polltable-app .

#### Run docker

docker run -d -p 4000:8000 -v "C:\Users\rivancic\OneDrive - cosylab.com\database_cslpool.db:/usr/src/app/database.db" polltable-app

> Database is stored at https://cosylab0-my.sharepoint.com/:u:/r/personal/rok_ivancic_cosylab_com/Documents/database_cslpool.db?csf=1&web=1&e=zJd61o