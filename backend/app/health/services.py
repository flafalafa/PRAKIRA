"""Placeholder health check implementations."""
from app.health.checker import HealthChecker
from app.health.models import HealthCheckResult
from app.health.status import HealthStatus

class DatabaseHealthCheck(HealthChecker):
    async def check(self) -> HealthCheckResult:
        return HealthCheckResult(name="Database", status=HealthStatus.HEALTHY, latency_ms=1.2)

class RedisHealthCheck(HealthChecker):
    async def check(self) -> HealthCheckResult:
        return HealthCheckResult(name="Redis", status=HealthStatus.HEALTHY, latency_ms=0.5)

class CollectorHealthCheck(HealthChecker):
    async def check(self) -> HealthCheckResult:
        return HealthCheckResult(name="Collector", status=HealthStatus.HEALTHY)

class SchedulerHealthCheck(HealthChecker):
    async def check(self) -> HealthCheckResult:
        return HealthCheckResult(name="Scheduler", status=HealthStatus.HEALTHY)

class DecisionEngineHealthCheck(HealthChecker):
    async def check(self) -> HealthCheckResult:
        return HealthCheckResult(name="DecisionEngine", status=HealthStatus.HEALTHY)

class NotificationHealthCheck(HealthChecker):
    async def check(self) -> HealthCheckResult:
        return HealthCheckResult(name="Notification", status=HealthStatus.HEALTHY)

class AppProcessHealthCheck(HealthChecker):
    async def check(self) -> HealthCheckResult:
        # Represents basic process liveness
        return HealthCheckResult(name="AppProcess", status=HealthStatus.HEALTHY)

def register_health_checks() -> None:
    """Register all health checks with the appropriate registry."""
    from app.health.registry import readiness_registry, liveness_registry
    
    # Liveness (is the app process running?)
    liveness_registry.register(AppProcessHealthCheck())
    
    # Readiness (can we handle external requests?)
    readiness_registry.register(DatabaseHealthCheck())
    readiness_registry.register(RedisHealthCheck())
    readiness_registry.register(CollectorHealthCheck())
    readiness_registry.register(SchedulerHealthCheck())
    readiness_registry.register(DecisionEngineHealthCheck())
    readiness_registry.register(NotificationHealthCheck())
