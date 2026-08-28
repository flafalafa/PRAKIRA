"""FCM Message Mapper."""
from typing import Dict, Any
from app.notification.scheduler.job import ScheduledNotification

class FCMMapper:
    @staticmethod
    def map_to_payload(job: ScheduledNotification, target: str) -> Dict[str, Any]:
        req = job.request
        
        payload = {
            "token": target,
            "notification": {
                "title": f"Flood Guardian: {req.notification_type}",
                "body": req.message_template
            },
            "data": {
                "notification_id": req.notification_id,
                "prediction_id": req.prediction_id,
                "severity": req.severity,
                "recommendation": req.recommendation
            }
        }
        
        if req.priority in ["HIGH", "CRITICAL", "EMERGENCY"]:
            payload["android"] = {"priority": "high"}
        else:
            payload["android"] = {"priority": "normal"}
            
        return payload
