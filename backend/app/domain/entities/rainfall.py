"""Rainfall domain entity."""
import uuid
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, model_validator
from datetime import datetime, timezone, timedelta

from app.domain.value_objects.geography import Coordinate
from app.domain.value_objects.hydrology import Rainfall as RainfallVO, RainfallIntensity
from app.domain.value_objects.analysis import PredictionConfidence
from app.domain.value_objects.core import TimestampUTC, Duration
from app.domain.exceptions.rainfall_exceptions import (
    RainfallValidationError, InvalidObservationTime, RainfallNotValidated
)
from app.domain.events.rainfall_events import (
    DomainEvent, RainfallRecorded, RainfallValidated, RainfallCorrected,
    RainfallClassified, HeavyRainDetected, ExtremeRainDetected, RainfallRejected
)
from app.core.logger import get_logger

logger = get_logger(__name__)

class RainfallCategory(str, Enum):
    NO_RAIN = "NO_RAIN"
    LIGHT = "LIGHT"
    MODERATE = "MODERATE"
    HEAVY = "HEAVY"
    VERY_HEAVY = "VERY_HEAVY"
    EXTREME = "EXTREME"
    UNKNOWN = "UNKNOWN"

class QualityStatus(str, Enum):
    RAW = "RAW"
    VALIDATED = "VALIDATED"
    ESTIMATED = "ESTIMATED"
    CORRECTED = "CORRECTED"

class MeasurementMethod(str, Enum):
    RADAR = "RADAR"
    SATELLITE = "SATELLITE"
    RAIN_GAUGE = "RAIN_GAUGE"
    INTERPOLATED = "INTERPOLATED"

class RainfallClassificationPolicy(BaseModel):
    """
    Configurable policy for rainfall classification.
    Allows external configuration (e.g. BMKG standards vs WHO standards) 
    without hardcoding rules into the Entity.
    Default follows typical BMKG daily thresholds.
    """
    light_threshold: float = 0.5     # > 0.5 mm
    moderate_threshold: float = 20.0 # > 20 mm
    heavy_threshold: float = 50.0    # > 50 mm
    very_heavy_threshold: float = 100.0 # > 100 mm
    extreme_threshold: float = 150.0    # > 150 mm
    
    def classify(self, amount: float) -> RainfallCategory:
        if amount < self.light_threshold:
            return RainfallCategory.NO_RAIN
        elif amount < self.moderate_threshold:
            return RainfallCategory.LIGHT
        elif amount < self.heavy_threshold:
            return RainfallCategory.MODERATE
        elif amount < self.very_heavy_threshold:
            return RainfallCategory.HEAVY
        elif amount < self.extreme_threshold:
            return RainfallCategory.VERY_HEAVY
        else:
            return RainfallCategory.EXTREME


