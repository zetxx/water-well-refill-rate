from uasyncio import run, sleep_ms
from net import conn
from machine import deepsleep #, reset_cause, DEEPSLEEP_RESET
from config import config
from counter import init as initCounter
from detector import Detector
from pump import off as pumpOff, on as pumpOn
from flows.main import flows
from metrics import influxdb

# wakeFromDeepSleep = reset_cause() == DEEPSLEEP_RESET

async def runnable():
    await conn(config["wifi"]) # connect to ti wifi
    await sleep_ms(config["waitForRepl"] * 1000) # sleep for 30 sec if someone tries to connect over serial
    await pumpOn(config["pump"])
    detector = Detector(initCounter(), config["pump"]["safeTimeout"])
    mtrcs = await detector.run()
    await pumpOff(config["pump"])
    flowResult = flows[config["flow"]["type"]](config["flow"], mtrcs)
    print(flowResult)
    print(mtrcs)
    influxdb(config["metrics"], config["sensorId"], mtrcs)
    print("sleep for: " + str(flowResult["runAfter"]))
    deepsleep(flowResult["runAfter"] * 1000) # ms

run(runnable())
