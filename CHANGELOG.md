# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

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
- `Current_AC_Phase_*` ist jetzt vorzeichenbehaftet (wie UL/TS-Meter laut Doku)
- Frühere CamelCase-Feldnamen (z.B. `CurrentACPhase1`, `PowerRealPSum`) sind behoben

**`GetPowerFlowRealtimeData`** (Listing 56-60):
- Alle Site-Felder jetzt EXAKT mit Unterstrichen:
  - `P_PV`, `P_Grid`, `P_Load`, `P_Akku` (nicht `PPV`, `PGrid`, `PLoad`, `PAkku`)
  - `E_Day`, `E_Total`, `E_Year` (nicht `EDay`, `ETotal`, `EYear`)
  - `Meter_Location` (nicht `MeterLocation`)
  - `rel_Autonomy`, `rel_SelfConsumption` (nicht `relAutonomy`, `relSelfConsumption`)
- `BackupMode`, `BatteryStandby` ergänzt
- Inverter: `Battery_Mode` (nicht `BatteryMode`), `CID` ergänzt

**`GetStorageRealtimeData`** (Listing 47-51):
- `Status_BatteryCell`-Logik: jetzt ENABLED (3) für Laden UND Entladen

**`GetInverterRealtimeData`** (Listing 7, 14):
- `InverterState: "Running"` zu `DeviceStatus` ergänzt (GEN24-Kompatibilität, Listing 10)
- Timestamp-Format auf RFC3339 mit korrekter Zeitzone korrigiert
- `unavailable`/`unknown`-Sensorstatus wird als `0.0` behandelt

### Hinzugefügt
- Neuer Endpunkt `GetInverterInfo.cgi` (Listing 31-33)
- Deutsche und englische UI-Übersetzungen (`translations/de.yaml`, `translations/en.yaml`)

## [1.0.7] - 2026-05-16

### Behoben
- Vollständiger Abgleich aller Feldnamen mit der offiziellen Fronius Solar API V1 Dokumentation (42,0410,2012,EN)

**`GetInverterRealtimeData`** (Listing 4, 7, 14):
- `DAY_ENERGY`, `YEAR_ENERGY`, `TOTAL_ENERGY` (MIT Unterstrich) – korrekter Feldname laut Doku
- Scope=System: `Values`-Objekt statt `Value` (Listing 14)
- `3PInverterData`: `IAC_L1`, `IAC_L2`, `IAC_L3`, `UAC_L1`, `UAC_L2`, `UAC_L3` (Listing 8)

**`GetMeterRealtimeData`** (Listing 43, 45):
- Erste Implementierung CamelCase (noch nicht korrekt)

**`GetStorageRealtimeData`** (Listing 48):
- Feldnamen: `StateOfCharge_Relative`, `Capacity_Maximum`, `DesignedCapacity`, `Current_DC`, `Voltage_DC`, `Temperature_Cell`, `Status_BatteryCell`

**`GetPowerFlowRealtimeData`** (Listing 57-60):
- Erste Implementierung (Feldnamen noch ohne Unterstriche)

**`GetActiveDeviceInfo`**:
- Meter und Storage: `DT: -1`

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
