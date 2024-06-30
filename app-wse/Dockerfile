FROM python:3.10.12-slim
WORKDIR /app-wse
COPY requirements.txt ./requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
COPY . ./app-wse