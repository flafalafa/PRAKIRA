"""Preference Evaluation Result."""
from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from datetime import datetime, timezone

class PreferenceDecision(str, Enum):
    ALLOW = "ALLOW"
    SUPPRESS = "SUPPRESS"

class NotificationPreferenceResult(BaseModel):
    decision: PreferenceDecision = PreferenceDecision.ALLOW
    delivery_allowed: bool = True
    selected_channels: List[str] = Field(default_factory=list)
    suppression_reason: str = ""
    quiet_hours_status: bool = False
    emergency_override_status: bool = False
    applied_preferences: List[str] = Field(default_factory=list)
    evaluation_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
