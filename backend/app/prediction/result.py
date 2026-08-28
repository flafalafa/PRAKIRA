"""Prediction Result Data Models."""
from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

class PredictionStatus(str, Enum):
    SAFE = "SAFE"
    WATCH = "WATCH"
    WARNING = "WARNING"
    DANGER = "DANGER"
    EMERGENCY = "EMERGENCY"

class FloodPredictionResult(BaseModel):
    prediction_id: str
    prediction_code: str
    prediction_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    risk_score: float = 0.0
    risk_level: str = "VERY_LOW"
    confidence: float = 0.0
    estimated_arrival_time: Optional[int] = None
    estimated_flood_depth: Optional[float] = None
    estimated_duration: Optional[int] = None
    prediction_status: PredictionStatus = PredictionStatus.SAFE
    recommendation: str = "No Action Required"
    explanation: str = ""
    supporting_factors: Dict[str, Any] = Field(default_factory=dict)
    prediction_version: str = "1.0"
