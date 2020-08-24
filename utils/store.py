import memcache

class Store():

    HOST = '127.0.0.1'
    PORT = 11211

    def __init__(self):
        self.client = memcache.Client([(self.HOST, self.PORT)])

    def set(self, key, val, ttl=0):
        self.client.set(key, val, time=ttl)
    
    def get (self, key):
        return self.client.get(key)
