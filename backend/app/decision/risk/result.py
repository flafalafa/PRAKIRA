"""Risk Assessment Result Data Models."""
from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime, timezone
from app.decision.explanation import DecisionExplanation

class RiskLevel(str, Enum):
    VERY_LOW = "VERY_LOW"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"
    EXTREME = "EXTREME"

class FloodRiskAssessmentResult(BaseModel):
    assessment_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    risk_score: float = 0.0
    risk_level: RiskLevel = RiskLevel.VERY_LOW
    confidence: float = 0.0
    risk_factors: Dict[str, Any] = Field(default_factory=dict)
    risk_contributions: Dict[str, float] = Field(default_factory=dict)
    triggered_rules: List[str] = Field(default_factory=list)
    recommended_actions: List[str] = Field(default_factory=list)
    explanation: DecisionExplanation = Field(default_factory=DecisionExplanation)
