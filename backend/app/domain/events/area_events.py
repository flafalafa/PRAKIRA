"""Area domain events."""
from pydantic import BaseModel
from typing import Optional

class DomainEvent(BaseModel):
    """Base Domain Event."""
    pass

class AreaCreated(DomainEvent):
    area_id: str
    code: str

class AreaActivated(DomainEvent):
    area_id: str

class AreaDeactivated(DomainEvent):
    area_id: str

class AreaArchived(DomainEvent):
    area_id: str

class AreaBoundaryUpdated(DomainEvent):
    area_id: str
    # Placeholder for geometry boundary delta

class AreaElevationChanged(DomainEvent):
    area_id: str
    new_elevation: float
    old_elevation: Optional[float]
