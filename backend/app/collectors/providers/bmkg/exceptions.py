"""BMKG Collector specific exceptions."""
from app.collectors.exceptions import CollectorException

class BMKGException(CollectorException):
    pass

class BMKGConnectionError(BMKGException):
    pass

class BMKGTimeoutError(BMKGException):
    pass

class BMKGInvalidResponse(BMKGException):
    pass

class BMKGParsingError(BMKGException):
    pass
