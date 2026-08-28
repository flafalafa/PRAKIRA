"""Unit of Work Exceptions."""
from app.exceptions.base import AppException

class UnitOfWorkError(AppException):
    """Base exception for all Unit of Work related errors."""
    pass

class TransactionError(UnitOfWorkError):
    """Raised when a transaction fails to commit or rollback properly."""
    pass
