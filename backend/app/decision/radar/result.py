"""Radar Analysis Result Data Models."""
from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from app.decision.explanation import DecisionExplanation

class RadarSeverity(str, Enum):
    NORMAL = "NORMAL"
    WATCH = "WATCH"
    WARNING = "WARNING"
    SEVERE = "SEVERE"

class RadarAnalysisResult(BaseModel):
    analysis_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    observation_window: str = "1h"
    storm_cells: int = 0
    movement_direction: float = 0.0
    movement_speed: float = 0.0
    estimated_arrival_time: Optional[int] = None
    coverage_area: float = 0.0
    radar_severity: RadarSeverity = RadarSeverity.NORMAL
    confidence: float = 0.0
    triggered_rules: List[str] = Field(default_factory=list)
    explanation: DecisionExplanation = Field(default_factory=DecisionExplanation)
