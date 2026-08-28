"""Dependency injection configuration."""
from app.config.settings import Settings, get_settings


def get_current_settings() -> Settings:
    """Provide application settings."""
    return get_settings()

# Placeholders for future DI (e.g. get_db, get_redis)
