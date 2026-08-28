"""Health check registry."""
from app.health.status import HealthStatus
from app.health.models import HealthCheckResult
from app.health.checker import HealthChecker

class HealthCheckRegistry:
    """Registry for managing and executing health checks."""
    
    def __init__(self) -> None:
        self._checkers: list[HealthChecker] = []
        
    def register(self, checker: HealthChecker) -> None:
        """Register a new health checker."""
        self._checkers.append(checker)
        
    async def run_all(self) -> list[HealthCheckResult]:
        """Execute all registered health checks asynchronously."""
        results = []
        for checker in self._checkers:
            try:
                result = await checker.check()
                results.append(result)
            except Exception as e:
                # If a checker fails unexpectedly, mark as UNHEALTHY
                results.append(
                    HealthCheckResult(
                        name=checker.__class__.__name__,
                        status=HealthStatus.UNHEALTHY,
                        details={"error": str(e)}
                    )
                )
        return results

# Global instances for separating liveness (process) vs readiness (dependencies)
readiness_registry = HealthCheckRegistry()
liveness_registry = HealthCheckRegistry()
