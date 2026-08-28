"""Notification Channel Registry."""
from typing import Dict, List, Type, Any
from app.notification.channel import BaseNotificationChannel
from app.notification.exceptions import ChannelRegistrationFailure
from app.core.logger import get_logger

logger = get_logger(__name__)

class ChannelRegistry:
    _channels: Dict[str, Dict[str, Any]] = {}
    
    @classmethod
    def register(cls, channel_instance: BaseNotificationChannel, priority: int = 10, enabled: bool = True) -> None:
        name = channel_instance.channel_name
        if name in cls._channels:
            raise ChannelRegistrationFailure(f"Channel {name} already registered")
            
        cls._channels[name] = {
            "instance": channel_instance,
            "priority": priority,
            "enabled": enabled
        }
        logger.debug(f"Registered Notification Channel: {name}")
        
    @classmethod
    def get_enabled_channels(cls) -> List[BaseNotificationChannel]:
        active = [(k, v) for k, v in cls._channels.items() if v["enabled"]]
        sorted_active = sorted(active, key=lambda x: x[1]["priority"])
        return [v["instance"] for k, v in sorted_active]
