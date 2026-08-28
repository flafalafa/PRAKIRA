"""Notification Response Models."""
from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime, timezone

class DeliveryStatus(BaseModel):
    channel: str
    success: bool
    error_message: str = ""
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class NotificationResponse(BaseModel):
    notification_id: str
    overall_success: bool = False
    delivery_statuses: List[DeliveryStatus] = Field(default_factory=list)
