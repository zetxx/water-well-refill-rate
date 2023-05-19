from uasyncio import run
from net import conn
from machine import deepsleep
import config
from counter import init as initCounter, getAndSleepClear as counterGetAndSleepClear, sleepAndGet as counterSleepAndGet
from uasyncio import sleep_ms

class Detector:
    metrics = {"rate": 0}
    def __init__(self, counter):
        self.counter = counter
    async def waitForWater(self):
        # detect water first
        while True:
            rate1 = await counterSleepAndGet(self.counter, 1000)
            if rate1 > 1: # water detected for the first time, sleep for some time and check for water once again
                print("1:Water First Time")
                await sleep_ms(2000)
                rate2 = await counterSleepAndGet(self.counter, 1000)
                if rate2 > 1: # water still flows
                    print("2:Water flow steady")
                    self.metrics["rate"] = rate1 + rate2
                    break
            print("3:No Water")
    async def waitForWaterStops(self):
        while True:
            rate = await counterSleepAndGet(self.counter, 1000)
            print(rate)
            if rate < 1: # no water detected for the first time, sleep for some time and check for water once again
                print("5:No Water First Time")
                await sleep_ms(2000)
                if (await counterSleepAndGet(self.counter, 1000)) < 1: # no water
                    print("6:No Water flow")
                    break
            print("7:Water Flows")

    async def run(self):
        await self.waitForWater()
        print("4:Waiting water stops")
        print(self.metrics)
        # await self.waitForWaterStops()
        # print("8:Water stopped, sleeping")

async def runnable():
    # await conn(config.get()["wifi"]["ssid"], config.get()["wifi"]["password"])
    detector = Detector(initCounter())
    await detector.run()
    # print(await counter.get(counter=counterReady, sleep=2000))
    # deepsleep(10000) # ms

run(runnable())