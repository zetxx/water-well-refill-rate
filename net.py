from network import WLAN, STA_IF
from uasyncio import sleep_ms

class RetryLimitExceeded(Exception):
    def __init__(self, msg='Retry limit exceeded', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)

async def conn(config):
    wlan = WLAN(STA_IF)
    wlan.active(True)
    wlan.config(dhcp_hostname="pumpctrl")
    retry = config["retry"]
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(config["ssid"], config["password"])
        while True:
            if retry < 0:
                raise RetryLimitExceeded()
            if wlan.isconnected():
                break
            await sleep_ms(500)
            retry = retry - 1
    print('network config:', wlan.ifconfig())