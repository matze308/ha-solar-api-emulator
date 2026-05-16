#!/usr/bin/env python3
"""
Fronius Solar API V1 Emulator for Home Assistant.

Feldnamen gemaess offizieller Fronius Solar API V1 Dokumentation (42,0410,2012,EN).

GetInverterRealtimeData:
  Scope=Device: DAY_ENERGY, YEAR_ENERGY, TOTAL_ENERGY, PAC, FAC, IAC, IDC, UAC, UDC (Listing 7)
  Scope=System: DAY_ENERGY {Unit, Values:{"1":...}}, PAC, TOTAL_ENERGY, YEAR_ENERGY (Listing 14)

GetMeterRealtimeData:
  CurrentACPhase1/2/3, CurrentACSum, PowerRealPSum, PowerRealPPhase1/2/3
  EnergyRealWACMinusAbsolute, EnergyRealWACPlusAbsolute, etc. (Listing 43)

GetPowerFlowRealtimeData:
  Site: PPV, PGrid, PLoad, PAkku, EDay, ETotal, EYear, MeterLocation, Mode,
        relAutonomy, relSelfConsumption (Listing 57-60)
  Inverters: P, SOC, DT, EDay, ETotal, EYear, BatteryMode (Listing 57-60)
"""

import asyncio
import logging
import os
import time
from datetime import datetime

from aiohttp import web, ClientSession, ClientTimeout

LOG_LEVEL = os.environ.get("LOG_LEVEL", "info").upper()
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("fronius-emulator")

PORT = int(os.environ.get("PORT", 8088))
SUPERVISOR_TOKEN = os.environ.get("SUPERVISOR_TOKEN", "")
HA_API = "http://supervisor/core/api"

SENSOR_PV               = os.environ.get("SENSOR_PV",               "sensor.solar_manager_power_pv")
SENSOR_POWER            = os.environ.get("SENSOR_POWER",            "sensor.solar_manager_power")
SENSOR_GRID             = os.environ.get("SENSOR_GRID",             "sensor.solar_manager_power_grid")
SENSOR_SOC              = os.environ.get("SENSOR_SOC",              "sensor.solar_manager_soc")
SENSOR_BATTERY          = os.environ.get("SENSOR_BATTERY",          "sensor.solar_manager_power_battery")
SENSOR_PRODUCTION_TODAY = os.environ.get("SENSOR_PRODUCTION_TODAY", "sensor.solar_manager_production_today")


def now_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H%M%S") + "+0200"


def unix_timestamp() -> int:
    return int(time.time())


def ok_head(request_arguments: dict) -> dict:
    return {
        "RequestArguments": request_arguments,
        "Status": {"Code": 0, "Reason": "", "UserMessage": ""},
        "Timestamp": now_timestamp(),
    }


async def fetch_sensor(session: ClientSession, entity_id: str) -> float:
    headers = {"Authorization": f"Bearer {SUPERVISOR_TOKEN}"}
    url = f"{HA_API}/states/{entity_id}"
    try:
        async with session.get(url, headers=headers, timeout=ClientTimeout(total=5)) as resp:
            if resp.status == 200:
                data = await resp.json()
                return float(data.get("state", 0))
    except Exception as e:
        log.warning(f"Could not fetch {entity_id}: {e}")
    return 0.0


async def fetch_all_sensors(session: ClientSession) -> dict:
    results = await asyncio.gather(
        fetch_sensor(session, SENSOR_PV),
        fetch_sensor(session, SENSOR_POWER),
        fetch_sensor(session, SENSOR_GRID),
        fetch_sensor(session, SENSOR_SOC),
        fetch_sensor(session, SENSOR_BATTERY),
        fetch_sensor(session, SENSOR_PRODUCTION_TODAY),
    )
    s = {
        "pv":               results[0],
        "power":            results[1],
        "grid":             results[2],
        "soc":              results[3],
        "battery":          results[4],
        "production_today": results[5],
    }
    log.debug(
        f"Sensors: pv={s['pv']}W grid={s['grid']}W bat={s['battery']}W "
        f"load={s['power']}W soc={s['soc']}% today={s['production_today']}Wh"
    )
    return s


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------

