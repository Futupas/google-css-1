FROM dorowu/ubuntu-desktop-lxde-vnc

# Install Apache, PHP, Wireshark
# RUN apt-get update && \
#     DEBIAN_FRONTEND=noninteractive apt-get install -y --allow-unauthenticated apache2 php wireshark && \
#     # Change Apache to listen on 8080
#     sed -i 's/80/8080/' /etc/apache2/ports.conf && \
#     sed -i 's/<VirtualHost \*:80>/<VirtualHost *:8080>/' /etc/apache2/sites-enabled/000-default.conf

RUN echo 'deb [trusted=yes] http://dl.google.com/linux/chrome/deb stable main' > /etc/apt/sources.list.d/google-chrome.list

# RUN apt-get update --allow-unauthenticated && \
#     apt-get install -y --allow-unauthenticated apache2 php wireshark tshark && \
#     # Change Apache to listen on 8080
#     sed -i 's/80/8080/' /etc/apache2/ports.conf && \
#     sed -i 's/<VirtualHost \*:80>/<VirtualHost *:8080>/' /etc/apache2/sites-enabled/000-default.conf

RUN apt-get update --allow-unauthenticated && \
    apt-get install -y --allow-unauthenticated apache2 php wireshark tshark python3-pip

RUN mkdir -p /etc/apache2/ssl && \
    openssl req -x509 -nodes -days 365 \
    -newkey rsa:2048 \
    -keyout /etc/apache2/ssl/apache.key \
    -out /etc/apache2/ssl/apache.crt \
    -subj "/C=CZ/ST=Brno/L=Brno/O=AlexPascal/OU=Dev/CN=localhost"

RUN a2enmod ssl && a2ensite default-ssl

RUN pip3 install asyncio websockets
# RUN pip3 install -r /opt/chat/requirements.txt

# # Copy startup script
# COPY start.sh /start.sh
# RUN chmod +x /start.sh

# Expose ports
EXPOSE 80 8080 5901

# Use our startup script
CMD ["/start.sh"]
