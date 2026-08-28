"""Notification API Schemas."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class NotificationDeliveryStatus(BaseModel):
    notification_status: str
    provider_status: str
    delivery_timestamp: Optional[datetime] = None
    failure_state: Optional[str] = None
    retry_state: Optional[str] = None

class NotificationResponse(BaseModel):
    notification_id: str
    alert_id: str
    prediction_id: Optional[str] = None
    area_id: str
    severity: str
    title: str
    message: str
    priority: str
    current_status: str
    created_at: datetime
    updated_at: datetime
    delivery_summary: Optional[NotificationDeliveryStatus] = None

class NotificationFilterParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    status: Optional[str] = None
    severity: Optional[str] = None
    provider: Optional[str] = None
