"""Job Executor."""
from app.notification.scheduler.job import ScheduledNotification
from app.notification.scheduler.state import JobState
from app.notification.scheduler.registry import JobRegistry
from app.core.logger import get_logger

logger = get_logger(__name__)

class JobExecutor:
    @staticmethod
    async def execute(job: ScheduledNotification) -> bool:
        """
        Placeholder for executing the job via Notification Manager.
        """
        logger.info(f"Executing job: {job.schedule_id} for notification {job.notification_id}")
        JobRegistry.update_state(job.schedule_id, JobState.RUNNING)
        
        # Simulate dispatch success
        success = True 
        
        if success:
            JobRegistry.update_state(job.schedule_id, JobState.COMPLETED)
            logger.info(f"Job {job.schedule_id} completed successfully")
        else:
            JobRegistry.update_state(job.schedule_id, JobState.FAILED)
            logger.error(f"Job {job.schedule_id} failed")
            
        return success
