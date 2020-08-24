import logging

class APIException(Exception):
    """Generic exception for APIException """
    def __init__(self, original_exception):
        super(APIException, self).__init__(": %s" % original_exception)
        self.original_exception = original_exception
        logging.error(self.original_exception)
    
class HaltCallbackException(Exception):
    """Generic exception for HaltCallbackException """
    def __init__(self, msg, original_exception):
        super(HaltCallbackException, self).__init__(msg + (": %s" % original_exception))
        self.original_exception = original_exception
        logging.error(self.original_exception)
