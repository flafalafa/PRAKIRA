"""Scheduler Dispatcher."""
import asyncio
from datetime import datetime, timezone
from app.notification.scheduler.queue import MemoryPriorityQueue
from app.notification.scheduler.executor import JobExecutor
from app.notification.scheduler.state import JobState
from app.notification.scheduler.registry import JobRegistry
from app.notification.scheduler.policy import RetryPolicy
from app.core.logger import get_logger

logger = get_logger(__name__)

class SchedulerDispatcher:
    def __init__(self, queue: MemoryPriorityQueue):
        self.queue = queue
        self.retry_policy = RetryPolicy()
        
    async def process_ready_jobs(self) -> None:
        now = datetime.now(timezone.utc)
        ready_jobs = await self.queue.dequeue_ready(now)
        
        for job in ready_jobs:
            JobRegistry.update_state(job.schedule_id, JobState.READY)
            success = await JobExecutor.execute(job)
            
            if not success:
                await self._handle_retry(job)
                
    async def _handle_retry(self, job) -> None:
        try:
            delay = self.retry_policy.calculate_next_retry(job.retry_count)
            job.retry_count += 1
            job.execution_time = datetime.now(timezone.utc) + delay
            job.current_state = JobState.WAITING
            job.delay_reason = f"Retry {job.retry_count}"
            
            await self.queue.enqueue(job)
            logger.info(f"Job {job.schedule_id} scheduled for retry at {job.execution_time}")
        except ValueError:
            JobRegistry.update_state(job.schedule_id, JobState.FAILED)
            logger.error(f"Job {job.schedule_id} max retries exceeded.")
