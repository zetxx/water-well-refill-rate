import urequests

 # https://docs.influxdata.com/influxdb/cloud/api/
def rq(config, data):
    print("send metrics")
    r = urequests.post(config["url"], headers={"Authorization": " Token" + config["authorization"]})
    r.close()