import ugit
import env
from config import config as conf

ENV = env.get()
config = conf[ENV]
print("ENV: " + ENV)


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(config["wifi"]["ssid"], config["wifi"]["password"])
ugit.pull_all()