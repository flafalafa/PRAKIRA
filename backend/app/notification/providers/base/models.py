"""Provider Models."""
import uuid
from enum import Enum
from pydantic import BaseModel, Field
from typing import Dict, Any, List
from datetime import datetime, timezone

class DeliveryStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PENDING = "PENDING"
    UNKNOWN = "UNKNOWN"

class ProviderHealthStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    DEGRADED = "DEGRADED"
    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"

class ProviderHealth(BaseModel):
    status: ProviderHealthStatus
    latency_ms: float = 0.0
    auth_status: str = ""
    config_status: str = ""
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class NotificationDeliveryResult(BaseModel):
    delivery_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    notification_id: str
    provider_name: str
    provider_message_id: str = ""
    delivery_status: DeliveryStatus
    delivery_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    retryable: bool = False
    failure_reason: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)
