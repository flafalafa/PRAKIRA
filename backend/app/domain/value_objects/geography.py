"""Geographic value objects."""
from pydantic import model_validator
from app.domain.value_objects.base import BaseValueObject
from app.domain.value_objects.validators import validate_range, validate_not_empty, validate_positive

class Latitude(BaseValueObject):
    value: float
    
    @model_validator(mode='after')
    def validate_lat(self):
        validate_range(self.value, -90.0, 90.0, "Latitude")
        return self

class Longitude(BaseValueObject):
    value: float
    
    @model_validator(mode='after')
    def validate_lon(self):
        validate_range(self.value, -180.0, 180.0, "Longitude")
        return self

class Coordinate(BaseValueObject):
    latitude: Latitude
    longitude: Longitude

class Distance(BaseValueObject):
    value: float # in meters
    
    @model_validator(mode='after')
    def validate_dist(self):
        validate_positive(self.value, "Distance")
        return self

class AreaCode(BaseValueObject):
    value: str
    
    @model_validator(mode='after')
    def validate_code(self):
        validate_not_empty(self.value, "AreaCode")
        return self

class RiverCode(BaseValueObject):
    value: str
    
    @model_validator(mode='after')
    def validate_code(self):
        validate_not_empty(self.value, "RiverCode")
        return self
