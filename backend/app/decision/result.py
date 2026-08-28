"""Decision Result Data Models."""
from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime, timezone
from app.decision.explanation import DecisionExplanation
from app.decision.state import DecisionStatus

class RiskLevel(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class DecisionResult(BaseModel):
    decision_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: DecisionStatus
    risk_score: float = 0.0
    risk_level: RiskLevel = RiskLevel.LOW
    confidence: float = 0.0
    triggered_rules: List[str] = Field(default_factory=list)
    supporting_evidence: Dict[str, Any] = Field(default_factory=dict)
    explanation: DecisionExplanation = Field(default_factory=DecisionExplanation)
