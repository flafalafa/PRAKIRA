"""River domain events."""
from typing import Optional
from app.domain.events.area_events import DomainEvent

class RiverCreated(DomainEvent):
    river_id: str
    code: str

class RiverActivated(DomainEvent):
    river_id: str

class RiverDeactivated(DomainEvent):
    river_id: str

class RiverWaterLevelUpdated(DomainEvent):
    river_id: str
    new_level: float
    old_level: Optional[float]

class RiverFlowRateUpdated(DomainEvent):
    river_id: str
    new_rate: float
    old_rate: Optional[float]

class RiverStatusChanged(DomainEvent):
    river_id: str
    old_status: str
    new_status: str

class RiverOverflowDetected(DomainEvent):
    river_id: str
    current_level: float
    overflow_threshold: float

class RiverMonitoringPriorityChanged(DomainEvent):
    river_id: str
    new_priority: str
    old_priority: str
