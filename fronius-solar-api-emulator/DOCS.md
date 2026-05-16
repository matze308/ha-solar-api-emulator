# Fronius Solar API Emulator – Dokumentation

Dieses Add-on emuliert die **Fronius Solar API V1** (Dokumentation: 42,0410,2012,EN) vollständig.

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

## Port

Der **interne Port ist fest auf `8088`** gesetzt. Der nach außen exponierte Host-Port
kann in der Add-on-Konfiguration unter *Netzwerk* geändert werden.

Standard-Zugriff:
```
http://<HA-IP>:8088/solar_api/v1/GetPowerFlowRealtimeData.fcgi
```

## Konfiguration

```yaml
log_level: info
sensor_pv: sensor.solar_manager_power_pv
sensor_power: sensor.solar_manager_power
sensor_grid: sensor.solar_manager_power_grid
sensor_soc: sensor.solar_manager_soc
sensor_battery: sensor.solar_manager_power_battery
sensor_production_today: sensor.solar_manager_production_today
```

### Sensor-Bedeutung

| Option | Bedeutung | Unterstützte Einheiten |
|---|---|---|
| `sensor_pv` | PV-Erzeugungsleistung | W, kW |
| `sensor_power` | Hausverbrauch (Load) | W, kW |
| `sensor_grid` | Netzleistung (+ Bezug, − Einspeisung) | W, kW |
| `sensor_soc` | Batterieladezustand | % |
| `sensor_battery` | Batterieleistung (+ Laden, − Entladen) | W, kW |
| `sensor_production_today` | PV-Erzeugung heute | Wh, kWh |

kW und kWh werden automatisch in W bzw. Wh konvertiert.
