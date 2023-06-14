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
import env
ENV = env.get()
config = conf[ENV]
print("ENV: " + ENV)

# wakeFromDeepSleep = reset_cause() == DEEPSLEEP_RESET
i2c = SoftI2C(scl=Pin(22), sda=Pin(23))
async def runnable():
    await conn(config["wifi"]) # connect to ti wifi
    pm = power(i2c) # get fn for power readings
    metricsPower = await pm();
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
