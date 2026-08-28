"""Notification Lifecycle Status."""
from enum import Enum

class NotificationStatus(str, Enum):
    CREATED = "CREATED"
    QUEUED = "QUEUED"
    SCHEDULED = "SCHEDULED"
    DISPATCHED = "DISPATCHED"
    PROVIDER_ACCEPTED = "PROVIDER_ACCEPTED"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"
    UNKNOWN = "UNKNOWN"
