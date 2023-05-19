from uasyncio import run
from time import sleep
from net import conn
from machine import deepsleep
from config import config
from counter import init as initCounter
from detector import Detector
from flows.main import flows

async def runnable():
    await conn(config["wifi"])
    detector = Detector(initCounter())
    metrics = await detector.run()
    flowResult = flows[config["flow"]["type"]](config["flow"], metrics)
    print(flowResult)
    print(metrics)
    # sleep(20)
    deepsleep(flowResult["runAfter"] * 1000) # ms

run(runnable())