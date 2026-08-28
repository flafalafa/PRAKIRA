"""Collector execution context."""
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

class CollectorContext:
    """Holds metadata, state, and tracking info during a pipeline run."""
    def __init__(self, provider_id: str, job_id: Optional[str] = None):
        self.provider_id = provider_id
        self.job_id = job_id or str(uuid.uuid4())
        self.start_time = datetime.utcnow()
        self.end_time: Optional[datetime] = None
        self.metrics: Dict[str, Any] = {}
        self.errors: list = []
        
    def add_metric(self, key: str, value: Any):
        self.metrics[key] = value
        
    def add_error(self, error: Exception):
        self.errors.append(error)
        
    def mark_completed(self):
        self.end_time = datetime.utcnow()
        
    def get_duration_ms(self) -> float:
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds() * 1000
        return (datetime.utcnow() - self.start_time).total_seconds() * 1000
