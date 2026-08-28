"""Rate Limiter Exceptions."""
from app.core.exceptions import AppException

class RateLimitExceededException(AppException):
    def __init__(self, message: str = "Rate limit exceeded", retry_after: int = 60):
        super().__init__(message)
        self.retry_after = retry_after

class RequestTooLargeException(AppException):
    def __init__(self, message: str = "Request too large"):
        super().__init__(message)

class ConcurrencyLimitException(AppException):
    def __init__(self, message: str = "Concurrency limit reached. Try again later."):
        super().__init__(message)
