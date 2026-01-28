#!/bin/bash
set -e

# --- 1. Start Apache config for HTTP + HTTPS ---
# Enable SSL module
a2enmod ssl

# Create SSL folder
mkdir -p /etc/apache2/ssl

# Generate self-signed certificate (Alex Pascal, Brno)
openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout /etc/apache2/ssl/apache.key \
  -out /etc/apache2/ssl/apache.crt \
  -subj "/C=CZ/ST=Brno/L=Brno/O=AlexPascal/OU=Dev/CN=localhost"

# # --- 2. Update ports.conf to listen on 8080 (HTTP) and 8443 (HTTPS) ---
# sed -i '/Listen 80/c\Listen 8080' /etc/apache2/ports.conf
# grep -q "Listen 8443" /etc/apache2/ports.conf || echo "Listen 8443" >> /etc/apache2/ports.conf

# # --- 3. Create or modify SSL VirtualHost ---
# SSL_CONF="/etc/apache2/sites-available/default-ssl.conf"

# cat > $SSL_CONF <<EOL
# <VirtualHost *:8443>
#     ServerAdmin webmaster@localhost
#     DocumentRoot /var/www/html

#     SSLEngine on
#     SSLCertificateFile      /etc/apache2/ssl/apache.crt
#     SSLCertificateKeyFile   /etc/apache2/ssl/apache.key

#     <Directory /var/www/html>
#         Options Indexes FollowSymLinks
#         AllowOverride All
#         Require all granted
#     </Directory>
# </VirtualHost>
# EOL

# # Enable SSL site
# a2ensite default-ssl

# --- 4. Start Apache in foreground ---
apache2ctl -D FOREGROUND & # does not actually works

# --- 5. Start LXDE desktop with VNC ---
/startup.sh
