from uasyncio import run
from time import sleep
from machine import deepsleep
from config import config
from counter import init as initCounter
from detector import Detector
from flows.main import flows

sleep(20)
async def runnable():
    # await conn(config["wifi"]["ssid"], config["wifi"]["password"])
    detector = Detector(initCounter())
    metrics = await detector.run()
    flowResult = flows[config["flow"]["type"]](config["flow"], metrics)
    print(flowResult)
    print(metrics)
    deepsleep(flowResult["runAfter"] * 1000) # ms

run(runnable())