def get():
    f = open('.env')
    env = f.read()
    f.close()
    return env