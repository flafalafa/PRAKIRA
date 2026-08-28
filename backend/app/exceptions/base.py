"""Base application exception."""
from typing import Any

class AppException(Exception):
    """Base exception for all custom PRAKIRA exceptions."""
    
    def __init__(
        self, 
        message: str, 
        error_code: str = "INTERNAL_SERVER_ERROR", 
        status_code: int = 500,
        details: list[Any] | None = None
    ) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or []
