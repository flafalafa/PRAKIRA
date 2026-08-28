"""Value Object exceptions."""
from app.exceptions.base import AppException

class DomainError(AppException):
    """Base exception for all domain-related errors."""
    pass

class ValueObjectValidationError(DomainError):
    """Raised when a Value Object receives invalid data violating business rules."""
    pass
