"""Alert Policy Context."""
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from app.notification.request import NotificationRequest
from app.prediction.result import FloodPredictionResult

@dataclass
class AlertPolicyContext:
    notification_request: NotificationRequest
    flood_prediction: FloodPredictionResult
    prediction_metadata: Dict[str, Any] = field(default_factory=dict)
    # Abstract interface for history
    last_notification: Optional[NotificationRequest] = None 
