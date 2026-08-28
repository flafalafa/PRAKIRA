"""Notification History Data Models."""
import uuid
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from app.notification.history.status import NotificationStatus

class TimelineEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    event_type: str
    source_component: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class NotificationHistoryRecord(BaseModel):
    history_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    notification_id: str
    prediction_id: str
    current_status: NotificationStatus = NotificationStatus.CREATED
    previous_status: NotificationStatus = NotificationStatus.UNKNOWN
    timeline_events: List[TimelineEvent] = Field(default_factory=list)
    retry_count: int = 0
    provider_information: Dict[str, Any] = Field(default_factory=dict)
    failure_reason: str = ""
    audit_metadata: Dict[str, Any] = Field(default_factory=dict)
    created_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
