"""Not found exceptions."""
from app.exceptions.base import AppException
from app.exceptions.api import NOT_FOUND

class NotFoundException(AppException):
    """Thrown when a requested resource is not found."""
    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message, error_code=NOT_FOUND, status_code=404)
