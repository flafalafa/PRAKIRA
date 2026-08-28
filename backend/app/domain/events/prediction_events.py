"""Prediction domain events."""
from app.domain.events.area_events import DomainEvent

class PredictionGenerated(DomainEvent):
    prediction_id: str
    area_id: str

class PredictionValidated(DomainEvent):
    prediction_id: str

class PredictionExpired(DomainEvent):
    prediction_id: str

class PredictionCancelled(DomainEvent):
    prediction_id: str

class RiskLevelChanged(DomainEvent):
    prediction_id: str
    old_level: str
    new_level: str

class CriticalPredictionDetected(DomainEvent):
    prediction_id: str
    area_id: str
    risk_level: str

class PredictionReadyForNotification(DomainEvent):
    prediction_id: str
    area_id: str
