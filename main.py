from uasyncio import run, sleep_ms
from net import conn
from machine import deepsleep, Pin, SoftI2C #, reset_cause, DEEPSLEEP_RESET
from config import config as conf
from counter import init as initCounter
from detector import Detector
from pump import off as pumpOff, on as pumpOn
from flows.main import flows
from metrics import influxdb
from power import power
import ugit

import env
ENV = env.get()
config = conf[ENV]
print("ENV: " + ENV)

# enable power
led = Pin(13, Pin.OUT)
powerLine = Pin(12, Pin.OUT)
powerLine.value(1)
led.value(1)

# wakeFromDeepSleep = reset_cause() == DEEPSLEEP_RESET
i2c = SoftI2C(scl=Pin(23), sda=Pin(22))
async def runnable():
    try:
        await conn(config["wifi"]) # connect to ti wifi
    except:
        deepsleep(600 * 1000) # ms
    ugit.pull_all()
    pm = power(i2c) # get fn for power readings
    metricsPower = await pm()
    await sleep_ms(config["waitForRepl"] * 1000) # sleep for 30 sec if someone tries to connect over serial
    await pumpOn(config["pump"])
    detector = Detector(initCounter(), config["pump"]["safeTimeout"])
    metricsDetector = await detector.run()
    await pumpOff(config["pump"])
    flowResult = flows[config["flow"]["type"]](config["flow"], metricsDetector)
    print(flowResult)
    print(metricsDetector)
    print(metricsPower)
    influxdb(config["metrics"], config["sensorId"], metricsDetector, metricsPower)
    print("sleep for: " + str(flowResult["runAfter"]))
    deepsleep(flowResult["runAfter"] * 1000) # ms

run(runnable())
