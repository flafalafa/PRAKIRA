"""Scheduler Health."""
from pydantic import BaseModel

class SchedulerHealth(BaseModel):
    status: str
    queue_size: int
    active_jobs: int
    failed_jobs: int
