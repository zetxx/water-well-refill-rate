from uasyncio import run
import ugit
import env
from net import conn
from config import config as conf

ENV = env.get()
config = conf[ENV]
print("ENV: " + ENV)


async def runnable():
    try:
        await conn(config["wifi"]) # connect to ti wifi
    except:
        deepsleep(600 * 1000) # ms

run(runnable())

# ugit.backup()
ugit.pull_all()