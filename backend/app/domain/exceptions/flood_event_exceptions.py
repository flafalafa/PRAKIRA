"""Flood Event domain exceptions."""
from app.exceptions.base import AppException

class FloodEventDomainError(AppException):
    pass

class FloodEventValidationError(FloodEventDomainError):
    pass

class FloodEventStateError(FloodEventDomainError):
    pass

class InvalidFloodDepth(FloodEventValidationError):
    pass

class InvalidEventTime(FloodEventValidationError):
    pass

class InvalidSeverity(FloodEventValidationError):
    pass

class InvalidStatus(FloodEventValidationError):
    pass

class InvalidVerificationState(FloodEventValidationError):
    pass

class FloodEventAlreadyEnded(FloodEventStateError):
    pass
