"""Notification Manager (Placeholder for T-602+)."""
from app.notification.request import NotificationRequest
from app.notification.registry import ChannelRegistry
from app.core.logger import get_logger

logger = get_logger(__name__)

class NotificationManager:
    @staticmethod
    async def dispatch(request: NotificationRequest) -> None:
        """
        Placeholder for future dispatch logic.
        Currently just logs the intent.
        """
        channels = ChannelRegistry.get_enabled_channels()
        logger.info(f"Ready to dispatch notification {request.notification_id} to {len(channels)} channels.")
