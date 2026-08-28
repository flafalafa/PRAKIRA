"""FCM Provider Implementation."""
from typing import List
from app.notification.providers.base.provider import BasePushProvider
from app.notification.providers.base.models import NotificationDeliveryResult, DeliveryStatus, ProviderHealth
from app.notification.scheduler.job import ScheduledNotification
from app.notification.providers.fcm.client import FCMClient
from app.notification.providers.fcm.mapper import FCMMapper
from app.notification.providers.fcm.validator import FCMValidator
from app.notification.providers.fcm.health import FCMHealthChecker
from app.core.logger import get_logger

logger = get_logger(__name__)

class FCMProvider(BasePushProvider):
    def __init__(self):
        self._client = FCMClient()
        self._name = "FCM"
        
    @property
    def name(self) -> str:
        return self._name
        
    async def initialize(self) -> None:
        logger.info(f"Initializing {self.name} provider")
        
    async def connect(self) -> None:
        logger.info(f"Connecting to {self.name}")
        
    async def validate(self, notification: ScheduledNotification) -> bool:
        return True
        
    async def send(self, notification: ScheduledNotification, target: str) -> NotificationDeliveryResult:
        logger.info(f"FCM sending notification {notification.notification_id} to {target}")
        
        try:
            FCMValidator.validate_token(target)
            payload = FCMMapper.map_to_payload(notification, target)
            FCMValidator.validate_payload(payload)
            
            message_id = await self._client.send(payload)
            
            return NotificationDeliveryResult(
                notification_id=notification.notification_id,
                provider_name=self.name,
                provider_message_id=message_id,
                delivery_status=DeliveryStatus.SUCCESS,
                metadata={"target": target}
            )
        except Exception as e:
            logger.error(f"FCM send failed: {str(e)}")
            return NotificationDeliveryResult(
                notification_id=notification.notification_id,
                provider_name=self.name,
                delivery_status=DeliveryStatus.FAILED,
                retryable=True,
                failure_reason=str(e),
                metadata={"target": target}
            )
            
    async def send_batch(self, notifications: List[ScheduledNotification], targets: List[str]) -> List[NotificationDeliveryResult]:
        results = []
        for notif, target in zip(notifications, targets):
            res = await self.send(notif, target)
            results.append(res)
        return results
        
    async def health(self) -> ProviderHealth:
        return await FCMHealthChecker.check()
        
    async def disconnect(self) -> None:
        logger.info(f"Disconnecting {self.name}")
