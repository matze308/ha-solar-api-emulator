# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

## [1.0.7] - 2026-05-16

### Behoben
- Vollständiger Abgleich aller Feldnamen mit der offiziellen Fronius Solar API V1 Dokumentation (42,0410,2012,EN)

**`GetInverterRealtimeData`** (Listing 4, 7, 14):
- `DAY_ENERGY`, `YEAR_ENERGY`, `TOTAL_ENERGY` (MIT Unterstrich) – korrekter Feldname laut Doku
- Scope=System: `Values`-Objekt statt `Value` (Listing 14)
- `3PInverterData`: `IAC_L1`, `IAC_L2`, `IAC_L3`, `UAC_L1`, `UAC_L2`, `UAC_L3` (Listing 8)

**`GetMeterRealtimeData`** (Listing 43, 45):
- Alle Feldnamen als CamelCase ohne Unterstriche: `CurrentACPhase1`, `PowerRealPSum`, `EnergyRealWACMinusAbsolute` etc.
- `VoltageACPhaseAverage` ergänzt

**`GetStorageRealtimeData`** (Listing 48):
- Feldnamen korrigiert: `StateOfCharge_Relative`, `Capacity_Maximum`, `DesignedCapacity`, `Current_DC`, `Voltage_DC`, `Temperature_Cell`, `Status_BatteryCell`, `Voltage_DC_Maximum_Cell`, `Voltage_DC_Minimum_Cell`

**`GetPowerFlowRealtimeData`** (Listing 57-60):
- Site: `PPV`, `PGrid`, `PLoad`, `PAkku`, `EDay`, `ETotal`, `EYear`, `MeterLocation`, `relAutonomy`, `relSelfConsumption`
- Inverter: `BatteryMode`, `EDay`, `ETotal`, `EYear`, `P`, `SOC`
- (keine Unterstriche: nicht `P_PV`, nicht `E_Day`, nicht `rel_Autonomy`)

**`GetActiveDeviceInfo`**:
- Meter und Storage: `DT: -1` (korrekt laut Doku, Inverter haben DT-Nummern)

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
