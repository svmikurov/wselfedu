FROM python:3.13-slim

WORKDIR /docs

COPY docker/docs/requirements.txt /temp/requirements.txt
RUN pip3 install -r /temp/requirements.txt --no-cache-dir

COPY docs/source /docs/source

RUN sphinx-build /docs/source /docs/build/html

COPY docker/docs/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]