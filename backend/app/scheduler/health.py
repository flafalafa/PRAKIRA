"""Scheduler Health and metrics."""
from app.scheduler.registry import JobRegistry
from app.scheduler.job import JobStatus
from typing import Dict, Any

class SchedulerHealth:
    @staticmethod
    def get_metrics() -> Dict[str, Any]:
        jobs = JobRegistry.list_all()
        total = len(jobs)
        running = sum(1 for j in jobs if j.status == JobStatus.RUNNING)
        completed = sum(1 for j in jobs if j.status == JobStatus.COMPLETED)
        failed = sum(1 for j in jobs if j.status in (JobStatus.FAILED, JobStatus.TIMEOUT))
        
        return {
            "status": "AVAILABLE" if total > 0 else "UNKNOWN",
            "total_jobs": total,
            "running_jobs": running,
            "completed_jobs": completed,
            "failed_jobs": failed
        }
