"""River Collector specific exceptions."""
from app.collectors.exceptions import CollectorException

class RiverCollectorException(CollectorException):
    pass

class RiverConnectionError(RiverCollectorException):
    pass

class RiverTimeoutError(RiverCollectorException):
    pass

class RiverInvalidResponse(RiverCollectorException):
    pass

class RiverParsingError(RiverCollectorException):
    pass

class StationOffline(RiverCollectorException):
    pass
