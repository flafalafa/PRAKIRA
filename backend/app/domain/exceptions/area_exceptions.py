"""Area domain exceptions."""
from app.exceptions.base import AppException

class AreaDomainError(AppException):
    """Base exception for all area domain errors."""
    pass

class AreaValidationError(AreaDomainError):
    """Raised when an area violates a business rule."""
    pass

class AreaStateError(AreaDomainError):
    """Raised when an invalid state transition is attempted on an Area."""
    pass
