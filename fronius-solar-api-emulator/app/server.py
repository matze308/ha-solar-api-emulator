#!/usr/bin/env python3
"""
Fronius Solar API V1 Emulator for Home Assistant.

Feldnamen gemaess offizieller Fronius Solar API V1 Dokumentation (42,0410,2012,EN 021-15052025).

GetInverterRealtimeData:
  Scope=Device (Listing 7): DAY_ENERGY, YEAR_ENERGY, TOTAL_ENERGY, PAC, FAC, IAC, IDC, UAC, UDC
  Scope=System (Listing 14): DAY_ENERGY {Unit, Values:{"1":...}}, PAC, TOTAL_ENERGY, YEAR_ENERGY
  3PInverterData (Listing 8/9): IAC_L1/L2/L3, UAC_L1/L2/L3

GetMeterRealtimeData (Listing 43/45):
  Current_AC_Phase_1/2/3, Current_AC_Sum
  PowerReal_P_Sum, PowerReal_P_Phase_1/2/3
  EnergyReal_WAC_Minus_Absolute, EnergyReal_WAC_Plus_Absolute
  EnergyReal_WAC_Sum_Consumed, EnergyReal_WAC_Sum_Produced
  Frequency_Phase_Average, Meter_Location_Current
  Voltage_AC_Phase_1/2/3, Voltage_AC_PhaseToPhase_12/23/31
  PowerApparent_S_Sum, PowerFactor_Sum, PowerReactive_Q_Sum

GetStorageRealtimeData (Listing 47/48):
  StateOfCharge_Relative, Capacity_Maximum, DesignedCapacity
  Current_DC, Voltage_DC, Temperature_Cell, Status_BatteryCell
  Voltage_DC_Maximum_Cell, Voltage_DC_Minimum_Cell

GetPowerFlowRealtimeData (Listing 56-60):
  Site: P_PV, P_Grid, P_Load, P_Akku, E_Day, E_Total, E_Year
        Meter_Location, Mode, rel_Autonomy, rel_SelfConsumption
  Inverters: P, SOC, DT, E_Day, E_Total, E_Year, Battery_Mode, CID
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
    """RFC3339-Zeitstempel in Lokalzeit."""
    return datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")


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
                state = data.get("state", "0")
                if state in ("unavailable", "unknown", None, ""):
                    return 0.0
                return float(state)
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
# /solar_api/GetAPIVersion.cgi
# ---------------------------------------------------------------------------

async def handle_api_version(request: web.Request) -> web.Response:
    return web.json_response({
        "APIVersion": 1,
        "BaseURL": "/solar_api/v1/",
        "CompatibilityRange": "1.5-9",
    })


# ---------------------------------------------------------------------------
# /solar_api/v1/GetLoggerInfo.cgi
# ---------------------------------------------------------------------------

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
                "TimezoneLocation": "Berlin",
                "TimezoneName": "CEST",
                "UTCOffset": 7200,
                "UniqueID": "HA-SOLAR-EMULATOR-001",
            }
        },
    })


# ---------------------------------------------------------------------------
# /solar_api/v1/GetInverterInfo.cgi  (Listing 31-33)
# ---------------------------------------------------------------------------

async def handle_inverter_info(request: web.Request) -> web.Response:
    return web.json_response({
        "Head": ok_head({}),
        "Body": {
            "Data": {
                "1": {
                    "CustomName": "Emulated Inverter",
                    "DT": 1,
                    "ErrorCode": 0,
                    "PVPower": 10000,
                    "Show": 1,
                    "StatusCode": 7,
                    "InverterState": "Running",
                    "UniqueID": "INV-EMULATOR-001",
                }
            }
        },
    })


# ---------------------------------------------------------------------------
# /solar_api/v1/GetActiveDeviceInfo.cgi  (Listing 34-41)
# ---------------------------------------------------------------------------

async def handle_active_device_info(request: web.Request) -> web.Response:
    device_class = request.rel_url.query.get("DeviceClass", "System")

    if device_class == "System":
        data = {
            "Inverter":      {"1": {"DT": 1, "Serial": "INV-EMULATOR-001"}},
            "Meter":         {"0": {"DT": -1, "Serial": "SM-EMULATOR-001"}},
            "Storage":       {"0": {"DT": -1, "Serial": "BAT-EMULATOR-001"}},
            "Ohmpilot":      {},
            "SensorCard":    {},
            "StringControl": {},
        }
    elif device_class == "Inverter":
        data = {"1": {"DT": 1, "Serial": "INV-EMULATOR-001"}}
    elif device_class == "Meter":
        data = {"0": {"DT": -1, "Serial": "SM-EMULATOR-001"}}
    elif device_class == "Storage":
        data = {"0": {"DT": -1, "Serial": "BAT-EMULATOR-001"}}
    else:
        data = {}

    return web.json_response({
        "Head": ok_head({"DeviceClass": device_class}),
        "Body": {"Data": data},
    })


# ---------------------------------------------------------------------------
# /solar_api/v1/GetInverterRealtimeData.cgi
# ---------------------------------------------------------------------------

async def handle_inverter_realtime(request: web.Request) -> web.Response:
    """
    Listing 7  - CommonInverterData  (Scope=Device)
    Listing 14 - CumulationInverterData (Scope=System)
    Listing 8/9 - 3PInverterData
    Listing 11/12 - CumulationInverterData (Scope=Device)
    """
    scope      = request.rel_url.query.get("Scope", "Device")
    device_id  = request.rel_url.query.get("DeviceId", "1")
    collection = request.rel_url.query.get("DataCollection", "CommonInverterData")

    async with ClientSession() as session:
        s = await fetch_all_sensors(session)

    pac          = float(s["pv"])
    day_energy   = float(s["production_today"])  # Wh
    year_energy  = round(day_energy * 250, 1)
    total_energy = round(day_energy * 365, 1)
    uac = 230.0
    udc = 380.0
    iac = round(pac / (uac * 3), 3) if pac > 0 else 0.0
    idc = round(pac / udc, 3)       if pac > 0 else 0.0

    # ---- Scope=System: Listing 14 - Values-Objekt statt Value ----
    if scope == "System":
        return web.json_response({
            "Head": ok_head({"DeviceClass": "Inverter", "Scope": "System"}),
            "Body": {"Data": {
                "DAY_ENERGY":   {"Unit": "Wh", "Values": {"1": day_energy}},
                "PAC":          {"Unit": "W",  "Values": {"1": pac}},
                "TOTAL_ENERGY": {"Unit": "Wh", "Values": {"1": total_energy}},
                "YEAR_ENERGY":  {"Unit": "Wh", "Values": {"1": year_energy}},
            }},
        })

    req_args = {
        "DataCollection": collection,
        "DeviceClass": "Inverter",
        "DeviceId": device_id,
        "Scope": scope,
    }

    # ---- CommonInverterData (Listing 7) ----
    if collection == "CommonInverterData":
        data = {
            "DAY_ENERGY": {"Unit": "Wh", "Value": day_energy},
            "DeviceStatus": {
                "ErrorCode": 0,
                "InverterState": "Running",
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
            "TOTAL_ENERGY": {"Unit": "Wh", "Value": total_energy},
            "UAC":          {"Unit": "V",  "Value": uac},
            "UDC":          {"Unit": "V",  "Value": udc},
            "YEAR_ENERGY":  {"Unit": "Wh", "Value": year_energy},
        }

    # ---- CumulationInverterData (Listing 11/12) ----
    elif collection == "CumulationInverterData":
        data = {
            "DAY_ENERGY":   {"Unit": "Wh", "Value": day_energy},
            "PAC":          {"Unit": "W",  "Value": pac},
            "TOTAL_ENERGY": {"Unit": "Wh", "Value": total_energy},
            "YEAR_ENERGY":  {"Unit": "Wh", "Value": year_energy},
            "DeviceStatus": {
                "ErrorCode": 0,
                "InverterState": "Running",
                "StatusCode": 7,
            },
        }

    # ---- 3PInverterData (Listing 8/9) ----
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


# ---------------------------------------------------------------------------
# /solar_api/v1/GetMeterRealtimeData.cgi
# ---------------------------------------------------------------------------

async def handle_meter_realtime(request: web.Request) -> web.Response:
    """
    Listing 42-45: Feldnamen EXAKT wie in der Doku (Unterstriche!):
      Current_AC_Phase_1, Current_AC_Phase_2, Current_AC_Phase_3, Current_AC_Sum
      PowerReal_P_Sum, PowerReal_P_Phase_1/2/3
      EnergyReal_WAC_Minus_Absolute, EnergyReal_WAC_Plus_Absolute
      EnergyReal_WAC_Sum_Consumed, EnergyReal_WAC_Sum_Produced
      EnergyReactive_VArAC_Sum_Consumed, EnergyReactive_VArAC_Sum_Produced
      Frequency_Phase_Average, Meter_Location_Current
      PowerApparent_S_Phase_1/2/3, PowerApparent_S_Sum
      PowerFactor_Phase_1/2/3, PowerFactor_Sum
      PowerReactive_Q_Phase_1/2/3, PowerReactive_Q_Sum
      TimeStamp, Enable, Visible
      Voltage_AC_Phase_1/2/3, Voltage_AC_PhaseToPhase_12/23/31
    """
    scope     = request.rel_url.query.get("Scope", "System")
    device_id = request.rel_url.query.get("DeviceId", "0")

    async with ClientSession() as session:
        s = await fetch_all_sensors(session)

    # positiv = Netzbezug, negativ = Einspeisung
    p_sum   = float(s["grid"])
    p_phase = round(p_sum / 3, 3)
    uac     = 232.0
    # Vorzeichenbehafteter Strom (wie UL/TS-Meter laut Doku)
    iac_sign = round(p_sum / (uac * 3), 3)
    ts      = unix_timestamp()

    log.debug(f"Meter: PowerReal_P_Sum={p_sum}W")

    meter_data = {
        "Current_AC_Phase_1": iac_sign,
        "Current_AC_Phase_2": iac_sign,
        "Current_AC_Phase_3": iac_sign,
        "Current_AC_Sum":     round(iac_sign * 3, 3),
        "Details": {
            "Manufacturer": "Fronius",
            "Model": "Smart Meter 63A-3",
            "Serial": "SM-EMULATOR-001",
        },
        "Enable": 1,
        "EnergyReactive_VArAC_Sum_Consumed": 0,
        "EnergyReactive_VArAC_Sum_Produced": 0,
        # WAC_Minus = Export zum Netz (Einspeisung)
        # WAC_Plus  = Import vom Netz (Bezug)
        "EnergyReal_WAC_Minus_Absolute": max(0, round(-p_sum)),
        "EnergyReal_WAC_Plus_Absolute":  max(0, round( p_sum)),
        "EnergyReal_WAC_Sum_Consumed":   max(0, round( p_sum)),
        "EnergyReal_WAC_Sum_Produced":   max(0, round(-p_sum)),
        "Frequency_Phase_Average": 50.0,
        "Meter_Location_Current": 0,
        "PowerApparent_S_Phase_1": round(abs(p_phase), 3),
        "PowerApparent_S_Phase_2": round(abs(p_phase), 3),
        "PowerApparent_S_Phase_3": round(abs(p_phase), 3),
        "PowerApparent_S_Sum":     round(abs(p_sum), 3),
        "PowerFactor_Phase_1": 1.0,
        "PowerFactor_Phase_2": 1.0,
        "PowerFactor_Phase_3": 1.0,
        "PowerFactor_Sum":     1.0,
        "PowerReactive_Q_Phase_1": 0,
        "PowerReactive_Q_Phase_2": 0,
        "PowerReactive_Q_Phase_3": 0,
        "PowerReactive_Q_Sum":     0,
        "PowerReal_P_Phase_1": p_phase,
        "PowerReal_P_Phase_2": p_phase,
        "PowerReal_P_Phase_3": p_phase,
        "PowerReal_P_Sum":     round(p_sum, 3),
        "TimeStamp": ts,
        "Visible": 1,
        "Voltage_AC_PhaseToPhase_12": 400.0,
        "Voltage_AC_PhaseToPhase_23": 400.0,
        "Voltage_AC_PhaseToPhase_31": 400.0,
        "Voltage_AC_Phase_1": uac,
        "Voltage_AC_Phase_2": uac,
        "Voltage_AC_Phase_3": uac,
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


# ---------------------------------------------------------------------------
# /solar_api/v1/GetStorageRealtimeData.cgi
# ---------------------------------------------------------------------------

async def handle_storage_realtime(request: web.Request) -> web.Response:
    """
    Listing 47-51: Feldnamen EXAKT wie in der Doku:
      StateOfCharge_Relative, Capacity_Maximum, DesignedCapacity
      Current_DC, Voltage_DC, Temperature_Cell, Status_BatteryCell
      Voltage_DC_Maximum_Cell, Voltage_DC_Minimum_Cell
      Enable, TimeStamp
    Status_BatteryCell (LG-Chem Controller):
      1=STANDBY, 3=ENABLED, 5=FAULTED, 10=SLEEP
    """
    scope     = request.rel_url.query.get("Scope", "System")
    device_id = request.rel_url.query.get("DeviceId", "0")

    async with ClientSession() as session:
        s = await fetch_all_sensors(session)

    soc       = float(s["soc"])
    bat_power = float(s["battery"])  # positiv=Laden, negativ=Entladen
    ts        = unix_timestamp()
    voltage   = 51.2

    # Status_BatteryCell (LG-Chem Controller-Tabelle laut Doku):
    # 1=STANDBY, 3=ENABLED, 5=FAULTED, 10=SLEEP
    if abs(bat_power) > 50:
        bat_status = 3   # ENABLED
    else:
        bat_status = 1   # STANDBY

    storage_data = {
        "Controller": {
            "Capacity_Maximum":  10000,
            "DesignedCapacity":  10000,
            "Current_DC": round(bat_power / voltage, 2),
            "Details": {
                "Manufacturer": "Fronius",
                "Model": "Fronius Solar Battery 10.0",
                "Serial": "BAT-EMULATOR-001",
            },
            "Enable": 1,
            "StateOfCharge_Relative": soc,
            "Status_BatteryCell": bat_status,
            "Temperature_Cell": 25.0,
            "TimeStamp": ts,
            "Voltage_DC": voltage,
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


# ---------------------------------------------------------------------------
# /solar_api/v1/GetPowerFlowRealtimeData.fcgi
# ---------------------------------------------------------------------------

async def handle_powerflow_realtime(request: web.Request) -> web.Response:
    """
    Listing 56-60: Feldnamen EXAKT wie in der Doku (Unterstriche!):
    Site:
      P_PV, P_Grid, P_Load, P_Akku
      E_Day, E_Total, E_Year
      Meter_Location, Mode
      rel_Autonomy, rel_SelfConsumption
      BackupMode, BatteryStandby
    Inverters["1"]:
      P, SOC, DT, CID
      E_Day, E_Total, E_Year
      Battery_Mode
    """
    async with ClientSession() as session:
        s = await fetch_all_sensors(session)

    pv    = float(s["pv"])           # W, PV-Erzeugung
    grid  = float(s["grid"])         # W, positiv=Bezug, negativ=Einspeisung
    bat   = float(s["battery"])      # W, positiv=Laden, negativ=Entladen
    load  = float(s["power"])        # W, Hausverbrauch (positiv)
    soc   = float(s["soc"])
    e_day   = float(s["production_today"])  # Wh
    e_year  = round(e_day * 250, 1)
    e_total = round(e_day * 365, 1)

    # rel_Autonomy: Anteil des Verbrauchs aus eigener Erzeugung
    rel_autonomy = (
        min(100.0, round((1 - max(0.0, grid) / max(1.0, load)) * 100, 1))
        if load > 0 else 100.0
    )
    # rel_SelfConsumption: Anteil der PV-Produktion, der direkt verbraucht wird
    rel_self = (
        min(100.0, round((pv - max(0.0, -grid)) / max(1.0, pv) * 100, 1))
        if pv > 0 else 0.0
    )

    battery_standby = abs(bat) < 50

    log.debug(f"PowerFlow: P_PV={pv}W P_Grid={grid}W P_Load={load}W P_Akku={bat}W SOC={soc}%")

    return web.json_response({
        "Head": ok_head({}),
        "Body": {"Data": {
            "Inverters": {"1": {
                "Battery_Mode": "normal",
                "CID": 16843009,
                "DT": 1,
                "E_Day":   e_day   if e_day > 0   else None,
                "E_Total": e_total if e_total > 0 else None,
                "E_Year":  e_year  if e_year > 0  else None,
                "P":   pv,
                "SOC": soc,
            }},
            "Site": {
                "BackupMode":     False,
                "BatteryStandby": battery_standby,
                "E_Day":   e_day   if e_day > 0   else None,
                "E_Total": e_total if e_total > 0 else None,
                "E_Year":  e_year  if e_year > 0  else None,
                "Meter_Location": "grid",
                "Mode": "bidirectional",
                "P_Akku": bat  if abs(bat) > 1  else None,
                "P_Grid": grid if grid != 0      else None,
                "P_Load": -load if load != 0     else None,
                "P_PV":   pv   if pv > 0         else None,
                "rel_Autonomy":        rel_autonomy,
                "rel_SelfConsumption": rel_self,
            },
            "Version": "12",
        }},
    })


# ---------------------------------------------------------------------------
# App Factory
# ---------------------------------------------------------------------------

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

    add_routes(app, handle_inverter_info,
        "/solar_api/v1/GetInverterInfo.cgi",
        "/solar_api/v1/GetInverterInfo.fcgi")

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
    log.info(f"Fronius Solar API Emulator v1.1.0 starting on port {PORT}")
    log.info(f"Sensor PV:               {SENSOR_PV}")
    log.info(f"Sensor Power (Load):     {SENSOR_POWER}")
    log.info(f"Sensor Grid:             {SENSOR_GRID}")
    log.info(f"Sensor SOC:              {SENSOR_SOC}")
    log.info(f"Sensor Battery:          {SENSOR_BATTERY}")
    log.info(f"Sensor Production Today: {SENSOR_PRODUCTION_TODAY}")
    app = create_app()
    web.run_app(app, host="0.0.0.0", port=PORT)
