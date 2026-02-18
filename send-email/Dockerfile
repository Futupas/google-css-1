FROM php:8.2-apache

RUN apt-get update && apt-get install -y zip unzip git && rm -rf /var/lib/apt/lists/*
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

WORKDIR /var/www/html
COPY . .
RUN composer install --no-interaction --no-scripts
RUN mv .env ..
EXPOSE 80
