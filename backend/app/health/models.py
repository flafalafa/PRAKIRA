"""Health check models."""
from typing import Any
from pydantic import BaseModel
from app.health.status import HealthStatus

class HealthCheckResult(BaseModel):
    """Result of a single component health check."""
    name: str
    status: HealthStatus
    latency_ms: float = 0.0
    details: dict[str, Any] = {}
