from counter import sleepAndGet as counterSleepAndGet

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
                rate2 = await counterSleepAndGet(self.counter, 3000)
                if rate2 > 1: # water still flows
                    print("2:Water flow steady")
                    self.metrics["rate"] = rate1 + rate2
                    break
            print("3:No Water")
    async def waitForWaterStops(self):
        while True:
            rate1 = await counterSleepAndGet(self.counter, 1000)
            if rate1 < 1: # no water detected for the first time, sleep for some time and check for water once again
                print("5:No Water First Time")
                rate2 = await counterSleepAndGet(self.counter, 3000)
                if rate2 < 1: # no water
                    print("6:No Water flow")
                    break
            self.metrics["rate"] = self.metrics["rate"] + rate1
            print("7:Water Flows")

    async def run(self):
        await self.waitForWater()
        print("4:Waiting water stops")
        await self.waitForWaterStops()
        print("8:Water stopped, sleeping")
        return self.metrics