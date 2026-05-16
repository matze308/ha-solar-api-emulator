# Fronius Solar API Emulator – Dokumentation

Dieses Add-on emuliert die **Fronius Solar API V1** (Dokumentation: 42,0410,2012,EN) vollständig, sodass externe Systeme wie **Solar Manager**, **evcc** oder andere Energiemanager den Fronius-Wechselrichter inkl. Batterie und Smart Meter abfragen können.

## Emulierte API-Endpunkte

| Endpunkt | Beschreibung |
|---|---|
| `GET /solar_api/GetAPIVersion.cgi` | API-Version |
| `GET /solar_api/v1/GetLoggerInfo.cgi` | Logger-Informationen |
| `GET /solar_api/v1/GetInverterInfo.cgi` | Wechselrichter-Informationen |
| `GET /solar_api/v1/GetActiveDeviceInfo.cgi` | Aktive Geräte |
| `GET /solar_api/v1/GetInverterRealtimeData.cgi` | Wechselrichter Echtzeitdaten |
| `GET /solar_api/v1/GetMeterRealtimeData.cgi` | Smart Meter Echtzeitdaten |
| `GET /solar_api/v1/GetStorageRealtimeData.cgi` | Batteriespeicher Echtzeitdaten |
| `GET /solar_api/v1/GetPowerFlowRealtimeData.fcgi` | Leistungsfluss Echtzeitdaten |

Alle Endpunkte sind sowohl als `.cgi` als auch als `.fcgi` erreichbar.

## Konfiguration

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

### Sensor-Bedeutung

| Option | Bedeutung | Einheit |
|---|---|---|
| `sensor_pv` | PV-Erzeugungsleistung | W |
| `sensor_power` | Hausverbrauch (Load) | W |
| `sensor_grid` | Netzleistung (+ Bezug, − Einspeisung) | W |
| `sensor_soc` | Batterieladezustand | % |
| `sensor_battery` | Batterieleistung (+ Laden, − Entladen) | W |
| `sensor_production_today` | PV-Erzeugung heute | Wh |

## Feldname-Konformität

Die Feldnamen entsprechen exakt der offiziellen Fronius Solar API V1 Dokumentation:

- **GetMeterRealtimeData**: `Current_AC_Phase_1`, `PowerReal_P_Sum`, `EnergyReal_WAC_Minus_Absolute` etc.
- **GetStorageRealtimeData**: `StateOfCharge_Relative`, `Capacity_Maximum`, `Current_DC` etc.
- **GetPowerFlowRealtimeData**: `P_PV`, `P_Grid`, `P_Load`, `P_Akku`, `E_Day`, `rel_Autonomy` etc.
- **GetInverterRealtimeData**: `DAY_ENERGY`, `YEAR_ENERGY`, `TOTAL_ENERGY`, `PAC`, `IAC`, `IDC` etc.

## Zugriff

Nach dem Start ist die API unter `http://<HA-IP>:8088` erreichbar.

Beispiel:
```
http://192.168.1.100:8088/solar_api/v1/GetPowerFlowRealtimeData.fcgi
```
