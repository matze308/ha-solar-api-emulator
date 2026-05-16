# Fronius Solar API Emulator - Home Assistant Addon

[![Version](https://img.shields.io/badge/version-1.0.1-blue.svg)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Ein Home Assistant Addon, das die Fronius Solar API V1 simuliert. Es emuliert einen Wechselrichter (Inverter), Batteriespeicher (Storage) und Smart Meter basierend auf echten Sensordaten aus Home Assistant.

## Features

- **Wechselrichter (Inverter):** `GetInverterRealtimeData` – CommonInverterData, CumulationInverterData, 3PInverterData
- **Smart Meter:** `GetMeterRealtimeData` – System & Device Scope
- **Batteriespeicher:** `GetStorageRealtimeData` – System & Device Scope
- **PowerFlow:** `GetPowerFlowRealtimeData` – Echtzeit-Energiefluss
- **Logger Info:** `GetLoggerInfo`, `GetAPIVersion`
- **Aktive Geräte:** `GetActiveDeviceInfo`
- **Lokaler Build:** Kein externes Container-Image nötig – baut direkt aus dem Dockerfile

## Verwendete Home Assistant Entitäten

| Entität | Beschreibung |
|---|---|
| `sensor.solar_manager_power_pv` | PV-Leistung (W) |
| `sensor.solar_manager_power` | Hausverbrauch (W) |
| `sensor.solar_manager_power_grid` | Netzleistung (W, negativ = Einspeisung) |
| `sensor.solar_manager_soc` | Batterieladezustand (%) |
| `sensor.solar_manager_power_battery` | Batterieleistung (W, positiv = Laden) |
| `sensor.solar_manager_production_today` | Tagesertrag (Wh) |

## Installation

### Methode 1: Über Home Assistant Add-on Store (empfohlen)

1. Gehe zu **Einstellungen → Add-ons → Add-on Store**
2. Klicke auf das Menü (⋮) oben rechts → **Repositories**
3. Füge folgende URL hinzu:
   ```
   https://github.com/matze308/ha-solar-api-emulator
   ```
4. Suche nach **Fronius Solar API Emulator** und installiere es
5. Add-on starten – kein GHCR-Image nötig, wird lokal gebaut

## Konfiguration

```yaml
port: 8088
log_level: info
```

| Option | Beschreibung | Standard |
|---|---|---|
| `port` | HTTP-Port des API-Servers | `8088` |
| `log_level` | Log-Level (debug, info, warning, error) | `info` |

## API-Endpunkte

Nach dem Start ist die API erreichbar unter: `http://<HA-IP>:8088`

| Endpunkt | Beschreibung |
|---|---|
| `GET /solar_api/GetAPIVersion.cgi` | API Version |
| `GET /solar_api/v1/GetInverterRealtimeData.cgi` | Wechselrichter Daten |
| `GET /solar_api/v1/GetMeterRealtimeData.cgi` | Smart Meter Daten |
| `GET /solar_api/v1/GetStorageRealtimeData.cgi` | Batteriespeicher Daten |
| `GET /solar_api/v1/GetPowerFlowRealtimeData.cgi` | Energiefluss Daten |
| `GET /solar_api/v1/GetLoggerInfo.cgi` | Logger Informationen |
| `GET /solar_api/v1/GetActiveDeviceInfo.cgi` | Aktive Geräte |

## Changelog

Siehe [CHANGELOG.md](CHANGELOG.md)

## Lizenz

MIT License – siehe [LICENSE](LICENSE)
