#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 \
     -v db_name="$POSTGRES_DB" \
     -v db_user="$POSTGRES_USER" \
     -v db_password="'$POSTGRES_PASSWORD'" \
     --username "postgres" \
     -f /docker-entrypoint-initdb.d/init.sql