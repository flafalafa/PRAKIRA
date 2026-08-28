"""Notification Factory."""
from app.notification.context import NotificationContext
from app.notification.builder import NotificationBuilder
from app.notification.request import NotificationRequest

class NotificationFactory:
    @staticmethod
    def create_request(context: NotificationContext) -> NotificationRequest:
        return NotificationBuilder.build(context)
