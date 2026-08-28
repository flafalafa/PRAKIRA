"""Notification History Abstraction."""
from abc import ABC, abstractmethod
from typing import Optional, List
from app.notification.scheduler.job import ScheduledNotification

class NotificationHistory(ABC):
    @abstractmethod
    def get_recent_notifications(self, minutes: int = 60) -> List[ScheduledNotification]:
        pass
        
    @abstractmethod
    def get_last_notification(self) -> Optional[ScheduledNotification]:
        pass
        
    @abstractmethod
    def get_queued_notifications(self) -> List[ScheduledNotification]:
        pass
