"""Notification Request Data Models."""
from enum import Enum
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from app.notification.priority import NotificationPriority

class NotificationType(str, Enum):
    INFORMATION = "INFORMATION"
    WATCH = "WATCH"
    WARNING = "WARNING"
    DANGER = "DANGER"
    EMERGENCY = "EMERGENCY"
    SYSTEM_NOTIFICATION = "SYSTEM_NOTIFICATION"
    MAINTENANCE = "MAINTENANCE"

class NotificationRequest(BaseModel):
    notification_id: str
    prediction_id: str
    notification_type: NotificationType
    priority: NotificationPriority
    severity: str
    message_template: str
    recommendation: str
    area_metadata: Dict[str, Any] = Field(default_factory=dict)
    delivery_metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
