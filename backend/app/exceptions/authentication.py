"""Authentication exceptions."""
from app.exceptions.base import AppException
from app.exceptions.api import UNAUTHORIZED

class AuthenticationException(AppException):
    """Thrown when a user fails to authenticate."""
    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message, error_code=UNAUTHORIZED, status_code=401)
