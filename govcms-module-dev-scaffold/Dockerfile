# Stage 1: Base image
FROM govcms/govcms:10.x-latest as base

# Copy core files and configuration from the "govcms/govcms" image
COPY --from=drupal:10.2-php8.2-apache /opt/drupal/web/core/install.php /app/web/core/install.php

# Stage 2: Final image
FROM govcmstesting/ci:8.2-apache

RUN apt-get update && apt-get install -y vim ranger && apt-get clean

# Customize Drupal installation
RUN set -eux; \
    rm -rf /var/www/html; \
    mkdir -p /app/web/sites; \
    ln -sf /app/web /var/www/html;
# Customize Drupal installation
RUN set -eux; \
    groupadd -r govcms && useradd -r -g govcms -G root,www-data govcms;

# Customize Drupal installation
RUN set -eux; \
    mkdir -p /app/config/default; \
    chown -R govcms:govcms /app/config; \
    chown -R govcms:govcms /app/web/sites; \
    mkdir -p /home/govcms; \
    chown -R govcms:govcms /home/govcms;

# Copy contents from the "base" stage to "/app/"
COPY --from=base --chown=govcms:govcms /app /app
# Set environment variables
ENV SIMPLETEST_BASE_URL="http://localhost"
ENV SIMPLETEST_DB='mysql://drupal:drupal@mariadb/drupal'

# Set the working directory to "/app/"
WORKDIR /app/

RUN composer install

USER govcms
