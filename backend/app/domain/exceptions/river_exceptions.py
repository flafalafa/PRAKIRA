"""River domain exceptions."""
from app.exceptions.base import AppException

class RiverDomainError(AppException):
    """Base exception for all river domain errors."""
    pass

class RiverValidationError(RiverDomainError):
    """Raised when a river violates a business rule."""
    pass

class RiverStateError(RiverDomainError):
    """Raised when an invalid state transition is attempted on a River."""
    pass

class OverflowThresholdInvalid(RiverValidationError):
    """Raised when water levels violate logical height rules (e.g. Normal > Danger)."""
    pass

class RiverNotActive(RiverStateError):
    """Raised when attempting to update monitoring data on an INACTIVE river."""
    pass

class RiverAlreadyExists(RiverDomainError):
    """Raised when a river with the same code already exists."""
    pass
