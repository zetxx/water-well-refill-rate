from uasyncio import run
from net import conn
from machine import deepsleep, reset_cause, DEEPSLEEP_RESET
from config import config
from counter import init as initCounter
from detector import Detector
from pump import off as pumpOff, on as pumpOn
from flows.main import flows
from metrics import influxdb

wakeFromDeepSleep = reset_cause() == DEEPSLEEP_RESET

async def runnable():
    await conn(config["wifi"])
    pumpOn(config["pump"])
    detector = Detector(initCounter(), config["pump"]["safeTimeout"])
    mtrcs = await detector.run()
    pumpOff(config["pump"])
    flowResult = flows[config["flow"]["type"]](config["flow"], mtrcs)
    print(flowResult)
    print(mtrcs)
    influxdb(config["metrics"], config["sensorId"], mtrcs)
    print("sleep for: " + str(flowResult["runAfter"]))
    deepsleep(flowResult["runAfter"] * 1000) # ms

run(runnable())
