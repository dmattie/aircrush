ARG APACHE_VERSION=""
FROM httpd:${APACHE_VERSION:+${APACHE_VERSION}-}alpine

RUN apk update; \
    apk upgrade;

# Copy apache vhost file to proxy php requests to php-fpm container
COPY local.apache.conf /usr/local/apache2/conf/local.apache.conf
RUN echo "Include /usr/local/apache2/conf/local.apache.conf" \
    >> /usr/local/apache2/conf/httpd.conf
RUN ls /usr/local
RUN mkdir /usr/local/drupal_sync
RUN chmod a+w /usr/local/drupal_sync
RUN mkdir -p /var/www/html/sites/default/files/config_Z4M5xDXtp7oR0EqUCjwQMhk81aieDILyI6O2SeKlRy4JxfhMJGx1-jnLEjss2cxmEN_MzkbxaQ/sync
RUN chmod a+w -R /var/www/html/sites/default/files

#http://aircrush/admin/config/services/jsonapi

# RUN drush config:set system.site page.front node
#https://drushcommands.com/drush-9x/config/config:set/
#Email, homepage
    
