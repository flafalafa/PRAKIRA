"""Escalation & Deduplication Result Models."""
from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from app.notification.priority import NotificationPriority

class EngineDecision(str, Enum):
    PROCEED = "PROCEED"
    SUPPRESS = "SUPPRESS"
    REPLACE = "REPLACE"

class EscalationLevel(str, Enum):
    NO_CHANGE = "NO_CHANGE"
    UPGRADE = "UPGRADE"
    DOWNGRADE = "DOWNGRADE"
    EMERGENCY_OVERRIDE = "EMERGENCY_OVERRIDE"

class EscalationDecisionResult(BaseModel):
    decision: EngineDecision = EngineDecision.PROCEED
    escalation_level: EscalationLevel = EscalationLevel.NO_CHANGE
    duplicate_status: bool = False
    replacement_status: bool = False
    final_priority: NotificationPriority = NotificationPriority.LOW
    suppression_reason: str = ""
    triggered_policies: List[str] = Field(default_factory=list)
    explanation: str = ""
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
