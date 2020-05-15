class TDException(Exception):
    # Base class for all exceptions within this library
    pass

class APIException(TDException):
    def __init__(self, error_message):
        super(APIException, self).__init__(error_message)
        self.message = error_message

class ClientException(TDException):

    def __init__(self, error_message):
        super(ClientException, self).__init__(error_message)
        self.message = error_message


