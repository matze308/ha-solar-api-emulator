# Fronius Solar API Emulator - Home Assistant Addon

[![Version](https://img.shields.io/badge/version-1.0.4-blue.svg)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Ein Home Assistant Addon, das die Fronius Solar API V1 simuliert. Es emuliert einen Wechselrichter (Inverter), Batteriespeicher (Storage) und Smart Meter basierend auf echten Sensordaten aus Home Assistant.

## Features

- **Wechselrichter (Inverter):** `GetInverterRealtimeData`
- **Smart Meter:** `GetMeterRealtimeData`
- **Batteriespeicher:** `GetStorageRealtimeData`
- **PowerFlow:** `GetPowerFlowRealtimeData`
- **Logger Info:** `GetLoggerInfo`, `GetAPIVersion`
- **Aktive Geräte:** `GetActiveDeviceInfo`
- **Lokaler Build:** Kein externes Container-Image nötig
- **Beide URL-Varianten:** Antwortet auf `.cgi` und `.fcgi`
- **Konfigurierbare Sensoren:** Alle Entitätsnamen über die Add-on-Konfiguration einstellbar

## Verwendete Home Assistant Entitäten

Die folgenden Sensoren sind über die Add-on-Konfiguration anpassbar (Standardwerte):

| Option | Standard-Entität | Beschreibung |
|---|---|---|
| `sensor_pv` | `sensor.solar_manager_power_pv` | PV-Leistung (W) |
| `sensor_power` | `sensor.solar_manager_power` | Hausverbrauch (W) |
| `sensor_grid` | `sensor.solar_manager_power_grid` | Netzleistung (W) |
| `sensor_soc` | `sensor.solar_manager_soc` | Batterieladezustand (%) |
| `sensor_battery` | `sensor.solar_manager_power_battery` | Batterieleistung (W) |
| `sensor_production_today` | `sensor.solar_manager_production_today` | Tagesertrag (Wh) |

## Installation

1. Gehe zu **Einstellungen → Add-ons → Add-on Store**
2. Klicke auf das Menü (⋮) oben rechts → **Repositories**
3. Füge folgende URL hinzu:
   ```
   https://github.com/matze308/ha-solar-api-emulator
   ```
4. Suche nach **Fronius Solar API Emulator**, installieren und starten

## Konfiguration

```yaml
port: 8088
log_level: info
sensor_pv: sensor.solar_manager_power_pv
sensor_power: sensor.solar_manager_power
sensor_grid: sensor.solar_manager_power_grid
sensor_soc: sensor.solar_manager_soc
sensor_battery: sensor.solar_manager_power_battery
sensor_production_today: sensor.solar_manager_production_today
```

## API-Endpunkte

Nach dem Start erreichbar unter `http://<HA-IP>:8088`:

| Endpunkt |
|---|
| `GET /solar_api/GetAPIVersion.cgi` |
| `GET /solar_api/v1/GetInverterRealtimeData.cgi` |
| `GET /solar_api/v1/GetMeterRealtimeData.cgi` |
| `GET /solar_api/v1/GetStorageRealtimeData.cgi` |
| `GET /solar_api/v1/GetPowerFlowRealtimeData.cgi` |
| `GET /solar_api/v1/GetLoggerInfo.cgi` |
| `GET /solar_api/v1/GetActiveDeviceInfo.cgi` |

Jeder Endpunkt funktioniert auch mit `.fcgi` statt `.cgi`.

## Changelog

Siehe [CHANGELOG.md](CHANGELOG.md)

## Lizenz

MIT License