async def handle_api_version(request: web.Request) -> web.Response:
    return web.json_response({
        "Head": ok_head({}),
        "Body": {
            "APIVersion": 1,
            "BaseURL": "/solar_api/v1/",
            "CompatibilityRange": "1.5-9",
        },
    })


async def handle_logger_info(request: web.Request) -> web.Response:
    return web.json_response({
        "Head": ok_head({}),
        "Body": {
            "LoggerInfo": {
                "CO2Factor": 0.53,
                "CO2Unit": "kg/kWh",
                "CashCurrency": "EUR",
                "CashFactor": 0.28,
                "DefaultLanguage": "de",
                "DeliveryFactor": 0.15,
                "HWVersion": "2.4E",
                "PlatformID": "wilma",
                "ProductID": "fronius-solar-api-emulator",
                "SWVersion": "3.9.1-1",
                "TimezoneLocation": "Europe/Berlin",
                "TimezoneName": "CEST",
                "UTCOffset": 7200,
                "UniqueID": "HA-SOLAR-EMULATOR-001",
            }
        },
    })


async def handle_active_device_info(request: web.Request) -> web.Response:
    device_class = request.rel_url.query.get("DeviceClass", "System")
    return web.json_response({
        "Head": ok_head({"DeviceClass": device_class}),
        "Body": {
            "Data": {
                "Inverter": {"1": {"DT": 123, "PVPower": 10000, "Show": 1, "UniqueID": "INV-001"}},
                "Meter":    {"0": {"DT": -1, "Serial": "METER-001"}},
                "Storage":  {"0": {"DT": -1, "Serial": "BAT-001"}},
            }
        },
    })


async def handle_inverter_realtime(request: web.Request) -> web.Response:
    """
    Gemaess Fronius Solar API Doku Listing 7 (CommonInverterData) und Listing 14 (System):
    - Scope=Device: DAY_ENERGY, YEAR_ENERGY, TOTAL_ENERGY (mit Unterstrich!), PAC, FAC, IAC, IDC, UAC, UDC
    - Scope=System: DAY_ENERGY {Unit, Values:{"1":wert}}, PAC, TOTAL_ENERGY, YEAR_ENERGY
    - 3PInverterData: IAC_L1, IAC_L2, IAC_L3, UAC_L1, UAC_L2, UAC_L3 (Listing 8)
    """
    scope      = request.rel_url.query.get("Scope", "Device")
    device_id  = request.rel_url.query.get("DeviceId", "1")
    collection = request.rel_url.query.get("DataCollection", "CommonInverterData")

    async with ClientSession() as session:
        s = await fetch_all_sensors(session)

    pac        = float(s["pv"])
    day_energy = float(s["production_today"])
    uac = 230.0
    udc = 380.0
    iac = round(pac / (uac * 3), 3) if pac > 0 else 0.0
    idc = round(pac / udc, 3)       if pac > 0 else 0.0

    # Scope=System: Values-Objekt gemaess Listing 14
    if scope == "System":
        return web.json_response({
            "Head": ok_head({"DeviceClass": "Inverter", "Scope": "System"}),
            "Body": {"Data": {
                "DAY_ENERGY":   {"Unit": "Wh", "Values": {"1": day_energy}},
                "PAC":          {"Unit": "W",  "Values": {"1": pac}},
                "TOTAL_ENERGY": {"Unit": "Wh", "Values": {"1": day_energy * 365}},
                "YEAR_ENERGY":  {"Unit": "Wh", "Values": {"1": day_energy * 250}},
            }},
        })

    req_args = {
        "DataCollection": collection,
        "DeviceClass": "Inverter",
        "DeviceId": device_id,
        "Scope": scope,
    }

    # CommonInverterData - Listing 7: DAY_ENERGY, YEAR_ENERGY, TOTAL_ENERGY (MIT Unterstrich)
    if collection == "CommonInverterData":
        data = {
            "DAY_ENERGY": {"Unit": "Wh", "Value": day_energy},
            "DeviceStatus": {
                "ErrorCode": 0,
                "LEDColor": 2,
                "LEDState": 0,
                "MgmtTimerRemainingTime": -1,
                "StateToReset": False,
                "StatusCode": 7,
            },
            "FAC":          {"Unit": "Hz", "Value": 50.0},
            "IAC":          {"Unit": "A",  "Value": iac},
            "IDC":          {"Unit": "A",  "Value": idc},
            "PAC":          {"Unit": "W",  "Value": pac},
            "TOTAL_ENERGY": {"Unit": "Wh", "Value": day_energy * 365},
            "UAC":          {"Unit": "V",  "Value": uac},
            "UDC":          {"Unit": "V",  "Value": udc},
            "YEAR_ENERGY":  {"Unit": "Wh", "Value": day_energy * 250},
        }
    # CumulationInverterData - Listing 11/12: DAY_ENERGY, YEAR_ENERGY, TOTAL_ENERGY, PAC
    elif collection == "CumulationInverterData":
        data = {
            "DAY_ENERGY":   {"Unit": "Wh", "Value": day_energy},
            "PAC":          {"Unit": "W",  "Value": pac},
            "TOTAL_ENERGY": {"Unit": "Wh", "Value": day_energy * 365},
            "YEAR_ENERGY":  {"Unit": "Wh", "Value": day_energy * 250},
            "DeviceStatus": {
                "ErrorCode": 0,
                "LEDColor": 2,
                "LEDState": 0,
                "MgmtTimerRemainingTime": -1,
                "StateToReset": False,
                "StatusCode": 7,
            },
        }
    # 3PInverterData - Listing 8: IAC_L1, IAC_L2, IAC_L3, UAC_L1, UAC_L2, UAC_L3
    elif collection == "3PInverterData":
        iac_phase = round(iac / 3, 3)
        data = {
            "IAC_L1": {"Unit": "A", "Value": iac_phase},
            "IAC_L2": {"Unit": "A", "Value": iac_phase},
            "IAC_L3": {"Unit": "A", "Value": iac_phase},
            "UAC_L1": {"Unit": "V", "Value": uac},
            "UAC_L2": {"Unit": "V", "Value": uac},
            "UAC_L3": {"Unit": "V", "Value": uac},
        }
    else:
        data = {}

    return web.json_response({"Head": ok_head(req_args), "Body": {"Data": data}})


