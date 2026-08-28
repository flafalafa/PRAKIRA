"""Validation exceptions."""
from typing import Any
from app.exceptions.base import AppException
from app.exceptions.api import VALIDATION_ERROR

class ValidationException(AppException):
    """Thrown when input validation fails manually."""
    def __init__(self, message: str = "Validation failed", details: list[Any] | None = None) -> None:
        super().__init__(message, error_code=VALIDATION_ERROR, status_code=422, details=details)
