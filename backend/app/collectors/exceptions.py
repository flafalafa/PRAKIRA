"""Collector domain exceptions."""
from app.exceptions.base import AppException

class CollectorException(AppException):
    pass

class ProviderUnavailable(CollectorException):
    pass

class InvalidPayload(CollectorException):
    pass

class NormalizationFailed(CollectorException):
    pass

class ValidationFailed(CollectorException):
    pass

class Timeout(CollectorException):
    pass

class RateLimited(CollectorException):
    pass
