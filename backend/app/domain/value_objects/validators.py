"""Reusable validation logic for Value Objects."""
import re
from app.domain.value_objects.exceptions import ValueObjectValidationError
from app.core.logger import get_logger

logger = get_logger(__name__)

def validate_range(value: float, min_val: float, max_val: float, name: str) -> None:
    """Validates that a numeric value falls within an inclusive range."""
    if value < min_val or value > max_val:
        err = f"{name} must be between {min_val} and {max_val}. Got: {value}"
        logger.warning(f"Validation Failure: {err}")
        raise ValueObjectValidationError(err)

def validate_positive(value: float, name: str) -> None:
    """Validates that a numeric value is not negative."""
    if value < 0:
        err = f"{name} cannot be negative. Got: {value}"
        logger.warning(f"Validation Failure: {err}")
        raise ValueObjectValidationError(err)

def validate_not_empty(value: str, name: str) -> None:
    """Validates that a string is not empty or entirely whitespace."""
    if not value or not str(value).strip():
        err = f"{name} cannot be empty or whitespace."
        logger.warning(f"Validation Failure: {err}")
        raise ValueObjectValidationError(err)
