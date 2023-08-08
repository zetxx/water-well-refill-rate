from time import sleep
from machine import deepsleep, Pin, SoftI2C
# enable power
led = Pin(13, Pin.OUT)
powerLine = Pin(12, Pin.OUT)
powerLine.value(1)
led.value(1)
i2c = SoftI2C(scl=Pin(23), sda=Pin(22))
while(True):
    print(i2c.scan())
    sleep(3)