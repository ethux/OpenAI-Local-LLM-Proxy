#!/bin/bash

#Install Nginx
sudo apt update
sudo apt install -y nginx

#Create a Self-Signed SSL Certificate
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt

#Configure Nginx to Use the SSL Certificate
sudo bash -c 'cat > /etc/nginx/sites-available/my_proxies <<EOF
server {
    listen 443 ssl;
    server_name api.openai.com;

    ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
    ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF'

#Enable the nginx config
sudo ln -s /etc/nginx/sites-available/my_proxies /etc/nginx/sites-enabled/

#Test the nginx config
sudo nginx -t

#Reload nginx
if [ $? -eq 0 ]; then
    sudo systemctl reload nginx
else
    echo "Nginx configuration test failed"
    exit 1
fi

#Add the Self-Signed Certificate to Trusted Certificates (Linux)
sudo cp /etc/ssl/certs/nginx-selfsigned.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates
