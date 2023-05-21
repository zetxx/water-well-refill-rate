from counter import sleepAndGet as counterSleepAndGet
from time import time

class Detector:
    metrics = {"rate": 0, "ranFor": 0}
    def __init__(self, counter, safeTime):
        self.counter = counter
        self.safeTime = safeTime
    async def waitForWater(self):
        # detect water first
        noWaterTime = time() + self.safeTime
        while True:
            rate1 = await counterSleepAndGet(self.counter, 1000)
            if rate1 > 1: # water detected for the first time, sleep for some time and check for water once again
                print("1:Water First Time")
                st = time()
                rate2 = await counterSleepAndGet(self.counter, 3000)
                if rate2 > 1: # water still flows
                    print("2:Water flow steady")
                    self.metrics["rate"] = rate1 + rate2
                    self.metrics["ranFor"] = st
                    break
            if noWaterTime < time():
                break
            print("3:No Water")
    async def waitForWaterStops(self):
        while True:
            rate1 = await counterSleepAndGet(self.counter, 1000)
            print("R1:" + str(rate1))
            if rate1 < 7: # no water detected for the first time, sleep for some time and check for water once again
                print("4:No Water First Time")
                ed = time()
                rate2 = await counterSleepAndGet(self.counter, 2000)
                print("R2:" + str(rate2))
                if rate2 < 12: # no water
                    print("5:No Water flow")
                    self.metrics["ranFor"] = ed - self.metrics["ranFor"]
                    break
            self.metrics["rate"] = self.metrics["rate"] + rate1
            print("6:Water Flows")

    async def run(self):
        await self.waitForWater()
        if not self.metrics["ranFor"]:
            print("premature stop")
            return self.metrics
        print("Waiting water stops")
        await self.waitForWaterStops()
        print("Water stopped, sleeping")
        return self.metrics