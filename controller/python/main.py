from uasyncio import run
from net import conn
import config
import counter

async def runnable():
    await conn(config.get()["wifi"]["ssid"], config.get()["wifi"]["password"])
    counterReady = counter.init()
    print(await counter.get(counter=counterReady, sleep=2000))
    print(await counter.get(counter=counterReady, sleep=2000))
    print(await counter.get(counter=counterReady, sleep=2000))
    print(await counter.get(counter=counterReady, sleep=2000))
    print(await counter.get(counter=counterReady, sleep=2000))
    print(await counter.get(counter=counterReady, sleep=2000))
    print(await counter.get(counter=counterReady, sleep=2000))
    print(await counter.get(counter=counterReady, sleep=2000))
    print(await counter.get(counter=counterReady, sleep=2000))
    print(await counter.get(counter=counterReady, sleep=2000))

run(runnable())