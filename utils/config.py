import configparser

class Config(object):
    
    def __init__(self):
        self._config = configparser.ConfigParser()
        self._config.read('config.ini')

    def get(self, *args):
        return self._config.get(*args)
