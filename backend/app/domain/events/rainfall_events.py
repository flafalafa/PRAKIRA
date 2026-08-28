"""Rainfall domain events."""
from typing import Optional
from app.domain.events.area_events import DomainEvent

class RainfallRecorded(DomainEvent):
    rainfall_id: str
    area_id: str
    amount: float

class RainfallValidated(DomainEvent):
    rainfall_id: str

class RainfallCorrected(DomainEvent):
    rainfall_id: str

class RainfallClassified(DomainEvent):
    rainfall_id: str
    category: str

class HeavyRainDetected(DomainEvent):
    rainfall_id: str
    area_id: str
    amount: float

class ExtremeRainDetected(DomainEvent):
    rainfall_id: str
    area_id: str
    amount: float

class RainfallRejected(DomainEvent):
    rainfall_id: str
    reason: str
