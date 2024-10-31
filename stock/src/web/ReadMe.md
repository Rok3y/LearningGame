# Deployment

## Requirements 
* source myappenv/bin/activate
* pip install -r requirements.txt
* pip install gunicorn
* Add gunicorn_config.py file
* Run: 
> gunicorn --config gunicorn_config.py app:server (But does not work yet, check configuraiton)
* sudo apt install nginx

## Configuration
* sudo vim /etc/nginx/sites-available/finance-web
* add this to the config:

```
    server {
        listen 80;
        server_name yourdomain.com;

        location / {
            proxy_pass http://localhost:8080;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
```

* Create symlink
> sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
* Test the configuration for errors
> sudo nginx -t  
> sudo systemctl restart nginx

## Secure Your Application with SSL/TLS
> sudo apt install certbot python3-certbot-nginx

##### Firewall
> sudo ufw allow http https 'Nginx Full'

> sudo certbot --nginx -d finance.smod.si

### update 
sudo apt update && sudo apt upgrade

### Run web 

* cd LearningGame/
* source .venv/bin/activate
* cd stock/src/web/
> gunicorn --config gunicorn_config.py app:server