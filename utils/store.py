import json
import redis
from utils.config import Config
from utils.exceptions import HaltCallbackException


class Store:
    def __init__(self):
        config = Config()
        self.client = redis.StrictRedis(
            host=config.get("REDIS", "HOST"),
            port=config.get("REDIS", "PORT"),
            password=config.get("REDIS", "PWD"),
            decode_responses=True,
        )

    def set_dict(self, key, val):
        # Convert Dict to JSON string
        json_val = json.dumps(val)
        try:
            self.client.set(key, json_val)
        except redis.exceptions.ConnectionError as err:
            raise HaltCallbackException("Unable to connect", err)

    def get_dict(self, key):
        try:
            json_string = self.client.get(key)
        except redis.exceptions.ConnectionError as err:
            raise HaltCallbackException("Unable to connect", err)

        # Convert JSON string to Dict
        return json.loads(json_string)

