"""Hydrology Analysis Result Data Models."""
from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime, timezone
from app.decision.explanation import DecisionExplanation

class HydrologySeverity(str, Enum):
    NORMAL = "NORMAL"
    WATCH = "WATCH"
    WARNING = "WARNING"
    SEVERE = "SEVERE"
    CRITICAL = "CRITICAL"

class RiverStatus(str, Enum):
    NORMAL = "NORMAL"
    RISING = "RISING"
    OVERFLOW = "OVERFLOW"
    RECEDING = "RECEDING"

class HydrologyAnalysisResult(BaseModel):
    analysis_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    observation_window: str = "1h"
    current_water_level: float = 0.0
    water_level_trend: str = "STEADY"
    river_capacity_usage: float = 0.0
    flow_rate: float = 0.0
    flow_trend: str = "STEADY"
    river_status: RiverStatus = RiverStatus.NORMAL
    hydrology_severity: HydrologySeverity = HydrologySeverity.NORMAL
    confidence: float = 0.0
    triggered_rules: List[str] = Field(default_factory=list)
    explanation: DecisionExplanation = Field(default_factory=DecisionExplanation)
