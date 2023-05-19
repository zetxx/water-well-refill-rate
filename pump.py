def rq(config, state):
    print(config["url"])
    print(config["authorization"])
def on(config):
    print("motor on")
    rq(config, "on")
def off(config):
    print("motor off")
    rq(config, "off")