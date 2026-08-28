"""Scheduler Job States."""
from enum import Enum

class JobState(str, Enum):
    CREATED = "CREATED"
    QUEUED = "QUEUED"
    WAITING = "WAITING"
    READY = "READY"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"
