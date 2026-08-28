"""Repository exceptions."""
from app.exceptions.base import AppException

class RepositoryError(AppException):
    """Base exception for all repository-related errors."""
    pass

class EntityNotFoundError(RepositoryError):
    """Raised when an entity is not found by ID or criteria."""
    pass

class InvalidSpecificationError(RepositoryError):
    """Raised when an invalid specification is evaluated against a query."""
    pass
