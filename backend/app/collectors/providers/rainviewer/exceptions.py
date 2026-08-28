"""RainViewer Collector specific exceptions."""
from app.collectors.exceptions import CollectorException

class RainViewerException(CollectorException):
    pass

class RainViewerConnectionError(RainViewerException):
    pass

class RainViewerTimeoutError(RainViewerException):
    pass

class RainViewerInvalidResponse(RainViewerException):
    pass

class RainViewerParsingError(RainViewerException):
    pass

class MissingRadarFrame(RainViewerException):
    pass
