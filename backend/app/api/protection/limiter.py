"""Token Bucket In-Memory Implementation."""
from app.api.protection.strategy import RateLimiterStrategy
from typing import Tuple, Dict
import time
from threading import Lock

class Bucket:
    def __init__(self, capacity: int, window: int):
        self.capacity = capacity
        self.window = window
        self.tokens = capacity
        self.last_refill = time.time()
        self.lock = Lock()
        
    def consume(self) -> Tuple[bool, int, int]:
        with self.lock:
            now = time.time()
            # Refill
            elapsed = now - self.last_refill
            refill_amount = int(elapsed * (self.capacity / self.window))
            if refill_amount > 0:
                self.tokens = min(self.capacity, self.tokens + refill_amount)
                self.last_refill = now
                
            if self.tokens >= 1:
                self.tokens -= 1
                return True, self.tokens, 0
                
            # If rejected, calculate retry_after
            retry_after = int(self.window / self.capacity)
            return False, 0, retry_after

class InMemoryTokenBucketLimiter(RateLimiterStrategy):
    """
    In-memory Token Bucket rate limiter.
    Supports bursts natively. Chosen over sliding window for simpler memory management
    and better burst tolerance which is typical for APIs experiencing sudden spikes.
    """
    def __init__(self):
        self.buckets: Dict[str, Bucket] = {}
        self.global_lock = Lock()
        
    async def is_allowed(self, key: str, limit: int, window: int) -> Tuple[bool, int, int]:
        with self.global_lock:
            if key not in self.buckets:
                self.buckets[key] = Bucket(capacity=limit, window=window)
            bucket = self.buckets[key]
            
        return bucket.consume()
