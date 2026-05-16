# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/lang/de/).

## [1.0.5] - 2026-05-16

### Behoben
- `GetMeterRealtimeData`: `PowerRealPSum` / `PowerRealPPhase1-3` liefern jetzt den korrekten Wert direkt aus dem Grid-Sensor
- Falscher Skalierungsfaktor (`* 0.01`) bei den Energiezählern entfernt
- Strom (CurrentAC) wird nun korrekt aus der absoluten Netzleistung berechnet
- Debug-Logging für Meter-Werte hinzugefügt

## [1.0.4] - 2026-05-16

### Hinzugefügt
- Alle 6 Sensor-Entitäten über Add-on-Konfiguration einstellbar
- `run.sh` leitet Entitätsnamen als Umgebungsvariablen weiter
- Deutsche Übersetzungen für alle Konfigurationsoptionen

## [1.0.3] - 2026-05-16

### Behoben
- Alle API-Endpunkte antworten jetzt sowohl auf `.cgi` als auch auf `.fcgi` URLs

## [1.0.2] - 2026-05-16

### Behoben
- `build.yaml` mit korrekten Base-Images pro Architektur ergänzt
- `Dockerfile`: `ARG BUILD_FROM` erhält nun einen Standardwert
- `aiohttp` wird jetzt per `pip3` installiert

## [1.0.1] - 2026-05-16

### Geändert
- `image`-Feld aus `config.yaml` entfernt
- `homeassistant_api: true` ergänzt
- `DOCS.md` ergänzt

### Behoben
- Installationsfehler durch GHCR `403/401 denied`

## [1.0.0] - 2026-05-16

### Hinzugefügt
- Initiale Version des Fronius Solar API Emulators
- HTTP-Server basierend auf Python (aiohttp) für die Fronius Solar API V1
- `GetAPIVersion`, `GetInverterRealtimeData`, `GetMeterRealtimeData`, `GetStorageRealtimeData`, `GetPowerFlowRealtimeData`, `GetLoggerInfo`, `GetActiveDeviceInfo`
- Integration mit Home Assistant Supervisor API
- Konfigurierbare Port-Einstellung und Log-Level
