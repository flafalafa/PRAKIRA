"""Weather value objects."""
from pydantic import model_validator
from app.domain.value_objects.base import BaseValueObject
from app.domain.value_objects.validators import validate_positive, validate_range
from app.domain.value_objects.exceptions import ValueObjectValidationError

class WindSpeed(BaseValueObject):
    value: float # km/h
    
    @model_validator(mode='after')
    def validate_val(self):
        validate_positive(self.value, "WindSpeed")
        return self

class WindDirection(BaseValueObject):
    value: str 
    
    @model_validator(mode='after')
    def validate_val(self):
        valid_directions = [
            "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", 
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
        ]
        
        normalized = str(self.value).strip().upper()
        if normalized not in valid_directions:
            raise ValueObjectValidationError(
                f"Invalid WindDirection: {self.value}. Must be a valid compass direction (e.g. N, NW, SE)."
            )
            
        # Pydantic v2 frozen models require using object.__setattr__ if modifying fields internally
        object.__setattr__(self, 'value', normalized)
        return self

class Temperature(BaseValueObject):
    value: float # Celsius

class Humidity(BaseValueObject):
    value: float # percentage 0-100
    
    @model_validator(mode='after')
    def validate_val(self):
        validate_range(self.value, 0.0, 100.0, "Humidity")
        return self

class Pressure(BaseValueObject):
    value: float # hPa
    
    @model_validator(mode='after')
    def validate_val(self):
        validate_positive(self.value, "Pressure")
        return self
