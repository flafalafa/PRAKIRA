"""Standard error response schemas."""
from typing import Any
from pydantic import BaseModel

class ErrorDetails(BaseModel):
    """Details of the error."""
    code: str
    message: str
    details: list[Any] = []
    correlation_id: str
    timestamp: str
    path: str

class ErrorResponse(BaseModel):
    """Standardized API Error Response."""
    success: bool = False
    error: ErrorDetails
