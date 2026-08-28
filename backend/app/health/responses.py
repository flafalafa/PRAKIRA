"""Standardized API health responses."""
from pydantic import BaseModel
from app.health.status import HealthStatus
from app.health.models import HealthCheckResult

class HealthResponse(BaseModel):
    """Standardized response for /health, /ready, and /live endpoints."""
    success: bool
    status: HealthStatus
    timestamp: str
    uptime: str
    checks: list[HealthCheckResult]

class VersionResponse(BaseModel):
    """Response for /version endpoint."""
    name: str
    version: str
    environment: str
    git_commit: str
    build_number: str

class InfoResponse(BaseModel):
    """Response for /info endpoint."""
    name: str
    description: str
    environment: str
    start_time: str
    uptime: str
    timezone: str
    python_version: str
