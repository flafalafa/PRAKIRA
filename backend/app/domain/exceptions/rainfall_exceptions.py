"""Rainfall domain exceptions."""
from app.exceptions.base import AppException

class RainfallDomainError(AppException):
    pass

class RainfallValidationError(RainfallDomainError):
    pass

class InvalidRainfallAmount(RainfallValidationError):
    pass

class InvalidObservationTime(RainfallValidationError):
    pass

class InvalidAccumulationPeriod(RainfallValidationError):
    pass

class InvalidConfidenceScore(RainfallValidationError):
    pass

class InvalidRainfallCategory(RainfallValidationError):
    pass

class RainfallNotValidated(RainfallDomainError):
    """Raised when an operation requires validated rainfall data, but it is raw or unvalidated."""
    pass
