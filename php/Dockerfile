ARG PHP_VERSION=""
FROM php:${PHP_VERSION:+${PHP_VERSION}-}fpm-alpine

RUN apk update; \
    apk upgrade;

RUN docker-php-ext-install opcache

# Install gd library extension
RUN apk add libpng libpng-dev libjpeg-turbo-dev libwebp-dev zlib-dev libxpm-dev gd && docker-php-ext-install gd    

# Install MySql
RUN docker-php-ext-install mysqli pdo pdo_mysql

# Install Composer
RUN curl -sS https://getcomposer.org/installer | php && \
    mv composer.phar /usr/local/bin/composer && \
    ln -s /root/.composer/vendor/bin/drush /usr/local/bin/drush

# Install Drush
RUN composer global require drush/drush && \
    composer global update 
#RUN composer require drupal/jsonapi_views

# PHP packages
RUN apk add --update \
        libressl \
        ca-certificates \
        openssh-client \
        rsync \
        git \
        curl \
        wget \
        gzip \
        tar \
        patch \
        perl \
        pcre \
        imap \
        imagemagick \
        mariadb-client \
        build-base \
        autoconf \
        libtool \
        php8-dev \
        pcre-dev \
        imagemagick-dev \
        php8 \
        php8-fpm \
        php8-opcache \
        php8-session \
        php8-dom \
        php8-xml \
        php8-xmlreader \
        php8-ctype \
        php8-ftp \
        php8-gd \
        php8-json \
        php8-posix \
        php8-curl \
        php8-pdo \
        php8-pdo_mysql \
        php8-sockets \
        php8-zlib \        
        php8-mysqli \
        php8-sqlite3 \
        php8-bz2 \
        php8-phar \
        php8-openssl \
        php8-posix \
        php8-zip \
        php8-calendar \
        php8-iconv \
        php8-imap \
        php8-soap \
        php8-dev \
        php8-pear \
        php8-redis \
        php8-mbstring \
        php8-xdebug \
        php8-exif \
        php8-xsl \
        php8-ldap \
        php8-bcmath \       
        php8-apcu
        # php8-memcached \
        #php8-oauth \
        #php8-mcrypt \

# Copy php.ini memory limit increase    
COPY php.ini /usr/local/etc/php/

#RUN composer require drupal/migrate_tools
#RUN composer require drupal/charts
#RUN drush en migrate
#RUN drush en unique_entity_title
#RUN drush en basic_auth