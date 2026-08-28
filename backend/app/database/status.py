"""Database health status definitions."""
from app.health.status import HealthStatus

# Re-export HealthStatus to maintain bounded context within the database module
DatabaseHealthStatus = HealthStatus
