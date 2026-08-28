"""History Metrics Calculator."""
from typing import Dict, Any
from app.notification.history.repository import HistoryRepository
from app.notification.history.status import NotificationStatus

class HistoryMetrics:
    @staticmethod
    def calculate_metrics() -> Dict[str, Any]:
        records = HistoryRepository.get_all()
        total = len(records)
        if total == 0:
            return {"total": 0}
            
        delivered = sum(1 for r in records if r.current_status == NotificationStatus.DELIVERED)
        failed = sum(1 for r in records if r.current_status == NotificationStatus.FAILED)
        expired = sum(1 for r in records if r.current_status == NotificationStatus.EXPIRED)
        
        return {
            "total_notifications": total,
            "delivery_success_rate": (delivered / total) * 100,
            "failure_rate": (failed / total) * 100,
            "expired_rate": (expired / total) * 100
        }
