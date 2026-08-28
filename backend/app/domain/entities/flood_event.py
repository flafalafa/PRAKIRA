"""Flood Event domain entity."""
import uuid
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, model_validator
from datetime import datetime, timezone, timedelta

from app.domain.value_objects.geography import Coordinate
from app.domain.value_objects.hydrology import WaterLevel
from app.domain.value_objects.core import TimestampUTC
from app.domain.exceptions.flood_event_exceptions import (
    FloodEventValidationError, FloodEventStateError, InvalidEventTime, FloodEventAlreadyEnded
)
from app.domain.events.flood_event_events import (
    DomainEvent, FloodEventCreated, FloodEventStarted, FloodEventUpdated,
    FloodEventEnded, FloodEventVerified, FloodSeverityChanged, GroundTruthEstablished
)
from app.core.logger import get_logger

logger = get_logger(__name__)

class FloodSeverity(str, Enum):
    MINOR = "MINOR"
    MODERATE = "MODERATE"
    MAJOR = "MAJOR"
    SEVERE = "SEVERE"
    EXTREME = "EXTREME"

class FloodStatus(str, Enum):
    ACTIVE = "ACTIVE"
    PEAK = "PEAK"
    RECEDING = "RECEDING"
    ENDED = "ENDED"

class VerificationStatus(str, Enum):
    UNVERIFIED = "UNVERIFIED"
    COMMUNITY_VERIFIED = "COMMUNITY_VERIFIED"
    OFFICIAL_VERIFIED = "OFFICIAL_VERIFIED"

