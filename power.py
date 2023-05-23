from machine import Pin, I2C
from ina219 import INA219
from logging import INFO
import time

SHUNT_OHMS = 0.1
# [64, 68]
i2c = I2C(-1, scl=Pin(22), sda=Pin(23))
ina1 = INA219(SHUNT_OHMS, i2c, log_level=INFO, address=0x40)
ina1.configure()
ina2 = INA219(SHUNT_OHMS, i2c, log_level=INFO, address=0x44)
ina2.configure()

while True:
    ina1.wake()
    ina2.wake()
    ina1.sleep()
    ina2.sleep()
    time.sleep(5)
    ina1.wake()
    ina2.wake()
    print("1) Bus Voltage: %.3f V" % ina1.voltage())
    print("1) Current: %.3f mA" % ina1.current())
    print("1) Power: %.3f mW" % ina1.power())

    print("2) Bus Voltage: %.3f V" % ina2.voltage())
    print("2) Current: %.3f mA" % ina2.current())
    print("2) Power: %.3f mW" % ina2.power())