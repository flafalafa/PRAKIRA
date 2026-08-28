"""Base health checker interface."""
from abc import ABC, abstractmethod
from app.health.models import HealthCheckResult

class HealthChecker(ABC):
    """Abstract base class for all health checks."""
    
    @abstractmethod
    async def check(self) -> HealthCheckResult:
        """Execute the health check and return its result."""
        pass
