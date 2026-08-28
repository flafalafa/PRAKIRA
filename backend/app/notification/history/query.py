"""History Query Engine."""
from typing import List, Optional
from datetime import datetime
from app.notification.history.models import NotificationHistoryRecord
from app.notification.history.status import NotificationStatus
from app.notification.history.repository import HistoryRepository

class HistoryQuery:
    @staticmethod
    def by_notification_id(notif_id: str) -> Optional[NotificationHistoryRecord]:
        return HistoryRepository.get(notif_id)
        
    @staticmethod
    def by_status(status: NotificationStatus) -> List[NotificationHistoryRecord]:
        return [r for r in HistoryRepository.get_all() if r.current_status == status]
        
    @staticmethod
    def by_prediction_id(pred_id: str) -> List[NotificationHistoryRecord]:
        return [r for r in HistoryRepository.get_all() if r.prediction_id == pred_id]
