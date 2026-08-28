"""Rate limit exceptions."""
from app.exceptions.base import AppException
from app.exceptions.api import RATE_LIMITED

class RateLimitException(AppException):
    """Thrown when a user exceeds API quotas."""
    def __init__(self, message: str = "Too many requests") -> None:
        super().__init__(message, error_code=RATE_LIMITED, status_code=429)
