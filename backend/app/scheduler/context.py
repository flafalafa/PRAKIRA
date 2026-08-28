"""Execution Context for jobs."""
from datetime import datetime, timezone
from typing import Dict, Any

class ExecutionContext:
    def __init__(self, job_id: str):
        self.job_id = job_id
        self.start_time = datetime.now(timezone.utc)
        self.end_time = None
        self.attempt = 1
        self.state: Dict[str, Any] = {}
        
    def mark_complete(self):
        self.end_time = datetime.now(timezone.utc)
        
    @property
    def duration_seconds(self) -> float:
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return (datetime.now(timezone.utc) - self.start_time).total_seconds()
