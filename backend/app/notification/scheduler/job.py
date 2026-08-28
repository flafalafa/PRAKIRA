"""Scheduled Job Model."""
import uuid
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from app.notification.request import NotificationRequest
from app.notification.priority import NotificationPriority
from app.notification.scheduler.state import JobState

class ScheduledNotification(BaseModel):
    notification_id: str
    schedule_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    request: NotificationRequest
    execution_time: datetime
    priority: NotificationPriority
    retry_count: int = 0
    current_state: JobState = JobState.CREATED
    delay_reason: str = ""
    escalation_status: bool = False
    created_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
