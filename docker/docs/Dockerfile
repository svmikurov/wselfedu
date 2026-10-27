FROM python:3.13-slim

WORKDIR /docs

COPY docker/docs/requirements.txt /tmp/requirements.txt
RUN python -m pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

COPY docs/source /docs/source
RUN sphinx-build /docs/source /docs/build/html

COPY --chmod=0755 docker/docs/entrypoint.sh /entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]