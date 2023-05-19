from uasyncio import run
from time import sleep
from net import conn
from machine import deepsleep, reset_cause, DEEPSLEEP_RESET
from config import config
from counter import init as initCounter
from detector import Detector
from pump import off as pumpOff, on as pumpOn
from flows.main import flows

wakeFromDeepSleep = reset_cause() == DEEPSLEEP_RESET

async def runnable():
    await conn(config["wifi"])
    if wakeFromDeepSleep:
        pumpOn()
    detector = Detector(initCounter())
    metrics = await detector.run(wakeFromDeepSleep)
    pumpOff()
    flowResult = flows[config["flow"]["type"]](config["flow"], metrics)
    print(flowResult)
    print(metrics)
    # sleep(20)
    print("sleep for: " + str(flowResult["runAfter"]))
    deepsleep(flowResult["runAfter"] * 1000) # ms

run(runnable())
