"""Area domain entity."""
import uuid
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, model_validator
from datetime import datetime, timezone

from app.domain.value_objects.geography import Coordinate, AreaCode
from app.domain.value_objects.core import TimestampUTC
from app.domain.exceptions.area_exceptions import AreaValidationError, AreaStateError
from app.domain.events.area_events import (
    DomainEvent, AreaCreated, AreaActivated, AreaDeactivated, 
    AreaArchived, AreaBoundaryUpdated, AreaElevationChanged
)
from app.core.logger import get_logger

logger = get_logger(__name__)

class AreaStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    MONITORING_ONLY = "MONITORING_ONLY"
    ARCHIVED = "ARCHIVED"

class Area(BaseModel):
    """
    Area Domain Entity.
    Encapsulates geographic boundaries and core business rules.
    Designed as Immutable Entity (creates new copies on state transitions).
    """
    model_config = ConfigDict(frozen=True)

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    code: AreaCode
    name: str
    province: str
    city: str
    district: str
    village: str
    postal_code: str
    center_coordinate: Coordinate
    boundary_polygon: Optional[str] = None # placeholder
    elevation: float # meters
    area_size: float # square km
    timezone: str = "Asia/Jakarta"
    status: AreaStatus = AreaStatus.INACTIVE
    created_at: TimestampUTC = Field(default_factory=lambda: TimestampUTC(value=datetime.now(timezone.utc)))
    updated_at: TimestampUTC = Field(default_factory=lambda: TimestampUTC(value=datetime.now(timezone.utc)))
    
    _events: List[DomainEvent] = PrivateAttr(default_factory=list)

    @model_validator(mode='after')
    def validate_rules(self):
        if not self.name or not self.name.strip():
            raise AreaValidationError("Area Name cannot be empty.")
        if self.elevation < 0:
            raise AreaValidationError("Elevation cannot be negative.")
        if self.area_size <= 0:
            raise AreaValidationError("Area Size must be positive.")
        return self

    @classmethod
    def create(cls, code: AreaCode, name: str, province: str, city: str, district: str, village: str, postal_code: str, center: Coordinate, elevation: float, area_size: float, tz: str = "Asia/Jakarta") -> "Area":
        """Factory method to orchestrate the creation of a new Area."""
        area = cls(
            code=code,
            name=name,
            province=province,
            city=city,
            district=district,
            village=village,
            postal_code=postal_code,
            center_coordinate=center,
            elevation=elevation,
            area_size=area_size,
            timezone=tz
        )
        area._events.append(AreaCreated(area_id=area.id, code=area.code.value))
        logger.info(f"Domain Event: Area Created - {area.id} ({name})")
        return area

    def activate(self) -> "Area":
        if self.status == AreaStatus.ARCHIVED:
            raise AreaStateError("Cannot activate an archived area.")
        
        updated = self.model_copy(update={
            "status": AreaStatus.ACTIVE,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        updated._events.append(AreaActivated(area_id=self.id))
        logger.info(f"Domain Event: Area Activated - {self.id}")
        return updated

    def deactivate(self) -> "Area":
        if self.status == AreaStatus.ARCHIVED:
            raise AreaStateError("Cannot deactivate an archived area.")
            
        updated = self.model_copy(update={
            "status": AreaStatus.INACTIVE,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        updated._events.append(AreaDeactivated(area_id=self.id))
        logger.info(f"Domain Event: Area Deactivated - {self.id}")
        return updated

    def archive(self) -> "Area":
        updated = self.model_copy(update={
            "status": AreaStatus.ARCHIVED,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        updated._events.append(AreaArchived(area_id=self.id))
        logger.info(f"Domain Event: Area Archived - {self.id}")
        return updated

    def rename(self, new_name: str) -> "Area":
        if not new_name or not new_name.strip():
            raise AreaValidationError("New Area Name cannot be empty.")
            
        updated = self.model_copy(update={
            "name": new_name,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        logger.info(f"Domain Event: Area Renamed to '{new_name}' - {self.id}")
        return updated

    def update_boundary(self, boundary: str) -> "Area":
        if self.is_archived():
            raise AreaStateError("Archived areas cannot update boundary.")
            
        updated = self.model_copy(update={
            "boundary_polygon": boundary,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        updated._events.append(AreaBoundaryUpdated(area_id=self.id))
        logger.info(f"Domain Event: Area Boundary Updated - {self.id}")
        return updated

    def update_center_coordinate(self, center: Coordinate) -> "Area":
        if self.is_archived():
            raise AreaStateError("Archived areas cannot update center coordinate.")
            
        updated = self.model_copy(update={
            "center_coordinate": center,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        logger.info(f"Domain Event: Area Center Coordinate Updated - {self.id}")
        return updated

    def update_elevation(self, elevation: float) -> "Area":
        if self.is_archived():
            raise AreaStateError("Archived areas cannot update elevation.")
        if elevation < 0:
            raise AreaValidationError("Elevation cannot be negative.")
            
        updated = self.model_copy(update={
            "elevation": elevation,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        updated._events.append(AreaElevationChanged(
            area_id=self.id, 
            new_elevation=elevation, 
            old_elevation=self.elevation
        ))
        logger.info(f"Domain Event: Area Elevation Changed ({self.elevation} -> {elevation}) - {self.id}")
        return updated

    def is_active(self) -> bool:
        return self.status == AreaStatus.ACTIVE

    def is_archived(self) -> bool:
        return self.status == AreaStatus.ARCHIVED
        
    def pull_events(self) -> List[DomainEvent]:
        """Extract and clear accumulated domain events."""
        events = self._events.copy()
        self._events.clear()
        return events
