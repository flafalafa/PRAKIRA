"""Scheduler Registry (for storing active jobs)."""
from typing import Dict, Optional
from app.notification.scheduler.job import ScheduledNotification
from app.notification.scheduler.state import JobState
from app.core.logger import get_logger

logger = get_logger(__name__)

class JobRegistry:
    _jobs: Dict[str, ScheduledNotification] = {}
    
    @classmethod
    def register(cls, job: ScheduledNotification) -> None:
        cls._jobs[job.schedule_id] = job
        logger.debug(f"Job registered in registry: {job.schedule_id}")
        
    @classmethod
    def update_state(cls, schedule_id: str, state: JobState) -> None:
        if schedule_id in cls._jobs:
            cls._jobs[schedule_id].current_state = state
            
    @classmethod
    def get_job(cls, schedule_id: str) -> Optional[ScheduledNotification]:
        return cls._jobs.get(schedule_id)
