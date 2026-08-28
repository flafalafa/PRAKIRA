"""Base class for all Value Objects."""
from abc import ABC
from typing import Any, Dict
from pydantic import BaseModel, ConfigDict

class BaseValueObject(BaseModel, ABC):
    """
    Abstract base class for all Domain Value Objects.
    Enforces immutability via Pydantic frozen configuration.
    Provides standard DDD serialization and comparison methods.
    """
    model_config = ConfigDict(frozen=True)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize Value Object to dictionary."""
        return self.model_dump()

    def to_json(self) -> str:
        """Serialize Value Object to JSON string."""
        return self.model_dump_json()

    def equals(self, other: Any) -> bool:
        """
        Check equality with another object.
        Two Value Objects are equal if they are of the same type and hold the same values.
        """
        if not isinstance(other, self.__class__):
            return False
        return self == other

    def __str__(self) -> str:
        """Standard string representation based on internal dictionary."""
        return str(self.to_dict())
