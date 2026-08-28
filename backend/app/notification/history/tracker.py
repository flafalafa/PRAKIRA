"""Main Delivery Tracker."""
from app.notification.history.models import NotificationHistoryRecord
from app.notification.history.status import NotificationStatus
from app.notification.history.timeline import TimelineManager
from app.notification.history.audit import AuditManager
from app.notification.history.repository import HistoryRepository
from app.notification.request import NotificationRequest
from app.notification.scheduler.job import ScheduledNotification
from app.notification.providers.base.models import NotificationDeliveryResult, DeliveryStatus
from app.core.logger import get_logger

logger = get_logger(__name__)

class DeliveryTracker:
    @staticmethod
    def track_creation(request: NotificationRequest) -> NotificationHistoryRecord:
        logger.info(f"Tracking creation for {request.notification_id}")
        record = NotificationHistoryRecord(
            notification_id=request.notification_id,
            prediction_id=request.prediction_id,
            current_status=NotificationStatus.CREATED
        )
        TimelineManager.add_event(record, "CREATED", "NotificationFoundation")
        HistoryRepository.save(record)
        return record
        
    @staticmethod
    def track_scheduling(job: ScheduledNotification) -> None:
        record = HistoryRepository.get(job.notification_id)
        if record:
            _old = record.current_status
            record.current_status = NotificationStatus.SCHEDULED
            record.previous_status = _old
            TimelineManager.add_event(record, "SCHEDULED", "NotificationScheduler", {"schedule_id": job.schedule_id})
            AuditManager.record_state_change(record, _old, NotificationStatus.SCHEDULED)
            HistoryRepository.save(record)
            
    @staticmethod
    def track_delivery_result(result: NotificationDeliveryResult) -> None:
        record = HistoryRepository.get(result.notification_id)
        if record:
            _old = record.current_status
            
            if result.delivery_status == DeliveryStatus.SUCCESS:
                record.current_status = NotificationStatus.DELIVERED
            elif result.delivery_status == DeliveryStatus.FAILED and result.retryable:
                record.current_status = NotificationStatus.RETRYING
                record.retry_count += 1
            else:
                record.current_status = NotificationStatus.FAILED
                
            record.previous_status = _old
            record.provider_information = {
                "provider": result.provider_name,
                "provider_id": result.provider_message_id
            }
            record.failure_reason = result.failure_reason
            
            TimelineManager.add_event(record, "DELIVERY_RESULT", "PushProvider", {"status": result.delivery_status.value})
            AuditManager.record_state_change(record, _old, record.current_status, result.failure_reason)
            HistoryRepository.save(record)
