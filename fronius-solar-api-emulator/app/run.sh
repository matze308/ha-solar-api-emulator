#!/usr/bin/with-contenv bashio

export PORT=$(bashio::config 'port')
export LOG_LEVEL=$(bashio::config 'log_level')
export SUPERVISOR_TOKEN="${SUPERVISOR_TOKEN}"

export SENSOR_PV=$(bashio::config 'sensor_pv')
export SENSOR_POWER=$(bashio::config 'sensor_power')
export SENSOR_GRID=$(bashio::config 'sensor_grid')
export SENSOR_SOC=$(bashio::config 'sensor_soc')
export SENSOR_BATTERY=$(bashio::config 'sensor_battery')
export SENSOR_PRODUCTION_TODAY=$(bashio::config 'sensor_production_today')

bashio::log.info "Starting Fronius Solar API Emulator on port ${PORT}"
bashio::log.info "Sensors: PV=${SENSOR_PV}, Power=${SENSOR_POWER}, Grid=${SENSOR_GRID}"
bashio::log.info "         SOC=${SENSOR_SOC}, Battery=${SENSOR_BATTERY}, Today=${SENSOR_PRODUCTION_TODAY}"

exec python3 /app/server.py
