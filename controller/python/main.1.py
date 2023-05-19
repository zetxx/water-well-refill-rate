import time
from machine import Pin, ADC
from net import conn
import urequests

conn('aaaa', 'aaaa')

adc = ADC(Pin(34))
# adc.atten(ADC.ATTN_11DB);
def smooth_reading():
    avg = 0
    _AVG_NUM = 100
    for _ in range(_AVG_NUM):
        avg += adc.read()
    avg /= _AVG_NUM
    return(avg)


_THRESHOLD = 3000.0

while True:
    s1 = 0
    s2 = 0
    while True:
        analog_val = smooth_reading()
        print(analog_val)
        if analog_val > _THRESHOLD:
            if s1 > 9:
                r = urequests.get("http://storage.zetxx.eu:3000/water/1")
                r.close()
                print("S1: Water detected!")
                break
            s1 = s1 + 1
        else:
            s1 = 0
            print("S1: Water NOT detected!")
        time.sleep(1)
    s1 = 0
    s2 = 0
    while True:
        analog_val = smooth_reading()
        print(analog_val)
        if analog_val > _THRESHOLD:
            Pin(13, Pin.IN, Pin.PULL_UP)
            print("S2: Water detected!")
            s2 = 0
        else:
            Pin(13, Pin.IN, Pin.PULL_DOWN)
            if s2 > 2:
                print("S2: Water NOT detected!")
                r = urequests.get("http://storage.zetxx.eu:3000/water/0")
                r.close()
                break
            s2 = s2 + 1
        time.sleep(1)
