"""Audit Trail Manager."""
from typing import Dict, Any
from app.notification.history.models import NotificationHistoryRecord
from app.core.logger import get_logger

logger = get_logger(__name__)

class AuditManager:
    @staticmethod
    def record_state_change(record: NotificationHistoryRecord, old_state: str, new_state: str, reason: str = "") -> None:
        audit_entry = {
            "action": "STATE_CHANGE",
            "from": old_state,
            "to": new_state,
            "reason": reason,
            "timestamp": record.updated_timestamp.isoformat()
        }
        if "state_changes" not in record.audit_metadata:
            record.audit_metadata["state_changes"] = []
        record.audit_metadata["state_changes"].append(audit_entry)
        logger.debug(f"Audit: State change recorded for {record.notification_id}")
