"""External service exceptions."""
from app.exceptions.base import AppException
from app.exceptions.api import EXTERNAL_SERVICE_ERROR

class ExternalServiceException(AppException):
    """Thrown when a 3rd party API (like weather provider) fails."""
    def __init__(self, message: str, provider: str = "unknown") -> None:
        super().__init__(
            message, 
            error_code=EXTERNAL_SERVICE_ERROR, 
            status_code=502, 
            details=[{"provider": provider}]
        )
