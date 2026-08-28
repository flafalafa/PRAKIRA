"""Weather Analysis Result Data Models."""
from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime, timezone
from app.decision.explanation import DecisionExplanation

class WeatherSeverity(str, Enum):
    NORMAL = "NORMAL"
    WATCH = "WATCH"
    WARNING = "WARNING"
    SEVERE = "SEVERE"

class WeatherAnalysisResult(BaseModel):
    analysis_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    observation_window: str = "1h"
    rainfall_summary: str = ""
    rainfall_trend: str = "STEADY"
    rainfall_intensity: float = 0.0
    weather_severity: WeatherSeverity = WeatherSeverity.NORMAL
    storm_indicator: bool = False
    confidence: float = 0.0
    triggered_rules: List[str] = Field(default_factory=list)
    explanation: DecisionExplanation = Field(default_factory=DecisionExplanation)
