"""Base Entity for Flood Guardian."""
import json
from typing import Any
from app.persistence.base import Base
from app.entities.identity import UUIDIdentifierMixin

class BaseEntity(Base, UUIDIdentifierMixin):
    """
    Abstract BaseEntity combining the SQLAlchemy Declarative Base 
    and a standard UUID Primary Key.
    
    Every future business entity MUST inherit from this class.
    """
    __abstract__ = True
    
    def to_dict(self) -> dict[str, Any]:
        """Generic serialization to dictionary."""
        result = {}
        for c in self.__table__.columns:
            val = getattr(self, c.name)
            result[c.name] = val
        return result
        
    def to_json(self) -> str:
        """Generic serialization to JSON string."""
        return json.dumps(self.to_dict(), default=str)
        
    def __eq__(self, other: Any) -> bool:
        """Entity equality based on type and primary key identity."""
        if not isinstance(other, type(self)):
            return False
        # Do not equate entities that haven't been assigned an ID
        if not getattr(self, "id", None) or not getattr(other, "id", None):
            return False
        return self.id == other.id
        
    def __hash__(self) -> int:
        """Hash based on primary key."""
        return hash((type(self), getattr(self, "id", None)))
        
    def __repr__(self) -> str:
        """String representation."""
        return f"<{self.__class__.__name__}(id={getattr(self, 'id', None)})>"
