"""Domain validation exceptions."""
from app.exceptions.base import AppException

class DomainValidationException(AppException):
    """Base exception for domain validation errors."""
    pass

class CrossEntityValidationError(DomainValidationException):
    """Raised when validation fails across multiple entities."""
    pass

class PolicyViolationError(DomainValidationException):
    """Raised when a business policy is violated."""
    pass

class InvariantViolationError(DomainValidationException):
    """Raised when a domain invariant is broken."""
    pass
