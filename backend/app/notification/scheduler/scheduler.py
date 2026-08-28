"""Notification Scheduler."""
from datetime import datetime, timezone
from app.notification.scheduler.context import SchedulerContext
from app.notification.scheduler.job import ScheduledNotification
from app.notification.scheduler.state import JobState
from app.notification.scheduler.queue import MemoryPriorityQueue
from app.notification.scheduler.registry import JobRegistry
from app.notification.scheduler.policy import SchedulingPolicy
from app.notification.scheduler.dispatcher import SchedulerDispatcher
from app.notification.policy.result import PolicyDecision
from app.core.logger import get_logger

logger = get_logger(__name__)

class NotificationScheduler:
    _queue = MemoryPriorityQueue()
    _dispatcher = SchedulerDispatcher(_queue)
    
    @classmethod
    async def schedule(cls, context: SchedulerContext) -> ScheduledNotification:
        req = context.notification_request
        policy = context.policy_result
        
        logger.info(f"Scheduling notification: {req.notification_id}")
        
        if policy.policy_decision == PolicyDecision.DEFER:
            exec_time = SchedulingPolicy.calculate_execution_time(is_immediate=False, delay_minutes=15)
            delay_reason = policy.suppression_reason
            state = JobState.WAITING
        else:
            exec_time = SchedulingPolicy.calculate_execution_time(is_immediate=True)
            delay_reason = ""
            state = JobState.QUEUED
            
        job = ScheduledNotification(
            notification_id=req.notification_id,
            request=req,
            execution_time=exec_time,
            priority=req.priority,
            current_state=state,
            delay_reason=delay_reason,
            escalation_status=policy.escalation_decision
        )
        
        JobRegistry.register(job)
        await cls._queue.enqueue(job)
        
        logger.info(f"Notification scheduled. Schedule ID: {job.schedule_id}, Priority: {job.priority}")
        return job
        
    @classmethod
    async def tick(cls) -> None:
        """Called periodically to process queue."""
        await cls._dispatcher.process_ready_jobs()