async def handle_meter_realtime(request: web.Request) -> web.Response:
    """
    Gemaess Fronius Solar API Doku Listing 43 (System) und Listing 45 (Device):
    Feldnamen: CurrentACPhase1, PowerRealPSum, EnergyRealWACMinusAbsolute, etc.
    (CamelCase ohne Unterstriche zwischen Woertern)
    """
    scope     = request.rel_url.query.get("Scope", "System")
    device_id = request.rel_url.query.get("DeviceId", "0")

    async with ClientSession() as session:
        s = await fetch_all_sensors(session)

    # positiv = Netzbezug, negativ = Einspeisung
    p_sum   = float(s["grid"])
    p_phase = round(p_sum / 3, 3)
    uac     = 232.0
    iac     = round(abs(p_sum) / (uac * 3), 3) if p_sum != 0 else 0.0
    ts      = unix_timestamp()

    log.debug(f"Meter: PowerRealPSum={p_sum}W")

    # Feldnamen gemaess Doku Listing 43 (keine Unterstriche zwischen Woertern)
    meter_data = {
        "CurrentACPhase1": iac,
        "CurrentACPhase2": iac,
        "CurrentACPhase3": iac,
        "CurrentACSum":    round(iac * 3, 3),
        "Details": {
            "Manufacturer": "Fronius",
            "Model": "Smart Meter 63A-3",
            "Serial": "SM-EMULATOR-001",
        },
        "Enable": 1,
        "EnergyReactiveVArACSumConsumed": 0,
        "EnergyReactiveVArACSumProduced": 0,
        "EnergyRealWACMinusAbsolute": int(max(0, -p_sum)),
        "EnergyRealWACPlusAbsolute":  int(max(0,  p_sum)),
        "EnergyRealWACSumConsumed":   int(max(0,  p_sum)),
        "EnergyRealWACSumProduced":   int(max(0, -p_sum)),
        "FrequencyPhaseAverage": 50.0,
        "MeterLocationCurrent": 0,
        "PowerApparentSPhase1": round(abs(p_phase), 3),
        "PowerApparentSPhase2": round(abs(p_phase), 3),
        "PowerApparentSPhase3": round(abs(p_phase), 3),
        "PowerApparentSSum":    round(abs(p_sum), 3),
        "PowerFactorPhase1": 1.0,
        "PowerFactorPhase2": 1.0,
        "PowerFactorPhase3": 1.0,
        "PowerFactorSum":    1.0,
        "PowerReactiveQPhase1": 0,
        "PowerReactiveQPhase2": 0,
        "PowerReactiveQPhase3": 0,
        "PowerReactiveQSum":    0,
        # Wirkleistung direkt aus Grid-Sensor
        "PowerRealPPhase1": p_phase,
        "PowerRealPPhase2": p_phase,
        "PowerRealPPhase3": p_phase,
        "PowerRealPSum":    round(p_sum, 3),
        "TimeStamp": ts,
        "Visible": 1,
        "VoltageACPhaseToPhase12": 400.0,
        "VoltageACPhaseToPhase23": 400.0,
        "VoltageACPhaseToPhase31": 400.0,
        "VoltageACPhase1":       uac,
        "VoltageACPhase2":       uac,
        "VoltageACPhase3":       uac,
        "VoltageACPhaseAverage": uac,
    }

    if scope == "System":
        return web.json_response({
            "Head": ok_head({"DeviceClass": "Meter", "Scope": "System"}),
            "Body": {"Data": {"0": meter_data}},
        })
    return web.json_response({
        "Head": ok_head({"DeviceClass": "Meter", "DeviceId": device_id, "Scope": "Device"}),
        "Body": {"Data": meter_data},
    })


