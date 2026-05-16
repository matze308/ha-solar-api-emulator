# Fronius Solar API Emulator – Home Assistant Add-on

[![Version](https://img.shields.io/badge/version-1.2.2-blue)](fronius-solar-api-emulator/CHANGELOG.md)
[![HA Add-on](https://img.shields.io/badge/Home%20Assistant-Add--on-41bdf5)](https://www.home-assistant.io/addons)

Dieses Home Assistant Add-on emuliert eine **Fronius Solar API V1**-Schnittstelle vollständig.

Externe Energiemanagement-Systeme wie **Solar Manager**, **evcc** oder andere,
die eine Fronius-Schnittstelle erwarten, können so die Echtzeitdaten deiner
Home Assistant Sensoren abfragen – ohne echten Fronius-Wechselrichter.

## Emulierte Geräte

- **Wechselrichter** (Fronius GEN24-kompatibel, DT=1)
- **Batteriespeicher** (Fronius Solar Battery / LG-Chem kompatibel)
- **Smart Meter** (Fronius Smart Meter 63A-3 kompatibel)

## Emulierte API-Endpunkte

| Endpunkt | Listing (Doku) |
|---|---|
| `GET /solar_api/GetAPIVersion.cgi` | – |
| `GET /solar_api/v1/GetLoggerInfo.cgi` | Listing 27-28 |
| `GET /solar_api/v1/GetInverterInfo.cgi` | Listing 31-33 |
| `GET /solar_api/v1/GetActiveDeviceInfo.cgi` | Listing 34-41 |
| `GET /solar_api/v1/GetInverterRealtimeData.cgi` | Listing 7, 8, 11, 14 |
| `GET /solar_api/v1/GetMeterRealtimeData.cgi` | Listing 43, 45 |
| `GET /solar_api/v1/GetStorageRealtimeData.cgi` | Listing 47-51 |
| `GET /solar_api/v1/GetPowerFlowRealtimeData.fcgi` | Listing 56-60 |

Alle Endpunkte sind sowohl als `.cgi` als auch als `.fcgi` erreichbar.

## Installation

1. **Repository hinzufügen** in Home Assistant:
   - *Einstellungen → Add-ons → Add-on Store → ⋮ → Repositories*
   - URL: `https://github.com/matze308/ha-solar-api-emulator`

2. **Add-on installieren**: „Fronius Solar API Emulator“ suchen und installieren.

3. **Konfigurieren** – Sensornamen anpassen:

```yaml
log_level: info
sensor_pv: sensor.solar_manager_power_pv
sensor_power: sensor.solar_manager_power
sensor_grid: sensor.solar_manager_power_grid
sensor_soc: sensor.solar_manager_soc
sensor_battery: sensor.solar_manager_power_battery
sensor_production_today: sensor.solar_manager_production_today
```

4. **Host-Port anpassen** (optional): Im *Netzwerk*-Tab des Add-ons kann der
   nach außen exponierte Port geändert werden (Standard: `8088`).

5. **Add-on starten** – Die API ist dann erreichbar unter:
   ```
   http://<HA-IP>:8088/solar_api/v1/GetPowerFlowRealtimeData.fcgi
   ```

## Automatische Einheiten-Konvertierung

Das Add-on liest die `unit_of_measurement` jedes Sensors aus den HA-Attributen
und konvertiert automatisch:

| Sensor-Einheit | Wird zu | Faktor |
|---|---|---|
| `kW` | `W` | ×1000 |
| `kWh` | `Wh` | ×1000 |
| `W`, `Wh`, `%` | unveraendert | ×1 |

## Sensor-Bedeutung

| Konfiguration | Bedeutung | Einheit |
|---|---|---|
| `sensor_pv` | PV-Erzeugungsleistung | W oder kW |
| `sensor_power` | Hausverbrauch (Load) | W oder kW |
| `sensor_grid` | Netzleistung (+ Bezug, − Einspeisung) | W oder kW |
| `sensor_soc` | Batterieladezustand | % |
| `sensor_battery` | Batterieleistung (+ Laden, − Entladen) | W oder kW |
| `sensor_production_today` | PV-Erzeugung heute | Wh oder kWh |

## Changelog

Siehe [CHANGELOG.md](fronius-solar-api-emulator/CHANGELOG.md).
