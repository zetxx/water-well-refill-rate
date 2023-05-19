from uasyncio import sleep_ms
from machine import Pin
# from micropython import alloc_emergency_exception_buf
# alloc_emergency_exception_buf(100)

class Counter():
    count = 0

    def inc(self):
        self.count = self.count + 1

    def get(self):
        return self.count

    def reset(self):
        cur = self.get()
        self.count = 0
        return cur

def init():
    counter = Counter()
    pin = Pin(34, Pin.IN, pull=Pin.PULL_UP)
    pin.irq(trigger=Pin.IRQ_FALLING, handler=lambda _: counter.inc())
    return counter

async def get(counter, sleep = 0):
    r = counter.reset()
    if sleep > 0:
        await sleep_ms(sleep)
    return r