async def handle_storage_realtime(request: web.Request) -> web.Response:
    """
    Gemaess Fronius Solar API Doku Listing 48 (Solar Battery):
    Feldnamen: StateOfCharge_Relative, Capacity_Maximum, DesignedCapacity,
               Current_DC, Voltage_DC, Temperature_Cell, Status_BatteryCell
    """
    scope     = request.rel_url.query.get("Scope", "System")
    device_id = request.rel_url.query.get("DeviceId", "0")

    async with ClientSession() as session:
        s = await fetch_all_sensors(session)

    soc       = float(s["soc"])
    bat_power = float(s["battery"])
    ts        = unix_timestamp()
    # Status gemaess Doku: 3=Normal Charge, 5=Normal Discharge, 1=Standby (LG-Chem Werte)
    if bat_power > 50:
        status = 3   # Laden
    elif bat_power < -50:
        status = 5   # Entladen
    else:
        status = 1   # Standby

    storage_data = {
        "Controller": {
            "Capacity_Maximum": 10000,
            "DesignedCapacity": 10000,
            "Current_DC": round(bat_power / 51.2, 2),
            "Details": {
                "Manufacturer": "Fronius",
                "Model": "Fronius Solar Battery 10.0",
                "Serial": "BAT-EMULATOR-001",
            },
            "Enable": 1,
            "StateOfCharge_Relative": soc,
            "Status_BatteryCell": status,
            "Temperature_Cell": 25.0,
            "TimeStamp": ts,
            "Voltage_DC": 51.2,
            "Voltage_DC_Maximum_Cell": 3.65,
            "Voltage_DC_Minimum_Cell": 3.0,
        },
        "Modules": [],
    }

    if scope == "System":
        return web.json_response({
            "Head": ok_head({"DeviceClass": "Storage", "Scope": "System"}),
            "Body": {"Data": {"0": storage_data}},
        })
    return web.json_response({
        "Head": ok_head({"DeviceClass": "Storage", "DeviceId": device_id, "Scope": "Device"}),
        "Body": {"Data": storage_data},
    })


