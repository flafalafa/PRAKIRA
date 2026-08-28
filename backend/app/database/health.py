"""Database health module aggregator."""
from app.database.checker import DatabaseHealthChecker
from app.database.registry import register_database_health

__all__ = ["DatabaseHealthChecker", "register_database_health"]
