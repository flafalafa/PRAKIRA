"""Scheduler Context."""
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from app.notification.policy.result import AlertPolicyResult
from app.notification.request import NotificationRequest
from app.notification.scheduler.job import ScheduledNotification

@dataclass
class SchedulerContext:
    notification_request: NotificationRequest
    policy_result: AlertPolicyResult
    scheduler_metadata: Dict[str, Any] = field(default_factory=dict)
