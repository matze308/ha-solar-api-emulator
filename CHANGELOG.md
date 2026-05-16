# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/lang/de/).

## [1.0.1] - 2026-05-16

### Geändert
- `image`-Feld aus `config.yaml` entfernt – Home Assistant baut das Add-on nun lokal aus dem Dockerfile
- `homeassistant_api: true` in `config.yaml` ergänzt für korrekten Zugriff auf `http://supervisor/core/api`
- Add-on-Dokumentation als `DOCS.md` im Add-on-Ordner ergänzt

### Behoben
- Installationsfehler durch GHCR `403/401 denied` beim Pull von `ghcr.io/matze308/ha-solar-api-emulator/amd64:1.0.0`

## [1.0.0] - 2026-05-16

### Hinzugefügt
- Initiale Version des Fronius Solar API Emulators
- HTTP-Server basierend auf Python (aiohttp) für die Fronius Solar API V1
- `GetAPIVersion` Endpunkt
- `GetInverterRealtimeData` mit Scope Device und System (CommonInverterData, CumulationInverterData, 3PInverterData)
- `GetMeterRealtimeData` für Smart Meter (System & Device Scope)
- `GetStorageRealtimeData` für Batteriespeicher (System & Device Scope)
- `GetPowerFlowRealtimeData` für Echtzeit-Energiefluss
- `GetLoggerInfo` Endpunkt
- `GetActiveDeviceInfo` Endpunkt
- Integration mit Home Assistant Supervisor API (Long-Lived Access Token)
- Liest Echtzeit-Sensordaten aus Home Assistant:
  - `sensor.solar_manager_power_pv` (PV-Leistung)
  - `sensor.solar_manager_power` (Hausverbrauch)
  - `sensor.solar_manager_power_grid` (Netzleistung)
  - `sensor.solar_manager_soc` (Batterieladezustand)
  - `sensor.solar_manager_power_battery` (Batterieleistung)
  - `sensor.solar_manager_production_today` (Tagesertrag)
- Konfigurierbare Port-Einstellung
- Konfigurierbares Log-Level
- Home Assistant Addon Struktur (config.yaml, Dockerfile, run.sh)
- Repository-Konfiguration für HA Add-on Store (repository.yaml)
