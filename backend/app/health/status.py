"""Health status definitions."""
from enum import Enum

class HealthStatus(str, Enum):
    """Possible health statuses for components and system."""
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"
    UNKNOWN = "UNKNOWN"
