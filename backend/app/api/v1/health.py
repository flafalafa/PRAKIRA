import sys
import datetime
from datetime import timezone
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.config.settings import settings
from app.core.logger import get_logger
from app.health import APP_START_TIME, get_uptime_string
from app.health.registry import readiness_registry, liveness_registry
from app.health.responses import HealthResponse, VersionResponse, InfoResponse
from app.health.status import HealthStatus
from app.health.models import HealthCheckResult

logger = get_logger(__name__)
router = APIRouter(tags=["Health"])

def aggregate_status(checks: list[HealthCheckResult]) -> HealthStatus:
    """Aggregate multiple check statuses into a single system status."""
    if not checks:
        return HealthStatus.HEALTHY
    has_degraded = False
    for check in checks:
        if check.status == HealthStatus.UNHEALTHY:
            return HealthStatus.UNHEALTHY
        if check.status == HealthStatus.DEGRADED:
            has_degraded = True
    return HealthStatus.DEGRADED if has_degraded else HealthStatus.HEALTHY


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """General application health summary."""
    logger.debug("Health check requested")
    
    # Run both liveness and readiness checks for a full summary
    l_checks = await liveness_registry.run_all()
    r_checks = await readiness_registry.run_all()
    all_checks = l_checks + r_checks
    
    status = aggregate_status(all_checks)
    
    response = HealthResponse(
        success=status != HealthStatus.UNHEALTHY,
        status=status,
        timestamp=datetime.datetime.now(timezone.utc).isoformat(),
        uptime=get_uptime_string(),
        checks=all_checks
    )
    
    status_code = 200 if status != HealthStatus.UNHEALTHY else 503
    return JSONResponse(status_code=status_code, content=response.model_dump(mode="json"))


@router.get("/ready", response_model=HealthResponse)
async def readiness_check():
    """Indicates whether the application is ready to receive traffic (Dependencies checked)."""
    logger.debug("Readiness check requested")
    checks = await readiness_registry.run_all()
    status = aggregate_status(checks)
    
    response = HealthResponse(
        success=status != HealthStatus.UNHEALTHY,
        status=status,
        timestamp=datetime.datetime.now(timezone.utc).isoformat(),
        uptime=get_uptime_string(),
        checks=checks
    )
    status_code = 200 if status != HealthStatus.UNHEALTHY else 503
    return JSONResponse(status_code=status_code, content=response.model_dump(mode="json"))


@router.get("/live", response_model=HealthResponse)
async def liveness_check():
    """Indicates whether the application process is alive (Independent from infrastructure)."""
    logger.debug("Liveness check requested")
    checks = await liveness_registry.run_all()
    status = aggregate_status(checks)
    
    response = HealthResponse(
        success=status != HealthStatus.UNHEALTHY,
        status=status,
        timestamp=datetime.datetime.now(timezone.utc).isoformat(),
        uptime=get_uptime_string(),
        checks=checks
    )
    status_code = 200 if status != HealthStatus.UNHEALTHY else 503
    return JSONResponse(status_code=status_code, content=response.model_dump(mode="json"))


@router.get("/version", response_model=VersionResponse)
async def version_info():
    """Return version and deployment metadata."""
    return VersionResponse(
        name=settings.app.name,
        version=settings.app.version,
        environment=settings.app.environment.value,
        git_commit="placeholder-commit",
        build_number="placeholder-build"
    )

@router.get("/info", response_model=InfoResponse)
async def system_info():
    """Return extended application runtime information."""
    return InfoResponse(
        name=settings.app.name,
        description=settings.app.description,
        environment=settings.app.environment.value,
        start_time=APP_START_TIME.isoformat(),
        uptime=get_uptime_string(),
        timezone="UTC",
        python_version=sys.version.split(" ")[0]
    )
