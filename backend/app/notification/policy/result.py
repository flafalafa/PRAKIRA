"""Alert Policy Result Data Models."""
from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from app.notification.priority import NotificationPriority

class PolicyDecision(str, Enum):
    SEND = "SEND"
    SUPPRESS = "SUPPRESS"
    ESCALATE = "ESCALATE"
    DEFER = "DEFER"
    CANCEL = "CANCEL"

class AlertPolicyResult(BaseModel):
    policy_decision: PolicyDecision = PolicyDecision.SEND
    delivery_decision: bool = True
    suppression_reason: str = ""
    escalation_decision: bool = False
    priority: NotificationPriority = NotificationPriority.LOW
    policy_version: str = "1.0"
    triggered_policies: List[str] = Field(default_factory=list)
    explanation: str = ""
    evaluation_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
