from uasyncio import run
from time import sleep
from net import conn
from machine import deepsleep, wake_reason, DEEPSLEEP
from config import config
from counter import init as initCounter
from detector import Detector
from flows.main import flows

wakeFromDeepSleep = initCounter(), wake_reason() == DEEPSLEEP

async def runnable():
    await conn(config["wifi"])
    detector = Detector()
    metrics = await detector.run(wakeFromDeepSleep)
    flowResult = flows[config["flow"]["type"]](config["flow"], metrics)
    print(flowResult)
    print(metrics)
    # sleep(20)
    print("sleep for: " + flowResult["runAfter"])
    deepsleep(flowResult["runAfter"] * 1000) # ms

run(runnable())
