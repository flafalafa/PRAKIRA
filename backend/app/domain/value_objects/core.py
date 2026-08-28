"""Core common value objects."""
from datetime import datetime, timezone
from pydantic import model_validator
from app.domain.value_objects.base import BaseValueObject
from app.domain.value_objects.validators import validate_positive
from app.domain.value_objects.exceptions import ValueObjectValidationError

class TimestampUTC(BaseValueObject):
    value: datetime
    
    @model_validator(mode='after')
    def validate_val(self):
        # Must be timezone aware
        if self.value.tzinfo is None or self.value.tzinfo.utcoffset(self.value) is None:
            raise ValueObjectValidationError("TimestampUTC must be timezone-aware.")
        
        # Coerce strictly to UTC
        if self.value.tzinfo != timezone.utc:
            object.__setattr__(self, 'value', self.value.astimezone(timezone.utc))
            
        return self

class Duration(BaseValueObject):
    value: float # seconds
    
    @model_validator(mode='after')
    def validate_val(self):
        validate_positive(self.value, "Duration")
        return self
