#!/bin/bash
# set -e

# a2enmod ssl

# mkdir -p /etc/apache2/ssl

# openssl req -x509 -nodes -days 365 \
#   -newkey rsa:2048 \
#   -keyout /etc/apache2/ssl/apache.key \
#   -out /etc/apache2/ssl/apache.crt \
#   -subj "/C=CZ/ST=Brno/L=Brno/O=AlexPascal/OU=Dev/CN=localhost"

# Start Apache
service apache2 start

# Launch desktop + VNC
/startup.sh
