# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/lang/de/).

## [1.0.6] - 2026-05-16

### Behoben
- `GetInverterRealtimeData`: Feldnamen korrigiert gemäß Fronius API Doku Listing 7/11/14:
  - `DAY_ENERGY` → `DAYENERGY`
  - `TOTAL_ENERGY` → `TOTALENERGY`
  - `YEAR_ENERGY` → `YEARENERGY`
  - Scope=System gibt jetzt `Values`-Objekt statt `Value` zurück (Listing 14)
- `GetPowerFlowRealtimeData`: Site-Feldnamen korrigiert gemäß Doku Listing 59/60:
  - `P_PV` → `PPV`
  - `P_Grid` → `PGrid`
  - `P_Load` → `PLoad`
  - `P_Akku` → `PAkku`
  - Inverter-Felder: `E_Day` → `EDay`, `E_Total` → `ETotal`, `E_Year` → `EYear`
- Sensor-Rohdaten werden jetzt im Debug-Log ausgegeben (alle Endpunkte)

## [1.0.5] - 2026-05-16

### Behoben
- `GetMeterRealtimeData`: `PowerRealPSum` liefert jetzt korrekten Grid-Sensor-Wert
- Falscher Skalierungsfaktor entfernt

## [1.0.4] - 2026-05-16

### Hinzugefügt
- Alle 6 Sensor-Entitäten über Add-on-Konfiguration einstellbar

## [1.0.3] - 2026-05-16

### Behoben
- Alle API-Endpunkte antworten auf `.cgi` und `.fcgi`

## [1.0.2] - 2026-05-16

### Behoben
- `build.yaml` ergänzt, `Dockerfile` ARG-Standardwert gesetzt

## [1.0.1] - 2026-05-16

### Behoben
- GHCR 403/401 Installationsfehler

## [1.0.0] - 2026-05-16

### Hinzugefügt
- Initiale Version
