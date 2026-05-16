# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

## [1.2.0] - 2026-05-16

### Hinzugefügt
- **Automatische Einheiten-Konvertierung**: Die `unit_of_measurement` jedes HA-Sensors wird
  direkt ausgelesen und automatisch konvertiert:
  - `kW` → `W` (Faktor ×1000) – behebt falsche Werte (z.B. `1.206` statt `1206`)
  - `kWh` → `Wh` (Faktor ×1000)
  - `kVA`, `kvar` → `VA`, `var` (Faktor ×1000)
  - `W`, `Wh`, `%` bleiben unveraendert
- Alle Leistungs- und Energiewerte (PV, Grid, Load, Battery, Production Today)
  werden jetzt einheitenunabhaengig korrekt in Watt / Wh geliefert
- Debug-Log zeigt jetzt Rohwert+Einheit und konvertierten Wert

### Behoben
- Solar Manager zeigte 1 Watt PV-Leistung obwohl z.B. 1206 W erzeugt wurden,
  weil der HA-Sensor `sensor.solar_manager_power_pv` in kW liefert

## [1.1.0] - 2026-05-16

### Behoben – Kritische Feldnamen-Korrekturen laut Fronius Solar API V1 Doku (42,0410,2012,EN)

**`GetMeterRealtimeData`** (Listing 43, 45):
- Alle Feldnamen jetzt EXAKT mit Unterstrichen wie in der offiziellen Doku:
  - `Current_AC_Phase_1/2/3`, `Current_AC_Sum`
  - `PowerReal_P_Sum`, `PowerReal_P_Phase_1/2/3`
  - `EnergyReal_WAC_Minus_Absolute`, `EnergyReal_WAC_Plus_Absolute`
  - `EnergyReal_WAC_Sum_Consumed`, `EnergyReal_WAC_Sum_Produced`
  - `EnergyReactive_VArAC_Sum_Consumed`, `EnergyReactive_VArAC_Sum_Produced`
  - `Frequency_Phase_Average`, `Meter_Location_Current`
  - `PowerApparent_S_Phase_1/2/3`, `PowerApparent_S_Sum`
  - `PowerFactor_Phase_1/2/3`, `PowerFactor_Sum`
  - `PowerReactive_Q_Phase_1/2/3`, `PowerReactive_Q_Sum`
  - `Voltage_AC_Phase_1/2/3`, `Voltage_AC_PhaseToPhase_12/23/31`

**`GetPowerFlowRealtimeData`** (Listing 56-60):
- `P_PV`, `P_Grid`, `P_Load`, `P_Akku`, `E_Day`, `Meter_Location`, `rel_Autonomy` etc.
- `BackupMode`, `BatteryStandby`, `Battery_Mode`, `CID` ergänzt

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
