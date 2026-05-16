# Fronius Solar API Emulator

Dieses Add-on simuliert die Fronius Solar API V1 auf Basis vorhandener Home-Assistant-Sensoren.
Es emuliert einen Wechselrichter (Inverter), Batteriespeicher (Storage) und Smart Meter.

## Installation

1. Add-on installieren
2. Optional den Port anpassen (Standard: `8088`)
3. Add-on starten

> **Hinweis:** Dieses Add-on baut lokal aus dem Dockerfile und benötigt kein externes Container-Registry-Image.

## Konfiguration

```yaml
port: 8088
log_level: info
```

| Option | Beschreibung | Standard |
|---|---|---|
| `port` | HTTP-Port der Fronius API | `8088` |
| `log_level` | Log-Level (debug, info, warning, error) | `info` |

## Verwendete Entitäten

Folgende Home Assistant Sensoren werden für die API-Simulation benötigt:

| Entität | Beschreibung |
|---|---|
| `sensor.solar_manager_power_pv` | PV-Leistung in Watt |
| `sensor.solar_manager_power` | Hausverbrauch in Watt |
| `sensor.solar_manager_power_grid` | Netzleistung (pos. = Bezug, neg. = Einspeisung) |
| `sensor.solar_manager_soc` | Batterieladezustand in % |
| `sensor.solar_manager_power_battery` | Batterieleistung (pos. = Laden, neg. = Entladen) |
| `sensor.solar_manager_production_today` | Tagesertrag in Wh |

## API-Endpunkte

Nach dem Start ist die API erreichbar unter `http://<HA-IP>:8088`:

| Endpunkt | Beschreibung |
|---|---|
| `/solar_api/GetAPIVersion.cgi` | API-Version |
| `/solar_api/v1/GetInverterRealtimeData.cgi` | Wechselrichter-Daten |
| `/solar_api/v1/GetMeterRealtimeData.cgi` | Smart Meter-Daten |
| `/solar_api/v1/GetStorageRealtimeData.cgi` | Batteriespeicher-Daten |
| `/solar_api/v1/GetPowerFlowRealtimeData.cgi` | Echtzeit-Energiefluss |
| `/solar_api/v1/GetLoggerInfo.cgi` | Logger-Informationen |
| `/solar_api/v1/GetActiveDeviceInfo.cgi` | Aktive Geräte |

## Beispielaufruf

```bash
curl http://<HA-IP>:8088/solar_api/v1/GetPowerFlowRealtimeData.cgi
```
