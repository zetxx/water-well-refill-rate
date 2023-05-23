config = {
    "prod": {
    },
    "dev": { # env
        "sensorId": "selqnin1",
        "waitForRepl": 30,
        "wifi": {
            "ssid": "your ssid",
            "password": "your ssid's password",
            "retry": 200
        },
        "flow": {
            "type": "static",
            "runAfter": 60 * 60 * 3
        },
        "pump": {
            "authorization": "authorization header",
            "url": "shelly url",# shelly
            "safeTimeout": 20 # in seconds
        },
        "metrics": { # influxdb
            "org": "?",
            "bucket": "?",
            "precision": "s",
            "version": "2",
            "authorization": "token",
            "url": "?",
            "timestamp": {"url": "timestamp link"}
        }
    }
}