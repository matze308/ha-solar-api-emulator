# Fronius Solar API Emulator – Home Assistant Add-on

[![Version](https://img.shields.io/badge/version-1.1.0-blue)](CHANGELOG.md)
[![HA Add-on](https://img.shields.io/badge/Home%20Assistant-Add--on-41bdf5)](https://www.home-assistant.io/addons)

Dieses Home Assistant Add-on emuliert eine **Fronius Solar API V1**-Schnittstelle (Dokumentation: [42,0410,2012,EN](https://www.fronius.com/~/downloads/Solar%20Energy/Operating%20Instructions/42,0410,2012.pdf)) vollständig.

Externe Energiemanagement-Systeme wie **Solar Manager**, **evcc**, **SolarEdge** oder andere, die eine Fronius-Schnittstelle erwarten, können so die Echtzeitdaten deiner Home Assistant Sensoren abfragen – ohne echten Fronius-Wechselrichter.

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
port: 8088
log_level: info
sensor_pv: sensor.solar_manager_power_pv
sensor_power: sensor.solar_manager_power
sensor_grid: sensor.solar_manager_power_grid
sensor_soc: sensor.solar_manager_soc
sensor_battery: sensor.solar_manager_power_battery
sensor_production_today: sensor.solar_manager_production_today
```

4. **Add-on starten** – Die API ist dann erreichbar unter:
   ```
   http://<HA-IP>:8088/solar_api/v1/GetPowerFlowRealtimeData.fcgi
   ```

## Sensor-Bedeutung

| Konfiguration | Bedeutung | Einheit |
|---|---|---|
| `sensor_pv` | PV-Erzeugungsleistung | W |
| `sensor_power` | Hausverbrauch (Load) | W |
| `sensor_grid` | Netzleistung (+ Bezug, − Einspeisung) | W |
| `sensor_soc` | Batterieladezustand | % |
| `sensor_battery` | Batterieleistung (+ Laden, − Entladen) | W |
| `sensor_production_today` | PV-Erzeugung heute | Wh |

## Feldname-Konformität

Alle zurückgegebenen Feldnamen entsprechen **exakt** der offiziellen Fronius Solar API V1 Dokumentation:

- **GetMeterRealtimeData**: `Current_AC_Phase_1`, `PowerReal_P_Sum`, `EnergyReal_WAC_Minus_Absolute` ...
- **GetStorageRealtimeData**: `StateOfCharge_Relative`, `Capacity_Maximum`, `Current_DC` ...
- **GetPowerFlowRealtimeData**: `P_PV`, `P_Grid`, `P_Load`, `P_Akku`, `E_Day`, `rel_Autonomy` ...
- **GetInverterRealtimeData**: `DAY_ENERGY`, `YEAR_ENERGY`, `TOTAL_ENERGY`, `PAC`, `IAC` ...

## Changelog

Siehe [CHANGELOG.md](CHANGELOG.md).
