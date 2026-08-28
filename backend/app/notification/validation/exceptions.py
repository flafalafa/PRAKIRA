"""Validation Framework Exceptions."""
from app.notification.exceptions import NotificationException

class ValidationException(NotificationException):
    pass

class ValidationFailure(ValidationException):
    pass

class SimulationFailure(ValidationException):
    pass

class ConsistencyFailure(ValidationException):
    pass

class ReportingFailure(ValidationException):
    pass
