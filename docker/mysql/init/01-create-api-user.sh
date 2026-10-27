#!/bin/sh
set -eu

app_password="$(cat /run/secrets/mysql_app_password)"
case "${MYSQL_DATABASE:-}" in
    ''|*[!a-zA-Z0-9_]*)
        echo "MYSQL_DATABASE must contain only letters, digits, and underscores" >&2
        exit 1
        ;;
esac

case "$app_password" in
    ''|*[!a-fA-F0-9]*)
        echo "mysql_app_password must contain only hexadecimal characters" >&2
        exit 1
        ;;
esac

MYSQL_PWD="$MYSQL_ROOT_PASSWORD" mysql --protocol=socket -uroot <<SQL
CREATE USER IF NOT EXISTS 'classicmodels_api'@'%' IDENTIFIED BY '${app_password}';
ALTER USER 'classicmodels_api'@'%' IDENTIFIED BY '${app_password}';
GRANT SELECT ON ${MYSQL_DATABASE}.* TO 'classicmodels_api'@'%';
SQL
