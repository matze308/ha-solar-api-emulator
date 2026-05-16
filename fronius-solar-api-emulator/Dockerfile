ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG C.UTF-8

RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-aiohttp \
    py3-requests

WORKDIR /app
COPY app/ /app/

RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]
