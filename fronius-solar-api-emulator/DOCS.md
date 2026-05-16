# Fronius Solar API Emulator

Dieses Add-on simuliert die Fronius Solar API V1 auf Basis vorhandener Home-Assistant-Sensoren.
Es emuliert einen Wechselrichter (Inverter), Batteriespeicher (Storage) und Smart Meter.

## Installation

1. Add-on installieren
2. Sensor-Entitäten und Port konfigurieren
3. Add-on starten

> **Hinweis:** Dieses Add-on baut lokal aus dem Dockerfile und benötigt kein externes Container-Registry-Image.

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

| Option | Beschreibung | Standard |
|---|---|---|
| `port` | HTTP-Port der Fronius API | `8088` |
| `log_level` | Log-Level (debug, info, warning, error) | `info` |
| `sensor_pv` | Entität für PV-Leistung (W) | `sensor.solar_manager_power_pv` |
| `sensor_power` | Entität für Hausverbrauch (W) | `sensor.solar_manager_power` |
| `sensor_grid` | Entität für Netzleistung (W, pos.=Bezug, neg.=Einspeisung) | `sensor.solar_manager_power_grid` |
| `sensor_soc` | Entität für Batterieladezustand (%) | `sensor.solar_manager_soc` |
| `sensor_battery` | Entität für Batterieleistung (W, pos.=Laden, neg.=Entladen) | `sensor.solar_manager_power_battery` |
| `sensor_production_today` | Entität für Tagesertrag (Wh) | `sensor.solar_manager_production_today` |

## API-Endpunkte

Nach dem Start erreichbar unter `http://<HA-IP>:8088` – jeweils als `.cgi` und `.fcgi`:

| Endpunkt | Beschreibung |
|---|---|
| `/solar_api/GetAPIVersion.cgi` | API-Version |
| `/solar_api/v1/GetInverterRealtimeData.cgi` | Wechselrichter-Daten |
| `/solar_api/v1/GetMeterRealtimeData.cgi` | Smart Meter-Daten |
| `/solar_api/v1/GetStorageRealtimeData.cgi` | Batteriespeicher-Daten |
| `/solar_api/v1/GetPowerFlowRealtimeData.cgi` | Echtzeit-Energiefluss |
| `/solar_api/v1/GetLoggerInfo.cgi` | Logger-Informationen |
| `/solar_api/v1/GetActiveDeviceInfo.cgi` | Aktive Geräte |

## Beispielaufruf

```bash
curl http://<HA-IP>:8088/solar_api/v1/GetPowerFlowRealtimeData.fcgi
```
