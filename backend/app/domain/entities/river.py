"""River domain entity."""
import uuid
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, model_validator
from datetime import datetime, timezone

from app.domain.value_objects.geography import Coordinate, RiverCode, Distance
from app.domain.value_objects.hydrology import WaterLevel, RiverFlowRate
from app.domain.value_objects.core import TimestampUTC
from app.domain.exceptions.river_exceptions import (
    RiverValidationError, RiverStateError, OverflowThresholdInvalid, RiverNotActive
)
from app.domain.events.river_events import (
    DomainEvent, RiverCreated, RiverActivated, RiverDeactivated, 
    RiverWaterLevelUpdated, RiverFlowRateUpdated, RiverStatusChanged, 
    RiverOverflowDetected, RiverMonitoringPriorityChanged
)
from app.core.logger import get_logger

logger = get_logger(__name__)

class RiverStatus(str, Enum):
    NORMAL = "NORMAL"
    WATCH = "WATCH"
    ALERT = "ALERT"
    CRITICAL = "CRITICAL"
    INACTIVE = "INACTIVE"

class RiverType(str, Enum):
    NATURAL = "NATURAL"
    CANAL = "CANAL"
    DRAINAGE = "DRAINAGE"

class MonitoringPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class River(BaseModel):
    """
    River Domain Entity.
    Immutable, fully self-validating hydrological object.
    It encapsulates the state machine for flood monitoring (Water Level -> Status).
    """
    model_config = ConfigDict(frozen=True)

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    code: RiverCode
    name: str
    area_id: str
    river_type: RiverType = RiverType.NATURAL
    river_category: str 
    
    length: Distance
    width: Distance
    depth: Distance
    
    normal_water_level: WaterLevel
    current_water_level: Optional[WaterLevel] = None
    danger_water_level: WaterLevel
    overflow_water_level: WaterLevel
    
    flow_direction: str 
    flow_rate: Optional[RiverFlowRate] = None
    catchment_area: float # km2
    river_slope: float 
    
    source_coordinate: Coordinate
    mouth_coordinate: Coordinate
    
    monitoring_priority: MonitoringPriority = MonitoringPriority.MEDIUM
    status: RiverStatus = RiverStatus.INACTIVE
    
    created_at: TimestampUTC = Field(default_factory=lambda: TimestampUTC(value=datetime.now(timezone.utc)))
    updated_at: TimestampUTC = Field(default_factory=lambda: TimestampUTC(value=datetime.now(timezone.utc)))
    
    _events: List[DomainEvent] = PrivateAttr(default_factory=list)

    @model_validator(mode='after')
    def validate_rules(self):
        if not self.name or not self.name.strip():
            raise RiverValidationError("River Name cannot be empty.")
        if not self.area_id:
            raise RiverValidationError("River must belong to exactly one Area.")
            
        # Water level thresholds structural validation
        if self.danger_water_level.value <= self.normal_water_level.value:
            raise OverflowThresholdInvalid("Danger Water Level must be greater than Normal Water Level.")
        if self.overflow_water_level.value <= self.danger_water_level.value:
            raise OverflowThresholdInvalid("Overflow Water Level must be greater than Danger Water Level.")
            
        return self

    @classmethod
    def create(cls, code: RiverCode, name: str, area_id: str, river_type: RiverType, river_category: str,
               length: Distance, width: Distance, depth: Distance, 
               normal_water_level: WaterLevel, danger_water_level: WaterLevel, overflow_water_level: WaterLevel,
               flow_direction: str, catchment_area: float, river_slope: float,
               source: Coordinate, mouth: Coordinate, priority: MonitoringPriority = MonitoringPriority.MEDIUM) -> "River":
        
        river = cls(
            code=code,
            name=name,
            area_id=area_id,
            river_type=river_type,
            river_category=river_category,
            length=length,
            width=width,
            depth=depth,
            normal_water_level=normal_water_level,
            danger_water_level=danger_water_level,
            overflow_water_level=overflow_water_level,
            flow_direction=flow_direction,
            catchment_area=catchment_area,
            river_slope=river_slope,
            source_coordinate=source,
            mouth_coordinate=mouth,
            monitoring_priority=priority,
            status=RiverStatus.INACTIVE
        )
        river._events.append(RiverCreated(river_id=river.id, code=river.code.value))
        logger.info(f"Domain Event: River Created - {river.id} ({name})")
        return river

    def activate(self) -> "River":
        if self.status != RiverStatus.INACTIVE:
            raise RiverStateError("Only inactive rivers can be activated.")
        
        updated = self.model_copy(update={
            "status": RiverStatus.NORMAL,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        updated._events.append(RiverActivated(river_id=self.id))
        logger.info(f"Domain Event: River Activated - {self.id}")
        return updated

    def deactivate(self) -> "River":
        updated = self.model_copy(update={
            "status": RiverStatus.INACTIVE,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        updated._events.append(RiverDeactivated(river_id=self.id))
        logger.info(f"Domain Event: River Deactivated - {self.id}")
        return updated

    def rename(self, new_name: str) -> "River":
        if not new_name or not new_name.strip():
            raise RiverValidationError("New River Name cannot be empty.")
            
        updated = self.model_copy(update={
            "name": new_name,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        logger.info(f"Domain Event: River Renamed to '{new_name}' - {self.id}")
        return updated

    def update_water_level(self, new_level: WaterLevel) -> "River":
        if self.status == RiverStatus.INACTIVE:
            raise RiverNotActive("Cannot update water level on an INACTIVE river.")
            
        old_val = self.current_water_level.value if self.current_water_level else None
        
        # Internal State Machine (Status inference based on Water Level)
        new_status = self.status
        if new_level.value >= self.overflow_water_level.value:
            new_status = RiverStatus.CRITICAL
        elif new_level.value >= self.danger_water_level.value:
            new_status = RiverStatus.ALERT
        elif new_level.value > self.normal_water_level.value:
            new_status = RiverStatus.WATCH
        else:
            new_status = RiverStatus.NORMAL
            
        updated = self.model_copy(update={
            "current_water_level": new_level,
            "status": new_status,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        
        updated._events.append(RiverWaterLevelUpdated(
            river_id=self.id, new_level=new_level.value, old_level=old_val
        ))
        logger.info(f"Domain Event: Water Level Updated ({old_val} -> {new_level.value}) - {self.id}")
        
        if new_status != self.status:
            updated._events.append(RiverStatusChanged(
                river_id=self.id, old_status=self.status, new_status=new_status
            ))
            logger.info(f"Domain Event: River Status Escalation ({self.status} -> {new_status}) - {self.id}")
            
        if new_status == RiverStatus.CRITICAL and (self.status != RiverStatus.CRITICAL):
            updated._events.append(RiverOverflowDetected(
                river_id=self.id, current_level=new_level.value, overflow_threshold=self.overflow_water_level.value
            ))
            logger.warning(f"Domain Event: River Overflow Detected! Level: {new_level.value} >= Threshold: {self.overflow_water_level.value} - {self.id}")
            
        return updated

    def update_flow_rate(self, new_rate: RiverFlowRate) -> "River":
        if self.status == RiverStatus.INACTIVE:
            raise RiverNotActive("Cannot update flow rate on an INACTIVE river.")
            
        old_val = self.flow_rate.value if self.flow_rate else None
        
        updated = self.model_copy(update={
            "flow_rate": new_rate,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        updated._events.append(RiverFlowRateUpdated(
            river_id=self.id, new_rate=new_rate.value, old_rate=old_val
        ))
        logger.info(f"Domain Event: Flow Rate Updated ({old_val} -> {new_rate.value}) - {self.id}")
        return updated

    def update_monitoring_priority(self, priority: MonitoringPriority) -> "River":
        if self.monitoring_priority == priority:
            return self
            
        updated = self.model_copy(update={
            "monitoring_priority": priority,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        updated._events.append(RiverMonitoringPriorityChanged(
            river_id=self.id, new_priority=priority, old_priority=self.monitoring_priority
        ))
        logger.info(f"Domain Event: Monitoring Priority Changed ({self.monitoring_priority} -> {priority}) - {self.id}")
        return updated

    def change_status(self, status: RiverStatus) -> "River":
        """Manual status override (e.g. by Admin or Decision Engine fallback)."""
        if self.status == status:
            return self
            
        updated = self.model_copy(update={
            "status": status,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        updated._events.append(RiverStatusChanged(
            river_id=self.id, old_status=self.status, new_status=status
        ))
        logger.info(f"Domain Event: River Status Manually Changed ({self.status} -> {status}) - {self.id}")
        return updated

    def is_overflow(self) -> bool:
        if not self.current_water_level:
            return False
        return self.current_water_level.value >= self.overflow_water_level.value

    def is_danger(self) -> bool:
        if not self.current_water_level:
            return False
        return self.current_water_level.value >= self.danger_water_level.value

    def is_normal(self) -> bool:
        if not self.current_water_level:
            return True
        return self.current_water_level.value <= self.normal_water_level.value

    def calculate_remaining_capacity(self) -> float:
        """Returns remaining height in meters/cm before overflow."""
        current = self.current_water_level.value if self.current_water_level else self.normal_water_level.value
        remaining = self.overflow_water_level.value - current
        return max(0.0, remaining)
        
    def pull_events(self) -> List[DomainEvent]:
        events = self._events.copy()
        self._events.clear()
        return events
