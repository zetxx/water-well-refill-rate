from uasyncio import sleep_ms, create_task
from machine import Pin, disable_irq, enable_irq
from micropython import alloc_emergency_exception_buf
alloc_emergency_exception_buf(100)

class Counter():
    count = 0

    def inc(self):
        dir = disable_irq()
        self.count = self.count + 1
        enable_irq(dir)

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

async def getAndSleepClear(counter, sleep = 0):
    counter.reset()
    if sleep > 0:
        await sleep_ms(sleep)
    return counter.reset()

async def sleepAndGet(counter, sleep = 0):
    if sleep > 0:
        await sleep_ms(sleep)
    return counter.reset()