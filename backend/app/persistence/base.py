"""Declarative Base configuration."""
from typing import Any
from sqlalchemy.orm import DeclarativeBase
from app.persistence.metadata import metadata

class Base(DeclarativeBase):
    """
    Abstract base class for all SQLAlchemy declarative models.
    All future ORM models (User, Weather, Prediction) MUST inherit from this.
    """
    metadata = metadata
    
    def to_dict(self) -> dict[str, Any]:
        """Convert model instance to a dictionary representation."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
