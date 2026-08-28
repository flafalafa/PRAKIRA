"""Analysis and scoring value objects."""
from enum import Enum
from pydantic import model_validator
from app.domain.value_objects.base import BaseValueObject
from app.domain.value_objects.validators import validate_range

class RiskScore(BaseValueObject):
    value: float # 0 to 100
    
    @model_validator(mode='after')
    def validate_val(self):
        validate_range(self.value, 0.0, 100.0, "RiskScore")
        return self

class PredictionConfidence(BaseValueObject):
    value: float # 0.0 to 1.0
    
    @model_validator(mode='after')
    def validate_val(self):
        validate_range(self.value, 0.0, 1.0, "PredictionConfidence")
        return self

class NotificationPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
