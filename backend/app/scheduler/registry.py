"""In-memory Job Registry."""
from typing import Dict, List, Optional
from app.scheduler.job import Job
from app.core.logger import get_logger

logger = get_logger(__name__)

class JobRegistry:
    _jobs: Dict[str, Job] = {}
    
    @classmethod
    def register(cls, job: Job) -> None:
        cls._jobs[job.id] = job
        logger.debug(f"Registered job: {job.id}")
        
    @classmethod
    def unregister(cls, job_id: str) -> None:
        if job_id in cls._jobs:
            del cls._jobs[job_id]
            logger.debug(f"Unregistered job: {job_id}")
            
    @classmethod
    def get(cls, job_id: str) -> Optional[Job]:
        return cls._jobs.get(job_id)
        
    @classmethod
    def list_all(cls) -> List[Job]:
        return list(cls._jobs.values())
        
    @classmethod
    def enable(cls, job_id: str) -> None:
        if job := cls.get(job_id):
            job.enabled = True
            
    @classmethod
    def disable(cls, job_id: str) -> None:
        if job := cls.get(job_id):
            job.enabled = False
