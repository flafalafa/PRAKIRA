"""Weather Observation domain entity."""
import uuid
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, model_validator
from datetime import datetime, timezone, timedelta

from app.domain.value_objects.geography import Coordinate
from app.domain.value_objects.hydrology import Rainfall, RainfallIntensity
from app.domain.value_objects.weather import Temperature, Humidity, Pressure, WindSpeed, WindDirection
from app.domain.value_objects.analysis import PredictionConfidence
from app.domain.value_objects.core import TimestampUTC
from app.domain.exceptions.weather_exceptions import (
    WeatherValidationError, InvalidObservationTime, InvalidTemperature
)
from app.domain.events.weather_events import (
    DomainEvent, WeatherObservationCreated, WeatherValidated, WeatherCorrected,
    WeatherStatusChanged, HeavyRainDetected, ExtremeRainDetected, ObservationRejected
)
from app.core.logger import get_logger

logger = get_logger(__name__)

class ObservationQuality(str, Enum):
    RAW = "RAW"
    VALIDATED = "VALIDATED"
    ESTIMATED = "ESTIMATED"
    CORRECTED = "CORRECTED"

class WeatherStatus(str, Enum):
    NORMAL = "NORMAL"
    RAIN = "RAIN"
    HEAVY_RAIN = "HEAVY_RAIN"
    EXTREME_RAIN = "EXTREME_RAIN"
    STORM = "STORM"
    UNKNOWN = "UNKNOWN"

