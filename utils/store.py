import redis
import json

class Store():

    HOST = 'localhost'
    PORT = 6379
    PWD = ""

    def __init__(self):
        self.client = redis.StrictRedis(host=self.HOST, port=self.PORT, password=self.PWD, decode_responses=True)

    def set_dict(self, key, val):
        # Convert Dict to JSON string
        json_val = json.dumps(val)
        self.client.set(key, json_val)
    
    def get_dict (self, key):
        json_string =  self.client.get(key)
        # Convert JSON string to Dict
        return json.loads(json_string)
