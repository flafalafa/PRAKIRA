"""Retry and Timeout policies."""
from pydantic import BaseModel
from typing import Optional

class RetryPolicy(BaseModel):
    retry_count: int = 3
    retry_delay_seconds: int = 2
    exponential_backoff: bool = True
    
class TimeoutPolicy(BaseModel):
    timeout_seconds: int = 30
    
class JobPolicy(BaseModel):
    retry: RetryPolicy = RetryPolicy()
    timeout: TimeoutPolicy = TimeoutPolicy()