class WeatherObservation(BaseModel):
    """
    Weather Observation Domain Entity.
    Immutable, self-validating record of meteorological data.
    """
    model_config = ConfigDict(frozen=True)

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    observation_time: TimestampUTC
    area_id: str
    coordinate: Coordinate
    provider: str
    station_id: str
    
    temperature: Temperature
    humidity: Humidity
    pressure: Pressure
    rainfall: Rainfall
    rainfall_intensity: Optional[RainfallIntensity] = None
    wind_speed: WindSpeed
    wind_direction: WindDirection
    
    visibility: float # meters
    cloud_coverage: float # percentage 0-100
    weather_condition: str # Textual e.g. "Cloudy"
    weather_severity: str # Textual e.g. "Moderate"
    forecast_horizon: float = 0.0 # hours (0 for actual observations)
    
    observation_quality: ObservationQuality = ObservationQuality.RAW
    confidence_score: PredictionConfidence
    weather_status: WeatherStatus = WeatherStatus.UNKNOWN
    
    created_at: TimestampUTC = Field(default_factory=lambda: TimestampUTC(value=datetime.now(timezone.utc)))
    updated_at: TimestampUTC = Field(default_factory=lambda: TimestampUTC(value=datetime.now(timezone.utc)))
    
    _events: List[DomainEvent] = PrivateAttr(default_factory=list)

    @model_validator(mode='after')
    def validate_rules(self):
        # Allow a slight future margin (e.g. 5 mins) to account for server clock drift
        future_limit = datetime.now(timezone.utc) + timedelta(minutes=5)
        if self.observation_time.value > future_limit:
            raise InvalidObservationTime(f"Observation Time {self.observation_time.value} cannot be in the future.")
            
        if not self.area_id:
            raise WeatherValidationError("Area ID cannot be empty.")
        if not self.provider or not self.provider.strip():
            raise WeatherValidationError("Provider cannot be empty.")
        if not self.station_id or not self.station_id.strip():
            raise WeatherValidationError("Station ID cannot be empty.")
            
        # Bounds validation (-50C to +60C for realism in Indonesia bounds, though we use generous global bounds)
        if self.temperature.value < -50.0 or self.temperature.value > 60.0:
            raise InvalidTemperature(f"Temperature {self.temperature.value} is outside realistic limits.")
            
        return self

    @classmethod
    def create(cls, observation_time: TimestampUTC, area_id: str, coordinate: Coordinate, 
               provider: str, station_id: str, temperature: Temperature, humidity: Humidity, 
               pressure: Pressure, rainfall: Rainfall, wind_speed: WindSpeed, 
               wind_direction: WindDirection, visibility: float, cloud_coverage: float, 
               weather_condition: str, weather_severity: str, confidence_score: PredictionConfidence,
               rainfall_intensity: Optional[RainfallIntensity] = None, forecast_horizon: float = 0.0) -> "WeatherObservation":
        
        obs = cls(
            observation_time=observation_time,
            area_id=area_id,
            coordinate=coordinate,
            provider=provider,
            station_id=station_id,
            temperature=temperature,
            humidity=humidity,
            pressure=pressure,
            rainfall=rainfall,
            rainfall_intensity=rainfall_intensity,
            wind_speed=wind_speed,
            wind_direction=wind_direction,
            visibility=visibility,
            cloud_coverage=cloud_coverage,
            weather_condition=weather_condition,
            weather_severity=weather_severity,
            confidence_score=confidence_score,
            forecast_horizon=forecast_horizon,
            observation_quality=ObservationQuality.RAW,
            weather_status=WeatherStatus.UNKNOWN
        )
        
        obs._events.append(WeatherObservationCreated(
            observation_id=obs.id, area_id=obs.area_id, provider=obs.provider
        ))
        logger.info(f"Domain Event: Observation Created - {obs.id} (Provider: {provider})")
        
        # Self-determine weather status right at creation
        obs = obs.update_weather_status()
        return obs

    def mark_validated(self) -> "WeatherObservation":
        """Marks observation as clean after data validation processes."""
        updated = self.model_copy(update={
            "observation_quality": ObservationQuality.VALIDATED,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        updated._events.append(WeatherValidated(observation_id=self.id))
        logger.info(f"Domain Event: Observation Validated - {self.id}")
        return updated

    def mark_estimated(self) -> "WeatherObservation":
        """Marks observation as estimated (e.g. interpolated from missing data)."""
        updated = self.model_copy(update={
            "observation_quality": ObservationQuality.ESTIMATED,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        return updated

    def mark_corrected(self) -> "WeatherObservation":
        """Marks observation as corrected by a human or algorithm."""
        updated = self.model_copy(update={
            "observation_quality": ObservationQuality.CORRECTED,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        updated._events.append(WeatherCorrected(observation_id=self.id))
        logger.info(f"Domain Event: Observation Corrected - {self.id}")
        return updated

    def update_confidence(self, score: PredictionConfidence) -> "WeatherObservation":
        updated = self.model_copy(update={
            "confidence_score": score,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        return updated

    def update_weather_status(self) -> "WeatherObservation":
        """
        Derives internal weather status based primarily on rainfall limits.
        BMKG Standard approximate thresholds (per hour/day). Assuming hourly for now.
        Light/Normal: 0 - 5 mm
        Rain: 5 - 20 mm
        Heavy: 20 - 50 mm
        Extreme: > 50 mm
        """
        new_status = WeatherStatus.NORMAL
        rain = self.rainfall.value
        
        # Simple logical boundaries. Will be fine-tuned via Flood Prediction Model.
        if rain > 50.0:
            new_status = WeatherStatus.EXTREME_RAIN
        elif rain > 20.0:
            new_status = WeatherStatus.HEAVY_RAIN
        elif rain > 5.0:
            new_status = WeatherStatus.RAIN
        elif self.wind_speed.value > 60.0: # Arbitrary storm wind speed
            new_status = WeatherStatus.STORM
            
        if self.weather_status == new_status:
            return self

        updated = self.model_copy(update={
            "weather_status": new_status,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        updated._events.append(WeatherStatusChanged(
            observation_id=self.id, old_status=self.weather_status, new_status=new_status
        ))
        logger.info(f"Domain Event: Weather Status Changed ({self.weather_status} -> {new_status}) - {self.id}")
        
        # Spawn critical alerts
        if new_status == WeatherStatus.HEAVY_RAIN:
            updated._events.append(HeavyRainDetected(
                observation_id=self.id, area_id=self.area_id, rainfall=rain
            ))
            logger.warning(f"Domain Event: Heavy Rain Detected! ({rain}mm) Area: {self.area_id}")
            
        if new_status == WeatherStatus.EXTREME_RAIN:
            updated._events.append(ExtremeRainDetected(
                observation_id=self.id, area_id=self.area_id, rainfall=rain
            ))
            logger.warning(f"Domain Event: EXTREME Rain Detected! ({rain}mm) Area: {self.area_id}")
            
        return updated

    def is_heavy_rain(self) -> bool:
        return self.weather_status in (WeatherStatus.HEAVY_RAIN, WeatherStatus.EXTREME_RAIN)

    def is_extreme_rain(self) -> bool:
        return self.weather_status == WeatherStatus.EXTREME_RAIN

    def is_reliable(self) -> bool:
        # e.g., confidence score above 0.7 
        return self.confidence_score.value >= 0.7

    def can_be_used_for_prediction(self) -> bool:
        # Rule: Only VALIDATED observations may be used by the Prediction Engine.
        return self.observation_quality == ObservationQuality.VALIDATED and self.is_reliable()

    def pull_events(self) -> List[DomainEvent]:
        events = self._events.copy()
        self._events.clear()
        return events
