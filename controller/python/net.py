from network import WLAN, STA_IF
from uasyncio import sleep_ms

async def conn(ssid, key):
    wlan = WLAN(STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, key)
        while True:
            if wlan.isconnected():
                break
            await sleep_ms(500)
    print('network config:', wlan.ifconfig())