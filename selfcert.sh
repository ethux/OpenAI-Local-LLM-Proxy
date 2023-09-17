#!/bin/bash

# Step 1: Install Nginx
sudo apt update
sudo apt install -y nginx

# Step 2: Create a Self-Signed SSL Certificate
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt

# Step 3: Configure Nginx to Use the SSL Certificate
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

# Step 4: Enable the Configuration
sudo ln -s /etc/nginx/sites-available/my_proxies /etc/nginx/sites-enabled/

# Step 5: Test the Nginx Configuration
sudo nginx -t

# Step 6: Reload Nginx
if [ $? -eq 0 ]; then
    sudo systemctl reload nginx
else
    echo "Nginx configuration test failed"
    exit 1
fi

# Step 7: Add the Self-Signed Certificate to Your System's List of Trusted Certificates (Linux)
sudo cp /etc/ssl/certs/nginx-selfsigned.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates

# Step 8: Output a message indicating the script has finished
echo "The setup is complete. Please test the setup by visiting your Nginx proxy in a web browser using HTTPS."
