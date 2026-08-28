"""Job definition models."""
from enum import Enum
from typing import Optional, Dict, Any, Callable
from datetime import datetime, timezone
from pydantic import BaseModel
from app.scheduler.policy import JobPolicy

class JobStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    TIMEOUT = "TIMEOUT"

class Job(BaseModel):
    id: str
    name: str
    target_func: str
    policy: JobPolicy = JobPolicy()
    enabled: bool = True
    interval_seconds: Optional[int] = None
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    status: JobStatus = JobStatus.PENDING
    metadata: Dict[str, Any] = {}
