"""Escalation Context."""
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from app.notification.scheduler.job import ScheduledNotification
from app.notification.policy.result import AlertPolicyResult
from app.notification.escalation.history import NotificationHistory

@dataclass
class EscalationContext:
    current_job: ScheduledNotification
    policy_result: AlertPolicyResult
    history: NotificationHistory
    prediction_metadata: Dict[str, Any] = field(default_factory=dict)
