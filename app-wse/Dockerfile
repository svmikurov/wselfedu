FROM python:3.10.12-alpine
WORKDIR /app-wse

RUN apk add postgresql-client build-base postgresql-dev

COPY requirements.txt ./app-wse/requirements.txt
RUN pip install -r ./app-wse/requirements.txt

#RUN adduser --disabled-password service-user
#USER service-user

COPY . ./app-wse