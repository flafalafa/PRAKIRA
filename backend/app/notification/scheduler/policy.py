"""Scheduler Retry and Delay Policies."""
from datetime import datetime, timedelta, timezone

class RetryPolicy:
    def __init__(self, max_retries: int = 3, base_interval_seconds: int = 60, exponential: bool = True):
        self.max_retries = max_retries
        self.base_interval = base_interval_seconds
        self.exponential = exponential
        
    def calculate_next_retry(self, current_retry: int) -> timedelta:
        if current_retry >= self.max_retries:
            raise ValueError("Max retries exceeded")
            
        multiplier = (2 ** current_retry) if self.exponential else (current_retry + 1)
        seconds = self.base_interval * multiplier
        return timedelta(seconds=seconds)

class SchedulingPolicy:
    @staticmethod
    def calculate_execution_time(is_immediate: bool, delay_minutes: int = 0) -> datetime:
        now = datetime.now(timezone.utc)
        if is_immediate:
            return now
        return now + timedelta(minutes=delay_minutes)
