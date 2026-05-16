#!/usr/bin/with-contenv bashio

export PORT=$(bashio::config 'port')
export LOG_LEVEL=$(bashio::config 'log_level')
export SUPERVISOR_TOKEN="${SUPERVISOR_TOKEN}"

bashio::log.info "Starting Fronius Solar API Emulator on port ${PORT}"

exec python3 /app/server.py
