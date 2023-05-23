import urequests
from time import time

 # https://docs.influxdata.com/influxdb/cloud/api/
def influxdb(config, sensorId, data, powerData):
    print("send metrics")
    qs = "org=" + config["org"]
    qs += "&bucket=" + config["bucket"]
    qs += "&precision=" + config["precision"]
    headers = {"Authorization": " Token " + config["authorization"], "Content-Type": "text/plain; charset=utf-8"}
    print(headers)
    url = config["url"] + "/api/v" + config["version"] + "/write?" + qs
    print(url)
    try:
        ts = urequests.get(config["timestamp"]["url"])
        rqdata = "rate,sensorId=" + sensorId + ",pump=1 value=" + str(data["rate"]) + " " + ts.text
        rqdata += "\nranFor,sensorId=" + sensorId + ",pump=1 value=" + str(data["ranFor"]) + " "+ ts.text
        rqdata += "\nV,sensorId=" + sensorId + ",power=x40 value=" + str(powerData["x40"]["v"]) + " "+ ts.text
        rqdata += "\nA,sensorId=" + sensorId + ",power=x40 value=" + str(powerData["x40"]["a"]) + " "+ ts.text
        rqdata += "\nW,sensorId=" + sensorId + ",power=x40 value=" + str(powerData["x40"]["p"]) + " "+ ts.text
        rqdata += "\nV,sensorId=" + sensorId + ",power=x44 value=" + str(powerData["x44"]["v"]) + " "+ ts.text
        rqdata += "\nA,sensorId=" + sensorId + ",power=x44 value=" + str(powerData["x44"]["a"]) + " "+ ts.text
        rqdata += "\nW,sensorId=" + sensorId + ",power=x44 value=" + str(powerData["x44"]["p"]) + " "+ ts.text
        ts.close()
        r = urequests.post(url, headers=headers, data=rqdata)
        r.close()
    except:
        print("metrics request error")
