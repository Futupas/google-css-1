FROM dorowu/ubuntu-desktop-lxde-vnc

RUN echo 'deb [trusted=yes] http://dl.google.com/linux/chrome/deb stable main' > /etc/apt/sources.list.d/google-chrome.list

RUN apt-get update --allow-unauthenticated && \
    apt-get install -y --allow-unauthenticated apache2 php wireshark tshark

RUN mkdir -p /etc/apache2/ssl && \
    openssl req -x509 -nodes -days 365 \
    -newkey rsa:2048 \
    -keyout /etc/apache2/ssl/apache.key \
    -out /etc/apache2/ssl/apache.crt \
    -subj "/C=CZ/ST=Brno/L=Brno/O=AlexPascal/OU=Dev/CN=localhost"

RUN a2enmod ssl && a2ensite default-ssl

# Expose ports
EXPOSE 80 8080 8443 6080 5901

# Use our startup script
CMD ["/startup.sh"]
# CMD ["/start.sh"]
