"""Timeline Manager."""
from typing import Dict, Any
from app.notification.history.models import TimelineEvent, NotificationHistoryRecord
from app.core.logger import get_logger

logger = get_logger(__name__)

class TimelineManager:
    @staticmethod
    def add_event(record: NotificationHistoryRecord, event_type: str, source: str, metadata: Dict[str, Any] = None) -> None:
        event = TimelineEvent(
            event_type=event_type,
            source_component=source,
            metadata=metadata or {}
        )
        record.timeline_events.append(event)
        record.updated_timestamp = event.timestamp
        logger.debug(f"Added timeline event {event_type} to {record.notification_id}")
