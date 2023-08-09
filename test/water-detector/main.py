from uasyncio import sleep_ms
from machine import Pin
import time

led = Pin(13, Pin.OUT)
powerLine = Pin(12, Pin.OUT)
powerLine.value(1)
led.value(1)


counterc = 0
def counter(a):
    global counterc
    counterc = counterc + 1
    if (counterc % 20 == 0):
        print('\n')
    print(counterc)

def count():
    pin = Pin(34, Pin.IN, pull=Pin.PULL_UP)
    pin.irq(trigger=Pin.IRQ_FALLING, handler=counter)

count()