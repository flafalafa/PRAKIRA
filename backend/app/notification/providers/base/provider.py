"""Base Provider Interface."""
from abc import ABC, abstractmethod
from typing import List
from app.notification.scheduler.job import ScheduledNotification
from app.notification.providers.base.models import NotificationDeliveryResult, ProviderHealth

class BasePushProvider(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass
        
    @abstractmethod
    async def initialize(self) -> None:
        pass
        
    @abstractmethod
    async def connect(self) -> None:
        pass
        
    @abstractmethod
    async def validate(self, notification: ScheduledNotification) -> bool:
        pass
        
    @abstractmethod
    async def send(self, notification: ScheduledNotification, target: str) -> NotificationDeliveryResult:
        pass
        
    @abstractmethod
    async def send_batch(self, notifications: List[ScheduledNotification], targets: List[str]) -> List[NotificationDeliveryResult]:
        pass
        
    @abstractmethod
    async def health(self) -> ProviderHealth:
        pass
        
    @abstractmethod
    async def disconnect(self) -> None:
        pass
