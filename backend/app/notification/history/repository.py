"""History Repository (In-Memory for now)."""
from typing import Dict, List, Optional
from app.notification.history.models import NotificationHistoryRecord
from app.core.logger import get_logger

logger = get_logger(__name__)

class HistoryRepository:
    _records: Dict[str, NotificationHistoryRecord] = {}
    
    @classmethod
    def save(cls, record: NotificationHistoryRecord) -> None:
        cls._records[record.notification_id] = record
        
    @classmethod
    def get(cls, notification_id: str) -> Optional[NotificationHistoryRecord]:
        return cls._records.get(notification_id)
        
    @classmethod
    def get_all(cls) -> List[NotificationHistoryRecord]:
        return list(cls._records.values())
