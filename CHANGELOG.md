# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

## [1.2.1] - 2026-05-16

### Geändert
- Interner Container-Port ist jetzt **fest auf `8088`** gesetzt und nicht mehr
  über die Add-on-Konfiguration änderbar
- Der nach außen exponierte Host-Port bleibt wie gehabt über den
  *Netzwerk*-Tab der Add-on-Konfiguration änderbar (Standard: `8088`)
- Option `port` aus dem Konfigurationsschema entfernt (war redundant)
- `run.sh` setzt `PORT=8088` jetzt direkt als Konstante

## [1.2.0] - 2026-05-16

### Hinzugefügt
- **Automatische Einheiten-Konvertierung**: `unit_of_measurement` wird aus den
  HA-Sensor-Attributen gelesen und automatisch konvertiert:
  - `kW` → `W` (Faktor ×1000)
  - `kWh` → `Wh` (Faktor ×1000)
  - `kVA`, `kvar` entsprechend
  - `W`, `Wh`, `%` bleiben unveraendert

### Behoben
- Solar Manager zeigte 1 Watt PV-Leistung, weil Sensor in kW lieferte

## [1.1.0] - 2026-05-16

### Behoben – Kritische Feldnamen-Korrekturen laut Fronius Solar API V1 Doku

**`GetMeterRealtimeData`**: `Current_AC_Phase_1`, `PowerReal_P_Sum`, `EnergyReal_WAC_Minus_Absolute` etc.

**`GetPowerFlowRealtimeData`**: `P_PV`, `P_Grid`, `P_Load`, `P_Akku`, `E_Day`, `rel_Autonomy` etc.

### Hinzugefügt
- Neuer Endpunkt `GetInverterInfo.cgi`
- Deutsche und englische UI-Übersetzungen

## [1.0.7] - 2026-05-16

### Behoben
- Vollständiger Abgleich aller Feldnamen mit der offiziellen Fronius Solar API V1 Dokumentation

## [1.0.6] - 2026-05-16

### Behoben
- Erster Versuch Feldnamen-Korrektur (teilweise falsch)

## [1.0.5] - 2026-05-16

### Behoben
- `GetMeterRealtimeData`: `PowerRealPSum` liefert korrekten Grid-Sensor-Wert

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
