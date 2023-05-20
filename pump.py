import urequests

def rq(config, state):
    r = urequests.get(config["url"] + state, headers={"authorization": config["authorization"]})
    r.close()
def on(config):
    print("motor on")
    rq(config, "on")
def off(config):
    print("motor off")
    rq(config, "off")