class RainfallEntity(BaseModel):
    """
    Rainfall Domain Entity.
    The authoritative hydrometeorological source for flood prediction.
    """
    model_config = ConfigDict(frozen=True)

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    area_id: str
    river_id: Optional[str] = None
    observation_time: TimestampUTC
    accumulation_period: Duration
    measurement_source: str
    
    rainfall_amount: RainfallVO
    rainfall_intensity: Optional[RainfallIntensity] = None
    rainfall_category: RainfallCategory = RainfallCategory.UNKNOWN
    
    forecast_flag: bool = False
    confidence_score: PredictionConfidence
    quality_status: QualityStatus = QualityStatus.RAW
    measurement_method: MeasurementMethod
    coordinate: Optional[Coordinate] = None
    
    created_at: TimestampUTC = Field(default_factory=lambda: TimestampUTC(value=datetime.now(timezone.utc)))
    updated_at: TimestampUTC = Field(default_factory=lambda: TimestampUTC(value=datetime.now(timezone.utc)))
    
    _events: List[DomainEvent] = PrivateAttr(default_factory=list)

    @model_validator(mode='after')
    def validate_rules(self):
        # Time validation
        future_limit = datetime.now(timezone.utc) + timedelta(minutes=5)
        if self.observation_time.value > future_limit:
            raise InvalidObservationTime("Observation Time cannot be in the future.")
            
        if not self.area_id:
            raise RainfallValidationError("Area ID cannot be empty.")
            
        return self

    @classmethod
    def create(cls, area_id: str, observation_time: TimestampUTC, accumulation_period: Duration,
               measurement_source: str, rainfall_amount: RainfallVO, confidence_score: PredictionConfidence,
               measurement_method: MeasurementMethod, river_id: Optional[str] = None, 
               rainfall_intensity: Optional[RainfallIntensity] = None, forecast_flag: bool = False,
               coordinate: Optional[Coordinate] = None) -> "RainfallEntity":
               
        entity = cls(
            area_id=area_id,
            river_id=river_id,
            observation_time=observation_time,
            accumulation_period=accumulation_period,
            measurement_source=measurement_source,
            rainfall_amount=rainfall_amount,
            rainfall_intensity=rainfall_intensity,
            forecast_flag=forecast_flag,
            confidence_score=confidence_score,
            measurement_method=measurement_method,
            coordinate=coordinate
        )
        
        entity._events.append(RainfallRecorded(
            rainfall_id=entity.id, area_id=entity.area_id, amount=entity.rainfall_amount.value
        ))
        logger.info(f"Domain Event: Rainfall Recorded - {entity.id} ({entity.rainfall_amount.value}mm)")
        return entity

    def classify(self, policy: RainfallClassificationPolicy) -> "RainfallEntity":
        """Classify rainfall based on an injected domain policy."""
        new_category = policy.classify(self.rainfall_amount.value)
        
        if self.rainfall_category == new_category:
            return self
            
        updated = self.model_copy(update={
            "rainfall_category": new_category,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        updated._events.append(RainfallClassified(
            rainfall_id=self.id, category=new_category.value
        ))
        logger.info(f"Domain Event: Rainfall Classified ({new_category}) - {self.id}")
        
        if updated.is_extreme_rain():
            updated._events.append(ExtremeRainDetected(
                rainfall_id=self.id, area_id=self.area_id, amount=self.rainfall_amount.value
            ))
            logger.warning(f"Domain Event: Extreme Rain Detected! ({self.rainfall_amount.value}mm) Area: {self.area_id}")
        elif updated.is_heavy_rain():
            updated._events.append(HeavyRainDetected(
                rainfall_id=self.id, area_id=self.area_id, amount=self.rainfall_amount.value
            ))
            logger.warning(f"Domain Event: Heavy Rain Detected! ({self.rainfall_amount.value}mm) Area: {self.area_id}")
            
        return updated

    def mark_validated(self) -> "RainfallEntity":
        updated = self.model_copy(update={
            "quality_status": QualityStatus.VALIDATED,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        updated._events.append(RainfallValidated(rainfall_id=self.id))
        logger.info(f"Domain Event: Rainfall Validated - {self.id}")
        return updated

    def mark_estimated(self) -> "RainfallEntity":
        updated = self.model_copy(update={
            "quality_status": QualityStatus.ESTIMATED,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        return updated

    def mark_corrected(self) -> "RainfallEntity":
        updated = self.model_copy(update={
            "quality_status": QualityStatus.CORRECTED,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        updated._events.append(RainfallCorrected(rainfall_id=self.id))
        logger.info(f"Domain Event: Rainfall Corrected - {self.id}")
        return updated

    def update_confidence(self, score: PredictionConfidence) -> "RainfallEntity":
        updated = self.model_copy(update={
            "confidence_score": score,
            "updated_at": TimestampUTC(value=datetime.now(timezone.utc))
        })
        updated._events = self._events.copy()
        return updated

    def is_heavy_rain(self) -> bool:
        return self.rainfall_category in (RainfallCategory.HEAVY, RainfallCategory.VERY_HEAVY, RainfallCategory.EXTREME)

    def is_extreme_rain(self) -> bool:
        return self.rainfall_category == RainfallCategory.EXTREME

    def can_trigger_flood_analysis(self) -> bool:
        # Business Rule: Only VALIDATED rainfall can be consumed by the Decision Engine.
        if self.quality_status != QualityStatus.VALIDATED:
            return False
        # Additionally, light rain probably shouldn't trigger expensive ML analysis
        if self.rainfall_category in (RainfallCategory.NO_RAIN, RainfallCategory.LIGHT, RainfallCategory.UNKNOWN):
            return False
        return True

    def pull_events(self) -> List[DomainEvent]:
        events = self._events.copy()
        self._events.clear()
        return events
