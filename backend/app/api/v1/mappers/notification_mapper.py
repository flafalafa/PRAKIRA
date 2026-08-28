"""Notification Mapper."""
from typing import Any
from app.api.v1.schemas.notification import NotificationResponse, NotificationDeliveryStatus

class NotificationMapper:
    @staticmethod
    def to_response(notification: Any) -> NotificationResponse:
        delivery_status = None
        if hasattr(notification, "delivery"):
            delivery = notification.delivery
            delivery_status = NotificationDeliveryStatus(
                notification_status=getattr(delivery, "status", "UNKNOWN"),
                provider_status=getattr(delivery, "provider_status", "UNKNOWN"),
                delivery_timestamp=getattr(delivery, "timestamp", None),
                failure_state=getattr(delivery, "failure_reason", None),
                retry_state=getattr(delivery, "retry_state", None)
            )
            
        return NotificationResponse(
            notification_id=getattr(notification, "id", "UNKNOWN"),
            alert_id=getattr(notification, "alert_id", "UNKNOWN"),
            prediction_id=getattr(notification, "prediction_id", None),
            area_id=getattr(notification, "area_id", "UNKNOWN"),
            severity=getattr(notification, "severity", "UNKNOWN"),
            title=getattr(notification, "title", ""),
            message=getattr(notification, "message", ""),
            priority=getattr(notification, "priority", "UNKNOWN"),
            current_status=getattr(notification, "status", "UNKNOWN"),
            created_at=getattr(notification, "created_at", None),
            updated_at=getattr(notification, "updated_at", None),
            delivery_summary=delivery_status
        )
