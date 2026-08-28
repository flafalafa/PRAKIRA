"""Rate Limiter Strategy and Abstraction."""
from abc import ABC, abstractmethod
from typing import Tuple

class RateLimiterStrategy(ABC):
    @abstractmethod
    async def is_allowed(self, key: str, limit: int, window: int) -> Tuple[bool, int, int]:
        """
        Check if the request is allowed.
        Returns a tuple of:
        (is_allowed: bool, remaining_capacity: int, retry_after: int)
        """
        pass
