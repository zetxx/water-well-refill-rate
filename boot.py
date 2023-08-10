import env
import ugit
from config import config as conf
from net import conn

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