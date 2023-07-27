import urequests
from uasyncio import sleep_ms
async def rq(config, state):
    url = config["url"] + state
    print(url)
    try:
        r = urequests.get(url, headers={"authorization": config["authorization"]}, timeout=10.0)
        r.close()
    except:
        print("Can't find pump")
async def on(config):
    print("motor on")
    await rq(config, "on")
async def off(config):
    print("motor off")
    await rq(config, "off")