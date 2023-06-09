import urequests
from time import time

 # https://docs.influxdata.com/influxdb/cloud/api/
def influxdb(config, sensorId, mDetector, mPower):
    print("send metrics")
    qs = "org=" + config["org"]
    qs += "&bucket=" + config["bucket"]
    qs += "&precision=" + config["precision"]
    headers = {"Authorization": " Token " + config["authorization"], "Content-Type": "text/plain; charset=utf-8"}
    print(headers)
    url = config["url"] + "/api/v" + config["version"] + "/write?" + qs
    print(url)
    try:
        ts = urequests.get(config["timestamp"]["url"], timeout=10.0)
        rqdata = "rate,sensorId=" + sensorId + ",pump=1 value=" + str(mDetector["rate"]) + " " + ts.text
        rqdata += "\nranFor,sensorId=" + sensorId + ",pump=1 value=" + str(mDetector["ranFor"]) + " "+ ts.text
        rqdata += "\nV,sensorId=" + sensorId + ",power=x40 value=" + str(mPower["x40"]["v"]) + " "+ ts.text
        rqdata += "\nSV,sensorId=" + sensorId + ",power=x40 value=" + str(mPower["x40"]["sv"]) + " "+ ts.text
        rqdata += "\nA,sensorId=" + sensorId + ",power=x40 value=" + str(mPower["x40"]["a"]) + " "+ ts.text
        rqdata += "\nW,sensorId=" + sensorId + ",power=x40 value=" + str(mPower["x40"]["p"]) + " "+ ts.text
        rqdata += "\nV,sensorId=" + sensorId + ",power=x44 value=" + str(mPower["x44"]["v"]) + " "+ ts.text
        rqdata += "\nSV,sensorId=" + sensorId + ",power=x44 value=" + str(mPower["x44"]["sv"]) + " "+ ts.text
        rqdata += "\nA,sensorId=" + sensorId + ",power=x44 value=" + str(mPower["x44"]["a"]) + " "+ ts.text
        rqdata += "\nW,sensorId=" + sensorId + ",power=x44 value=" + str(mPower["x44"]["p"]) + " "+ ts.text
        ts.close()
        r = urequests.post(url, headers=headers, data=rqdata, timeout=10.0)
        r.close()
    except:
        print("metrics request error")
