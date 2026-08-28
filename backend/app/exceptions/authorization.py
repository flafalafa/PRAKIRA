"""Authorization exceptions."""
from app.exceptions.base import AppException
from app.exceptions.api import FORBIDDEN

class AuthorizationException(AppException):
    """Thrown when an authenticated user lacks permissions."""
    def __init__(self, message: str = "Access forbidden") -> None:
        super().__init__(message, error_code=FORBIDDEN, status_code=403)
