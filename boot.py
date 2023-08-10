from network import WLAN, STA_IF
import ugit
import env
from config import config as conf

ENV = env.get()
config = conf[ENV]
print("ENV: " + ENV)


wlan = WLAN(STA_IF)
wlan.active(True)
wlan.config(dhcp_hostname="pumpctrl")
wlan.connect(config["wifi"]["ssid"], config["wifi"]["password"])
while not wlan.isconnected():
    pass
print(wlan.ifconfig())
# ugit.pull_all(isconnected=True)