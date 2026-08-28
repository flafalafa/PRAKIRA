"""Database health checker implementation."""
import time
import asyncio
from sqlalchemy import text
from app.health.checker import HealthChecker
from app.health.models import HealthCheckResult
from app.database.status import DatabaseHealthStatus
from app.database.diagnostics import get_pool_metrics, is_metadata_loaded, is_session_factory_ready
from app.persistence.session import get_session_factory
from app.config.settings import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

class DatabaseHealthChecker(HealthChecker):
    """
    Validates database connectivity, pool metrics, and ORM readiness.
    Registers seamlessly into the enterprise Health Framework.
    """
    def __init__(self):
        self.timeout = settings.database.health_timeout
        # Naive cache preparation for future implementations where heavy checks are rate-limited
        self.cache_duration = settings.database.health_cache_duration
        
    async def check(self) -> HealthCheckResult:
        logger.debug("Database Health Started.")
        start_time = time.perf_counter()
        
        details = {
            "metadata_loaded": is_metadata_loaded(),
            "session_factory_ready": is_session_factory_ready(),
            "migration_status": "Not Checked" # Placeholder for future Alembic hook
        }
        
        try:
            # 1. Gather Pool Metrics
            pool_metrics = get_pool_metrics()
            details["pool"] = pool_metrics.model_dump()
            
            if getattr(pool_metrics, 'overflow', 0) > 0:
                logger.warning("Database Health Warning: Connection pool is overflowing.")

            # 2. Lightweight Ping Query (Do not use business queries)
            async def ping_db():
                factory = get_session_factory()
                if not factory:
                    raise Exception("Session factory is missing.")
                async with factory() as session:
                    await session.execute(text("SELECT 1"))
            
            await asyncio.wait_for(ping_db(), timeout=self.timeout)
            
            # 3. Assess Latency
            latency = (time.perf_counter() - start_time) * 1000
            
            status = DatabaseHealthStatus.HEALTHY
            if latency > 1000:  # over 1 second is degraded
                status = DatabaseHealthStatus.DEGRADED
                logger.warning(f"Database Health Degraded. High latency: {latency:.2f}ms")
            else:
                logger.debug(f"Database Health Success. Latency: {latency:.2f}ms")
                
            return HealthCheckResult(
                name="PostgreSQL",
                status=status,
                latency_ms=round(latency, 2),
                details=details
            )
            
        except asyncio.TimeoutError:
            latency = (time.perf_counter() - start_time) * 1000
            logger.error(f"Connection Timeout during health check (> {self.timeout}s).")
            details["error"] = "Connection Timeout"
            return HealthCheckResult(
                name="PostgreSQL",
                status=DatabaseHealthStatus.UNHEALTHY,
                latency_ms=round(latency, 2),
                details=details
            )
        except Exception as e:
            latency = (time.perf_counter() - start_time) * 1000
            logger.error(f"Database Health Failed: {e}")
            details["error"] = str(e)
            return HealthCheckResult(
                name="PostgreSQL",
                status=DatabaseHealthStatus.UNHEALTHY,
                latency_ms=round(latency, 2),
                details=details
            )
