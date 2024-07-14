FROM python:3.12-bookworm

WORKDIR /app-wse

RUN pip install --upgrade pip && \
    pip install playwright && \
    pip install pytest-playwright==0.5.0 && \
    playwright install && \
    playwright install-deps

COPY requirements.txt ./app-wse/requirements.txt
RUN pip install -r ./app-wse/requirements.txt

#RUN adduser --disabled-password app-user
#USER app-user

COPY . ./app-wse