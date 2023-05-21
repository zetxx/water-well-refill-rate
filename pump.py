import urequests

def rq(config, state):
    url = config["url"] + state
    print(url)
    r = urequests.get(url, headers={"authorization": config["authorization"]})
    r.close()
def on(config):
    print("motor on")
    rq(config, "on")
def off(config):
    print("motor off")
    rq(config, "off")