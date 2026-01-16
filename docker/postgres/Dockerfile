FROM postgres:17-bookworm

COPY docker/postgres/init/ /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/*.sh 2>/dev/null || true