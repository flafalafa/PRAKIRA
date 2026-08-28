"""Database health registry integration."""
from app.health.registry import readiness_registry
from app.database.checker import DatabaseHealthChecker
from app.config.settings import settings

def register_database_health() -> None:
    """Registers the database health checker if enabled in configuration."""
    if settings.database.enable_health_check:
        checker = DatabaseHealthChecker()
        readiness_registry.register(checker)
