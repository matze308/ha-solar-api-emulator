# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

## [1.2.2] - 2026-05-16

### Geändert
- `CHANGELOG.md` ins Add-on-Verzeichnis verschoben, damit Home Assistant
  den Changelog beim Update im Add-on Store anzeigt

## [1.2.1] - 2026-05-16

### Geändert
- Interner Container-Port ist jetzt **fest auf `8088`** gesetzt und nicht mehr
  über die Add-on-Konfiguration änderbar
- Der nach außen exponierte Host-Port bleibt über den *Netzwerk*-Tab änderbar
- Option `port` aus dem Konfigurationsschema entfernt (war redundant)

## [1.2.0] - 2026-05-16

### Hinzugefügt
- **Automatische Einheiten-Konvertierung**: `unit_of_measurement` wird aus den
  HA-Sensor-Attributen gelesen und automatisch konvertiert
  - `kW` → `W` (×1000), `kWh` → `Wh` (×1000)
  - `W`, `Wh`, `%` bleiben unveraendert

### Behoben
- Solar Manager zeigte 1 Watt PV-Leistung, weil Sensor in kW lieferte

## [1.1.0] - 2026-05-16

### Behoben
- Alle Feldnamen exakt laut Fronius Solar API V1 Dokumentation korrigiert
- `GetMeterRealtimeData`: `Current_AC_Phase_1`, `PowerReal_P_Sum` etc.
- `GetPowerFlowRealtimeData`: `P_PV`, `P_Grid`, `P_Load`, `P_Akku`,
  `E_Day`, `rel_Autonomy` etc.

### Hinzugefügt
- Neuer Endpunkt `GetInverterInfo.cgi`
- Deutsche und englische UI-Übersetzungen

## [1.0.7] - 2026-05-16

### Behoben
- Vollständiger Abgleich aller Feldnamen mit der offiziellen Doku

## [1.0.0] - 2026-05-16

### Hinzugefügt
- Initiale Version des Fronius Solar API Emulators
