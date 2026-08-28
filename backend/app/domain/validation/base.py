"""Base interfaces and models for domain validation."""
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class ValidationLevel(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

class ValidationMessage(BaseModel):
    level: ValidationLevel
    code: str
    message: str
    field: Optional[str] = None
    
class ValidationResult(BaseModel):
    is_valid: bool = True
    messages: List[ValidationMessage] = Field(default_factory=list)
    
    def add_error(self, code: str, message: str, field: Optional[str] = None):
        self.is_valid = False
        self.messages.append(ValidationMessage(level=ValidationLevel.ERROR, code=code, message=message, field=field))
        
    def add_warning(self, code: str, message: str, field: Optional[str] = None):
        self.messages.append(ValidationMessage(level=ValidationLevel.WARNING, code=code, message=message, field=field))
        
    def merge(self, other: "ValidationResult"):
        if not other.is_valid:
            self.is_valid = False
        self.messages.extend(other.messages)
