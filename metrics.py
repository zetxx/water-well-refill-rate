import urequests

 # https://docs.influxdata.com/influxdb/cloud/api/
def influxdb(config, data):
    print("send metrics")
    qs = "org=" + config["org"]
    qs += "&bucket=" + config["bucket"]
    qs += "&precision=" + config["precision"]
    headers = {"Authorization": " Token" + config["authorization"], "Content-Type": "text/plain; charset=utf-8"}
    data = "rate=100,ranFor=5"
    r = urequests.post(config["url"] + "/api/v" + config["version"] + "/write?" + qs, headers=headers, data=data)
    r.close()
