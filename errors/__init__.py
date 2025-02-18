__author__ = 'Seetharama'


class BaseError(Exception):
    """Base Error Class"""

    def __init__(self, code=400, message="", status="", field=None):
        Exception.__init__(self)
        self.code = code
        self.message = message
        self.status = status
        self.field = field

    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message,
            "status": self.status,
            "field": self.field,
        }


class BadRequestError(BaseError):
    def __init__(self, message="Bad request error", field=None):
        BaseError.__init__(self)
        self.code = 400
        self.message = message
        self.status = "BAD_REQUEST"
        self.field = field


class ServerError(BaseError):
    def __init__(self, message="Internal server error"):
        BaseError.__init__(self)
        self.code = 500
        self.message = message
        self.status = "SERVER_ERROR"


class RequestKeyError(BaseError):
    def __init__(self, message="Key error"):
        BaseError.__init__(self)
        self.code = 500
        self.message = message
        self.status = "KEY_ERROR"


class RequestValueError(BaseError):
    def __init__(self, message="Value error"):
        BaseError.__init__(self)
        self.code = 500
        self.message = message
        self.status = "VALUE_ERROR"


class ConnectionError(Exception):
    """Base Error Class"""

    def __init__(self, code=400, message="", status="", field=None):
        Exception.__init__(self)
        self.code = code
        self.message = message
        self.status = status
        self.field = field

    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message,
            "status": self.status,
            "field": self.field,
        }


# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""

    pass


class WrongInputError(Error):
    """Raised when the input value is too small"""

    pass


class InternalServerError(Error):
    pass


class BadRequestError(Error):
    pass
