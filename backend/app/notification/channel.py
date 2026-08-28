"""Notification Channel Abstractions."""
from abc import ABC, abstractmethod
from app.notification.request import NotificationRequest
from app.notification.response import DeliveryStatus

class BaseNotificationChannel(ABC):
    @property
    @abstractmethod
    def channel_name(self) -> str:
        pass
        
    @abstractmethod
    async def send(self, request: NotificationRequest) -> DeliveryStatus:
        pass
