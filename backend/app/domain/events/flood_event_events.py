"""Flood Event domain events."""
from typing import Optional
from app.domain.events.area_events import DomainEvent

class FloodEventCreated(DomainEvent):
    event_id: str
    area_id: str

class FloodEventStarted(DomainEvent):
    event_id: str

class FloodEventUpdated(DomainEvent):
    event_id: str

class FloodEventEnded(DomainEvent):
    event_id: str
    end_time: str

class FloodEventVerified(DomainEvent):
    event_id: str
    verification_status: str

class FloodSeverityChanged(DomainEvent):
    event_id: str
    old_severity: str
    new_severity: str

class GroundTruthEstablished(DomainEvent):
    event_id: str
    area_id: str
