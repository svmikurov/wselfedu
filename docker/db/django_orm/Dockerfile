# Database management via Django framework.

FROM python:3.13-slim

EXPOSE 8000

WORKDIR /app

COPY docker/db/django_orm/requirements.txt /temp/requirements.txt
RUN pip3 install -r /temp/requirements.txt --no-cache-dir

COPY src/wse/infrastructure/db/django_orm /app
COPY .env /app/.env