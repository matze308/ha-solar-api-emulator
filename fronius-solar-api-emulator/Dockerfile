ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base-python:3.11-alpine3.17
FROM $BUILD_FROM

ENV LANG C.UTF-8

RUN pip3 install --no-cache-dir aiohttp

WORKDIR /app
COPY app/ /app/

RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]
