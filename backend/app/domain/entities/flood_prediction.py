"""Flood Prediction domain entity."""
import uuid
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, model_validator
from datetime import datetime, timezone, timedelta

from app.domain.value_objects.hydrology import WaterLevel
from app.domain.value_objects.analysis import PredictionConfidence, RiskScore
from app.domain.value_objects.core import TimestampUTC, Duration
from app.domain.exceptions.prediction_exceptions import (
    PredictionValidationError, PredictionStateError, InvalidProbability, InvalidForecastWindow
)
from app.domain.events.prediction_events import (
    DomainEvent, PredictionGenerated, PredictionValidated, PredictionExpired,
    PredictionCancelled, RiskLevelChanged, CriticalPredictionDetected,
    PredictionReadyForNotification
)
from app.core.logger import get_logger

logger = get_logger(__name__)

class RiskLevel(str, Enum):
    VERY_LOW = "VERY_LOW"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"
    EXTREME = "EXTREME"

class PredictionStatus(str, Enum):
    DRAFT = "DRAFT"
    GENERATED = "GENERATED"
    VALIDATED = "VALIDATED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"

class RiskClassificationPolicy(BaseModel):
    """
    Configurable policy for Risk Level classification based on Risk Score (0-100).
    Separates the static threshold logic from the prediction entity itself.
    """
    low_threshold: float = 20.0
    medium_threshold: float = 40.0
    high_threshold: float = 60.0
    very_high_threshold: float = 80.0
    extreme_threshold: float = 95.0
    
    def classify(self, score: float) -> RiskLevel:
        if score < self.low_threshold:
            return RiskLevel.VERY_LOW
        elif score < self.medium_threshold:
            return RiskLevel.LOW
        elif score < self.high_threshold:
            return RiskLevel.MEDIUM
        elif score < self.very_high_threshold:
            return RiskLevel.HIGH
        elif score < self.extreme_threshold:
            return RiskLevel.VERY_HIGH
        else:
            return RiskLevel.EXTREME

