import urequests
from time import time

 # https://docs.influxdata.com/influxdb/cloud/api/
def influxdb(config, sensorId, data):
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
        rqdata = "rate,sensorId=" + sensorId + " value=" + str(data["rate"]) + " " + ts.text
        rqdata += "\nranFor,sensorId=" + sensorId + " value=" + str(data["ranFor"]) + " "+ ts.text
        ts.close()
        r = urequests.post(url, headers=headers, data=rqdata)
        print(r.text)
        r.close()
    except:
        print("metrics request error")
