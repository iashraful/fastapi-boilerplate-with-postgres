FROM python:3.9.6-alpine
RUN apk update && \
    apk add --virtual build-base gcc g++ python3-dev libressl-dev musl-dev libffi-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd py-pip jpeg-dev zlib-dev

WORKDIR /app
COPY requirements.txt /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt