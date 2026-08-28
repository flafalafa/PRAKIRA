"""Notification Builder."""
import uuid
from app.notification.context import NotificationContext
from app.notification.request import NotificationRequest, NotificationType
from app.notification.priority import NotificationPriority
from app.prediction.result import PredictionStatus
from app.core.logger import get_logger

logger = get_logger(__name__)

class NotificationBuilder:
    @staticmethod
    def _map_type(status: PredictionStatus) -> NotificationType:
        mapping = {
            PredictionStatus.SAFE: NotificationType.INFORMATION,
            PredictionStatus.WATCH: NotificationType.WATCH,
            PredictionStatus.WARNING: NotificationType.WARNING,
            PredictionStatus.DANGER: NotificationType.DANGER,
            PredictionStatus.EMERGENCY: NotificationType.EMERGENCY
        }
        return mapping.get(status, NotificationType.INFORMATION)
        
    @staticmethod
    def _map_priority(status: PredictionStatus) -> NotificationPriority:
        mapping = {
            PredictionStatus.SAFE: NotificationPriority.LOW,
            PredictionStatus.WATCH: NotificationPriority.NORMAL,
            PredictionStatus.WARNING: NotificationPriority.HIGH,
            PredictionStatus.DANGER: NotificationPriority.CRITICAL,
            PredictionStatus.EMERGENCY: NotificationPriority.EMERGENCY
        }
        return mapping.get(status, NotificationPriority.LOW)

    @classmethod
    def build(cls, context: NotificationContext) -> NotificationRequest:
        logger.debug(f"Building notification for prediction: {context.prediction.prediction_id}")
        pred = context.prediction
        
        req_type = cls._map_type(pred.prediction_status)
        req_priority = cls._map_priority(pred.prediction_status)
        
        message_template = pred.explanation
        
        return NotificationRequest(
            notification_id=str(uuid.uuid4()),
            prediction_id=pred.prediction_id,
            notification_type=req_type,
            priority=req_priority,
            severity=pred.risk_level,
            message_template=message_template,
            recommendation=pred.recommendation,
            area_metadata=context.area_metadata,
            delivery_metadata={}
        )
