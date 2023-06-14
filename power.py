from ina219 import INA219
from logging import ERROR

SHUNT_OHMS = 0.1
# [64, 68]

def read(x40, x44):
    async def read_():
        r = {"x40": {}, "x44": {}}
        x40.wake()
        x44.wake()
        r["x40"]["v"] = x40.voltage()
        r["x40"]["sv"] = x40.shunt_voltage()
        r["x40"]["a"] = x40.current()
        r["x40"]["p"] = x40.power()
        r["x44"]["v"] = x44.voltage()
        r["x44"]["sv"] = x44.shunt_voltage()
        r["x44"]["a"] = x44.current()
        r["x44"]["p"] = x44.power()
        x40.sleep()
        x44.sleep()
        return r
    return read_
async def dummyRead():
    return {"x40": {"v": 0, "sv": 0, "a": 0, "p": 0}, "x44": {"v": 0, "sv": 0, "a": 0, "p": 0}}

def power(i2c):
    try:
        x40 = INA219(SHUNT_OHMS, i2c, log_level=ERROR, address=0x40)
        x44 = INA219(SHUNT_OHMS, i2c, log_level=ERROR, address=0x44)
        x40.configure(INA219.RANGE_16V, bus_adc=INA219.ADC_32SAMP, shunt_adc=INA219.ADC_32SAMP)
        x44.configure(INA219.RANGE_16V, bus_adc=INA219.ADC_32SAMP, shunt_adc=INA219.ADC_32SAMP)
        read(x40, x44)
        return read(x40, x44)
    except:
        return dummyRead
