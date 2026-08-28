"""Scheduler Queue Management."""
import asyncio
from typing import List, Optional
from datetime import datetime
from app.notification.scheduler.job import ScheduledNotification
from app.notification.priority import NotificationPriority
from app.core.logger import get_logger

logger = get_logger(__name__)

class MemoryPriorityQueue:
    def __init__(self):
        self._priority_map = {
            NotificationPriority.EMERGENCY: 1,
            NotificationPriority.CRITICAL: 2,
            NotificationPriority.HIGH: 3,
            NotificationPriority.NORMAL: 4,
            NotificationPriority.LOW: 5
        }
        self._queue: List[ScheduledNotification] = []
        self._lock = asyncio.Lock()
        
    async def enqueue(self, job: ScheduledNotification) -> None:
        async with self._lock:
            self._queue.append(job)
            self._queue.sort(key=lambda j: (
                self._priority_map.get(j.priority, 99),
                j.execution_time
            ))
            
    async def dequeue_ready(self, current_time: datetime) -> List[ScheduledNotification]:
        async with self._lock:
            ready_jobs = [j for j in self._queue if j.execution_time <= current_time]
            self._queue = [j for j in self._queue if j.execution_time > current_time]
            return ready_jobs
            
    async def size(self) -> int:
        async with self._lock:
            return len(self._queue)
