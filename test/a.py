from uasyncio import sleep_ms
from machine import Pin
import time

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

def power():
    led = Pin(13, Pin.OUT)
    ledp = Pin(12, Pin.OUT)
    for i in range(1000):
        led.value(1)
        ledp.value(1)
        time.sleep(60)
        led.value(0)
        ledp.value(0)
        time.sleep(10)