"""Hydrological value objects."""
from pydantic import model_validator
from app.domain.value_objects.base import BaseValueObject
from app.domain.value_objects.validators import validate_positive

class Rainfall(BaseValueObject):
    value: float # mm
    
    @model_validator(mode='after')
    def validate_val(self):
        validate_positive(self.value, "Rainfall")
        return self

class RainfallIntensity(BaseValueObject):
    value: float # mm/hr
    
    @model_validator(mode='after')
    def validate_val(self):
        validate_positive(self.value, "RainfallIntensity")
        return self

class WaterLevel(BaseValueObject):
    value: float # cm or m
    
    @model_validator(mode='after')
    def validate_val(self):
        validate_positive(self.value, "WaterLevel")
        return self

class RiverFlowRate(BaseValueObject):
    value: float # m^3/s
    
    @model_validator(mode='after')
    def validate_val(self):
        validate_positive(self.value, "RiverFlowRate")
        return self
