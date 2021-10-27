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


    
