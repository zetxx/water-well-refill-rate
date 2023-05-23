from machine import Pin, I2C
from ina219 import INA219
from logging import INFO

SHUNT_OHMS = 0.1
# [64, 68]

def read(x40, x44):
    r = {"x40": {}, "x44": {}}
    x40.wake()
    x44.wake()
    r["x40"]["v"] = x40.voltage()
    r["x40"]["a"] = x40.current()
    r["x40"]["p"] = x40.power()
    r["x44"]["v"] = x44.voltage()
    r["x44"]["a"] = x44.current()
    r["x44"]["p"] = x44.power()
    x40.sleep()
    x44.sleep()
    return r

def power():
    i2c = I2C(-1, scl=Pin(22), sda=Pin(23))
    x40 = INA219(SHUNT_OHMS, i2c, log_level=INFO, address=0x40)
    x44 = INA219(SHUNT_OHMS, i2c, log_level=INFO, address=0x44)
    x40.configure()
    x44.configure()
    return lambda : read(x40, x44)
