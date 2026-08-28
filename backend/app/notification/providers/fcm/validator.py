"""FCM Payload Validator."""
from app.notification.scheduler.job import ScheduledNotification
from app.notification.providers.base.exceptions import PayloadTooLarge, InvalidDeviceToken

class FCMValidator:
    MAX_PAYLOAD_BYTES = 4096
    
    @staticmethod
    def validate_token(token: str) -> bool:
        if not token or len(token) < 10:
            raise InvalidDeviceToken("Token is empty or invalid")
        return True
        
    @staticmethod
    def validate_payload(payload: dict) -> bool:
        size = len(str(payload).encode('utf-8'))
        if size > FCMValidator.MAX_PAYLOAD_BYTES:
            raise PayloadTooLarge(f"Payload size {size} exceeds {FCMValidator.MAX_PAYLOAD_BYTES} bytes")
        return True
