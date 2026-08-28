"""Business logic exceptions."""
from app.exceptions.base import AppException
from app.exceptions.api import CONFLICT

class BusinessException(AppException):
    """Thrown when a domain business rule is violated."""
    def __init__(self, message: str, error_code: str = CONFLICT, status_code: int = 409) -> None:
        super().__init__(message, error_code=error_code, status_code=status_code)
