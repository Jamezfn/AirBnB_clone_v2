#!/usr/bin/env bash
# Set up web servers for web_static deployment
apt-get update -y && apt-get install nginx -y
mkdir -p /data/web_static/shared /data/web_static/releases/test
echo "<html><head></head><body>ALX</body></html>" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test /data/web_static/current
chown -R ubuntu:ubuntu /data
sed -i '/server_name _;/a\\tlocation /hbnb_static { alias /data/web_static/current/; }' /etc/nginx/sites-available/default
service nginx restart
