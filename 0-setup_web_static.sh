#!/usr/bin/env bash
# Set up web servers for the deployment of web_static
sudo apt-get update
sudo apt-get -y install nginx
sudo apt-get -y install ufw
sudo ufw allow "Nginx HTTP"

sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
sudo touch /data/web_static/releases/test/index.html
echo "Everything is working good"  | sudo tee /data/web_static/releases/test/index.html
sudo ln -sf /data/web_static/releases/test /data/web_static/current
if id "ubuntu" &>/dev/null; then
    sudo chown -R ubuntu:ubuntu /data/
else
    echo "User 'ubuntu' does not exist. Skipping ownership change."
fi
sudo sed -i "/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}" /etc/nginx/sites-enabled/default
sudo service nginx restart