class FloodPrediction(BaseModel):
    """
    Flood Prediction Domain Entity.
    The primary assessment record aggregating hydro/meteorological data.
    """
    model_config = ConfigDict(frozen=True)

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    prediction_code: str
    area_id: str
    river_id: Optional[str] = None
    
    prediction_time: TimestampUTC
    forecast_start: TimestampUTC
    forecast_end: TimestampUTC
    
    prediction_source: str
    prediction_method: str
    
    risk_score: RiskScore
    confidence_score: PredictionConfidence
    flood_probability: Optional[float] = None # 0.0 to 1.0
    
    estimated_flood_depth: Optional[WaterLevel] = None
    estimated_arrival_time: Optional[TimestampUTC] = None
    expected_duration: Optional[Duration] = None
    
    rainfall_reference: Optional[str] = None
    river_reference: Optional[str] = None
    weather_reference: Optional[str] = None
    
    recommended_action: str
    risk_level: RiskLevel = RiskLevel.VERY_LOW
    status: PredictionStatus = PredictionStatus.DRAFT
    
    created_at: TimestampUTC = Field(default_factory=lambda: TimestampUTC(value=datetime.now(timezone.utc)))
    updated_at: TimestampUTC = Field(default_factory=lambda: TimestampUTC(value=datetime.now(timezone.utc)))
    
    _events: List[DomainEvent] = PrivateAttr(default_factory=list)

    @model_validator(mode='after')
    def validate_rules(self):
        # Time validation
        future_limit = datetime.now(timezone.utc) + timedelta(minutes=5)
        if self.prediction_time.value > future_limit:
            raise InvalidForecastWindow("Prediction Time cannot be in the future.")
            
        if self.forecast_start.value > self.forecast_end.value:
            raise InvalidForecastWindow("Forecast Start cannot be after Forecast End.")
            
        if self.flood_probability is not None and not (0.0 <= self.flood_probability <= 1.0):
            raise InvalidProbability("Flood Probability must be between 0 and 1.")
            
        return self

    @classmethod
    def generate(cls, prediction_code: str, area_id: str, prediction_time: TimestampUTC,
                 forecast_start: TimestampUTC, forecast_end: TimestampUTC,
                 prediction_source: str, prediction_method: str, risk_score: RiskScore,
                 confidence_score: PredictionConfidence, recommended_action: str, policy: RiskClassificationPolicy,
                 flood_probability: Optional[float] = None,
                 estimated_flood_depth: Optional[WaterLevel] = None,
                 expected_duration: Optional[Duration] = None,
                 river_id: Optional[str] = None, estimated_arrival_time: Optional[TimestampUTC] = None,
                 rainfall_reference: Optional[str] = None, river_reference: Optional[str] = None,
                 weather_reference: Optional[str] = None) -> "FloodPrediction":
        
        prediction = cls(
            prediction_code=prediction_code,
            area_id=area_id,
            river_id=river_id,
            prediction_time=prediction_time,
            forecast_start=forecast_start,
            forecast_end=forecast_end,
            prediction_source=prediction_source,
            prediction_method=prediction_method,
            risk_score=risk_score,
            confidence_score=confidence_score,
            flood_probability=flood_probability,
            estimated_flood_depth=estimated_flood_depth,
            estimated_arrival_time=estimated_arrival_time,
            expected_duration=expected_duration,
            recommended_action=recommended_action,
            rainfall_reference=rainfall_reference,
            river_reference=river_reference,
            weather_reference=weather_reference,
            status=PredictionStatus.GENERATED
        )
        
        # Calculate initial risk level based on the injected policy
        prediction = prediction.calculate_risk_level(policy)
        
        prediction._events.append(PredictionGenerated(
            prediction_id=prediction.id, area_id=prediction.area_id
        ))
        logger.info(f"Domain Event: Prediction Generated - {prediction.id} ({prediction_code})")
        return prediction

    def validate(self) -> "FloodPrediction":
        if self.status in (PredictionStatus.EXPIRED, PredictionStatus.CANCELLED):
            raise PredictionStateError("Cannot validate an expired or cancelled prediction.")
            
        updated = self.model_copy(update={
            "status": PredictionStatus.VALIDATED,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        updated._events.append(PredictionValidated(prediction_id=self.id))
        logger.info(f"Domain Event: Prediction Validated - {self.id}")
        
        if updated.can_notify():
            updated._events.append(PredictionReadyForNotification(
                prediction_id=self.id, area_id=self.area_id
            ))
            logger.info(f"Domain Event: Prediction Ready For Notification - {self.id}")
            
        return updated

    def expire(self) -> "FloodPrediction":
        if self.status in (PredictionStatus.EXPIRED, PredictionStatus.CANCELLED):
            return self
            
        updated = self.model_copy(update={
            "status": PredictionStatus.EXPIRED,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        updated._events.append(PredictionExpired(prediction_id=self.id))
        logger.info(f"Domain Event: Prediction Expired - {self.id}")
        return updated

    def cancel(self) -> "FloodPrediction":
        if self.status in (PredictionStatus.EXPIRED, PredictionStatus.CANCELLED):
            return self
            
        updated = self.model_copy(update={
            "status": PredictionStatus.CANCELLED,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        updated._events.append(PredictionCancelled(prediction_id=self.id))
        logger.info(f"Domain Event: Prediction Cancelled - {self.id}")
        return updated

    def update_risk_score(self, new_score: RiskScore, policy: RiskClassificationPolicy) -> "FloodPrediction":
        if self.status in (PredictionStatus.EXPIRED, PredictionStatus.CANCELLED):
            raise PredictionStateError("Cannot update risk score for expired or cancelled prediction.")
            
        updated = self.model_copy(update={
            "risk_score": new_score,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        logger.info(f"Domain Event: Risk Score Updated ({self.risk_score.value} -> {new_score.value}) - {self.id}")
        
        return updated.calculate_risk_level(policy)

    def update_confidence(self, new_confidence: PredictionConfidence) -> "FloodPrediction":
        if self.status in (PredictionStatus.EXPIRED, PredictionStatus.CANCELLED):
            raise PredictionStateError("Cannot update confidence for expired or cancelled prediction.")
            
        updated = self.model_copy(update={
            "confidence_score": new_confidence,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        return updated

    def update_probability(self, new_probability: Optional[float]) -> "FloodPrediction":
        if self.status in (PredictionStatus.EXPIRED, PredictionStatus.CANCELLED):
            raise PredictionStateError("Cannot update probability for expired or cancelled prediction.")
        if new_probability is not None and not (0.0 <= new_probability <= 1.0):
            raise InvalidProbability("Flood Probability must be between 0 and 1.")
            
        updated = self.model_copy(update={
            "flood_probability": new_probability,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        return updated

    def calculate_risk_level(self, policy: RiskClassificationPolicy) -> "FloodPrediction":
        new_level = policy.classify(self.risk_score.value)
        
        if self.risk_level == new_level:
            return self
            
        updated = self.model_copy(update={
            "risk_level": new_level,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        updated._events.append(RiskLevelChanged(
            prediction_id=self.id, old_level=self.risk_level.value, new_level=new_level.value
        ))
        logger.info(f"Domain Event: Risk Level Changed ({self.risk_level} -> {new_level}) - {self.id}")
        
        if updated.is_critical():
            updated._events.append(CriticalPredictionDetected(
                prediction_id=self.id, area_id=self.area_id, risk_level=new_level.value
            ))
            logger.warning(f"Domain Event: CRITICAL PREDICTION DETECTED! Area: {self.area_id} Level: {new_level}")
            
        return updated

    def is_critical(self) -> bool:
        return self.risk_level in (RiskLevel.HIGH, RiskLevel.VERY_HIGH, RiskLevel.EXTREME)

    def can_notify(self) -> bool:
        # Rule: Only VALIDATED predictions can trigger notifications.
        return self.status == PredictionStatus.VALIDATED

    def is_expired(self) -> bool:
        # Prediction is expired if status is EXPIRED or current time is past forecast end
        if self.status == PredictionStatus.EXPIRED:
            return True
        if datetime.now(timezone.utc) > self.forecast_end.value:
            return True
        return False

    def pull_events(self) -> List[DomainEvent]:
        events = self._events.copy()
        self._events.clear()
        return events