async def handle_powerflow_realtime(request: web.Request) -> web.Response:
    """
    Gemaess Fronius Solar API Doku Listing 57-60:
    Site-Felder: PPV, PGrid, PLoad, PAkku, EDay, ETotal, EYear,
                 MeterLocation, Mode, relAutonomy, relSelfConsumption
    Inverter-Felder: P, SOC, DT, EDay, ETotal, EYear, BatteryMode
    (alle ohne Unterstrich, kein E_Day oder P_PV!)
    """
    async with ClientSession() as session:
        s = await fetch_all_sensors(session)

    pv    = float(s["pv"])
    grid  = float(s["grid"])
    bat   = float(s["battery"])
    load  = float(s["power"])
    soc   = float(s["soc"])
    e_day   = float(s["production_today"])
    e_year  = round(e_day * 250, 1)
    e_total = round(e_day * 365, 1)

    rel_autonomy = (
        min(100.0, round((1 - max(0, grid) / max(1, load)) * 100, 1))
        if load > 0 else 100.0
    )
    rel_self = (
        min(100.0, round((pv - max(0, -grid)) / max(1, pv) * 100, 1))
        if pv > 0 else 0.0
    )

    log.debug(f"PowerFlow: PPV={pv}W PGrid={grid}W PLoad={load}W PAkku={bat}W SOC={soc}%")

    return web.json_response({
        "Head": ok_head({}),
        "Body": {"Data": {
            "Inverters": {"1": {
                # Gemaess Listing 57: BatteryMode, DT, EDay, ETotal, EYear, P, SOC
                "BatteryMode": "normal",
                "DT": 123,
                "EDay":   e_day,
                "ETotal": e_total,
                "EYear":  e_year,
                "P":   pv,
                "SOC": soc,
            }},
            "Site": {
                # Gemaess Listing 57-60: PPV, PGrid, PLoad, PAkku, EDay, ETotal, EYear
                # MeterLocation, Mode, relAutonomy, relSelfConsumption
                "EDay":   e_day,
                "ETotal": e_total,
                "EYear":  e_year,
                "MeterLocation": "grid",
                "Mode": "bidirectional",
                "PAkku": bat  if abs(bat)  > 1 else None,
                "PGrid": grid if grid != 0  else None,
                "PLoad": -load if load != 0 else None,
                "PPV":   pv   if pv > 0    else None,
                "relAutonomy":        rel_autonomy,
                "relSelfConsumption": rel_self,
            },
            "Version": "12",
        }},
    })


def add_routes(app: web.Application, handler, *paths):
    for path in paths:
        app.router.add_get(path, handler)


def create_app() -> web.Application:
    app = web.Application()
    add_routes(app, handle_api_version,
        "/solar_api/GetAPIVersion.cgi",
        "/solar_api/GetAPIVersion.fcgi")
    add_routes(app, handle_logger_info,
        "/solar_api/v1/GetLoggerInfo.cgi",
        "/solar_api/v1/GetLoggerInfo.fcgi")
    add_routes(app, handle_active_device_info,
        "/solar_api/v1/GetActiveDeviceInfo.cgi",
        "/solar_api/v1/GetActiveDeviceInfo.fcgi")
    add_routes(app, handle_inverter_realtime,
        "/solar_api/v1/GetInverterRealtimeData.cgi",
        "/solar_api/v1/GetInverterRealtimeData.fcgi")
    add_routes(app, handle_meter_realtime,
        "/solar_api/v1/GetMeterRealtimeData.cgi",
        "/solar_api/v1/GetMeterRealtimeData.fcgi")
    add_routes(app, handle_storage_realtime,
        "/solar_api/v1/GetStorageRealtimeData.cgi",
        "/solar_api/v1/GetStorageRealtimeData.fcgi")
    add_routes(app, handle_powerflow_realtime,
        "/solar_api/v1/GetPowerFlowRealtimeData.cgi",
        "/solar_api/v1/GetPowerFlowRealtimeData.fcgi")
    return app


if __name__ == "__main__":
    log.info(f"Fronius Solar API Emulator v1.0.7 starting on port {PORT}")
    log.info(f"Sensor PV:               {SENSOR_PV}")
    log.info(f"Sensor Power (Load):     {SENSOR_POWER}")
    log.info(f"Sensor Grid:             {SENSOR_GRID}")
    log.info(f"Sensor SOC:              {SENSOR_SOC}")
    log.info(f"Sensor Battery:          {SENSOR_BATTERY}")
    log.info(f"Sensor Production Today: {SENSOR_PRODUCTION_TODAY}")
    app = create_app()
    web.run_app(app, host="0.0.0.0", port=PORT)
