"""Notification Foundation Entry Point."""
from app.notification.context import NotificationContext
from app.notification.factory import NotificationFactory
from app.notification.request import NotificationRequest
from app.prediction.result import FloodPredictionResult
from app.core.logger import get_logger

logger = get_logger(__name__)

class NotificationFoundation:
    @staticmethod
    def process_prediction(prediction: FloodPredictionResult, area_metadata: dict) -> NotificationRequest:
        logger.info(f"Notification Foundation Started for prediction: {prediction.prediction_id}")
        
        context = NotificationContext(
            prediction=prediction,
            area_metadata=area_metadata
        )
        
        request = NotificationFactory.create_request(context)
        
        logger.info(f"Notification Request Generated: {request.notification_id} with Priority {request.priority}")
        return request
