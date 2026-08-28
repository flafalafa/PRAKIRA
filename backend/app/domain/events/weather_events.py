"""Weather domain events."""
from app.domain.events.area_events import DomainEvent

class WeatherObservationCreated(DomainEvent):
    observation_id: str
    area_id: str
    provider: str

class WeatherValidated(DomainEvent):
    observation_id: str

class WeatherCorrected(DomainEvent):
    observation_id: str

class WeatherStatusChanged(DomainEvent):
    observation_id: str
    old_status: str
    new_status: str

class HeavyRainDetected(DomainEvent):
    observation_id: str
    area_id: str
    rainfall: float

class ExtremeRainDetected(DomainEvent):
    observation_id: str
    area_id: str
    rainfall: float

class ObservationRejected(DomainEvent):
    observation_id: str
    reason: str