class FloodEvent(BaseModel):
    """
    Flood Event Domain Entity.
    The primary source of truth for flood history and model evaluation.
    """
    model_config = ConfigDict(frozen=True)

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    area_id: str
    river_id: Optional[str] = None
    prediction_id: Optional[str] = None
    
    event_code: str
    event_source: str
    
    event_start_time: TimestampUTC
    event_end_time: Optional[TimestampUTC] = None
    peak_time: Optional[TimestampUTC] = None
    
    flood_depth: WaterLevel
    flood_area: float 
    
    affected_population: int
    affected_roads: int
    affected_buildings: int
    
    cause: str
    severity: FloodSeverity
    status: FloodStatus
    verification_status: VerificationStatus
    
    coordinate: Coordinate
    reported_by: str
    evidence_reference: Optional[str] = None
    
    created_at: TimestampUTC = Field(default_factory=lambda: TimestampUTC(value=datetime.now(timezone.utc)))
    updated_at: TimestampUTC = Field(default_factory=lambda: TimestampUTC(value=datetime.now(timezone.utc)))
    
    _events: List[DomainEvent] = PrivateAttr(default_factory=list)

    @model_validator(mode='after')
    def validate_rules(self):
        # Time constraints
        future_limit = datetime.now(timezone.utc) + timedelta(minutes=5)
        if self.event_start_time.value > future_limit:
            raise InvalidEventTime("Event Start Time cannot be in the future.")
            
        if self.event_end_time:
            if self.event_end_time.value < self.event_start_time.value:
                raise InvalidEventTime("Event End Time cannot be earlier than Event Start Time.")
                
        if self.flood_area < 0:
            raise FloodEventValidationError("Flood Area cannot be negative.")
            
        if self.affected_population < 0 or self.affected_roads < 0 or self.affected_buildings < 0:
            raise FloodEventValidationError("Affected metrics cannot be negative.")
            
        return self

    @classmethod
    def start_event(cls, area_id: str, event_code: str, event_source: str, 
                    start_time: TimestampUTC, coordinate: Coordinate, 
                    reported_by: str, flood_depth: WaterLevel, 
                    cause: str = "UNKNOWN",
                    severity: FloodSeverity = FloodSeverity.MINOR,
                    flood_area: float = 0.0, affected_population: int = 0,
                    affected_roads: int = 0, affected_buildings: int = 0,
                    river_id: Optional[str] = None, prediction_id: Optional[str] = None,
                    evidence_reference: Optional[str] = None) -> "FloodEvent":
        
        event = cls(
            area_id=area_id,
            river_id=river_id,
            prediction_id=prediction_id,
            event_code=event_code,
            event_source=event_source,
            event_start_time=start_time,
            coordinate=coordinate,
            reported_by=reported_by,
            flood_depth=flood_depth,
            cause=cause,
            severity=severity,
            status=FloodStatus.ACTIVE,
            verification_status=VerificationStatus.UNVERIFIED,
            flood_area=flood_area,
            affected_population=affected_population,
            affected_roads=affected_roads,
            affected_buildings=affected_buildings,
            evidence_reference=evidence_reference
        )
        event._events.append(FloodEventCreated(event_id=event.id, area_id=event.area_id))
        event._events.append(FloodEventStarted(event_id=event.id))
        logger.info(f"Domain Event: Flood Event Started - {event.id} ({event_code})")
        return event

    def update_peak(self, peak_time: TimestampUTC, peak_depth: WaterLevel) -> "FloodEvent":
        if self.status == FloodStatus.ENDED:
            raise FloodEventAlreadyEnded("Cannot update peak for an ended flood event.")
            
        # Ensure peak depth is mathematically sound
        new_depth = peak_depth if peak_depth.value > self.flood_depth.value else self.flood_depth
            
        updated = self.model_copy(update={
            "peak_time": peak_time,
            "flood_depth": new_depth,
            "status": FloodStatus.PEAK,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        updated._events.append(FloodEventUpdated(event_id=self.id))
        logger.info(f"Domain Event: Flood Event Peak Updated - {self.id}")
        return updated

    def end_event(self, end_time: TimestampUTC) -> "FloodEvent":
        if self.status == FloodStatus.ENDED:
            return self
            
        updated = self.model_copy(update={
            "event_end_time": end_time,
            "status": FloodStatus.ENDED,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        updated._events.append(FloodEventEnded(event_id=self.id, end_time=end_time.value.isoformat()))
        logger.info(f"Domain Event: Flood Event Ended - {self.id}")
        return updated

    def verify_community(self) -> "FloodEvent":
        if self.verification_status == VerificationStatus.OFFICIAL_VERIFIED:
            # Official validation supersedes community validation
            return self
            
        updated = self.model_copy(update={
            "verification_status": VerificationStatus.COMMUNITY_VERIFIED,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        updated._events.append(FloodEventVerified(
            event_id=self.id, verification_status=VerificationStatus.COMMUNITY_VERIFIED.value
        ))
        logger.info(f"Domain Event: Flood Event Community Verified - {self.id}")
        return updated

    def verify_official(self) -> "FloodEvent":
        updated = self.model_copy(update={
            "verification_status": VerificationStatus.OFFICIAL_VERIFIED,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        updated._events.append(FloodEventVerified(
            event_id=self.id, verification_status=VerificationStatus.OFFICIAL_VERIFIED.value
        ))
        updated._events.append(GroundTruthEstablished(
            event_id=self.id, area_id=self.area_id
        ))
        logger.info(f"Domain Event: Flood Event Officially Verified (Ground Truth Established) - {self.id}")
        return updated

    def change_severity(self, severity: FloodSeverity) -> "FloodEvent":
        if self.status == FloodStatus.ENDED:
            raise FloodEventAlreadyEnded("Cannot change severity for an ended flood event.")
            
        if self.severity == severity:
            return self
            
        updated = self.model_copy(update={
            "severity": severity,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        updated._events.append(FloodSeverityChanged(
            event_id=self.id, old_severity=self.severity.value, new_severity=severity.value
        ))
        logger.info(f"Domain Event: Flood Event Severity Changed ({self.severity} -> {severity}) - {self.id}")
        return updated

    def update_flood_depth(self, depth: WaterLevel) -> "FloodEvent":
        if self.status == FloodStatus.ENDED:
            raise FloodEventAlreadyEnded("Cannot update depth for an ended flood event.")
            
        updated = self.model_copy(update={
            "flood_depth": depth,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        updated._events.append(FloodEventUpdated(event_id=self.id))
        return updated

    def update_affected_area(self, flood_area: float, pop: int, roads: int, buildings: int) -> "FloodEvent":
        if self.status == FloodStatus.ENDED:
            raise FloodEventAlreadyEnded("Cannot update area metrics for an ended flood event.")
            
        updated = self.model_copy(update={
            "flood_area": flood_area,
            "affected_population": pop,
            "affected_roads": roads,
            "affected_buildings": buildings,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        updated._events.append(FloodEventUpdated(event_id=self.id))
        return updated

    def is_active(self) -> bool:
        return self.status in (FloodStatus.ACTIVE, FloodStatus.PEAK, FloodStatus.RECEDING)

    def is_verified(self) -> bool:
        return self.verification_status in (VerificationStatus.COMMUNITY_VERIFIED, VerificationStatus.OFFICIAL_VERIFIED)

    def is_ground_truth(self) -> bool:
        # Rule: Only OFFICIAL_VERIFIED events become ground truth for model evaluation.
        return self.verification_status == VerificationStatus.OFFICIAL_VERIFIED

    def pull_events(self) -> List[DomainEvent]:
        events = self._events.copy()
        self._events.clear()
        return events
