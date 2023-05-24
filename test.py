from machine import Pin, I2C, SoftI2C, sleep
from ina219 import INA219
import logging

SHUNT_OHMS = 0.1
x44 = INA219(SHUNT_OHMS, SoftI2C(scl=Pin(22), sda=Pin(23)), log_level=logging.DEBUG, address=0x44)
x44.configure(INA219.RANGE_16V, bus_adc=INA219.ADC_32SAMP, shunt_adc=INA219.ADC_32SAMP)


while True:
    x44.wake()
    print("------------------------------")
    print("Supply Voltage: %.3f V" % x44.supply_voltage())
    print("Shunt Voltage: %.3f V" % x44.shunt_voltage())
    print("Bus Voltage: %.3f V" % x44.voltage())
    print("Current: %.3f mA" % x44.current())
    print("Power: %.3f mW" % x44.power())
    print("------------------------------")
    x44.sleep()
    sleep(2000)