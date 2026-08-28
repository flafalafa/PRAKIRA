"""Database session factory configuration."""
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from app.persistence.engine import engine_manager
from app.config.settings import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

_async_session_factory = None

def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Get or initialize the async session factory."""
    global _async_session_factory
    if _async_session_factory is None:
        engine = engine_manager.get_engine()
        _async_session_factory = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=settings.db.expire_on_commit,
            autoflush=settings.db.auto_flush
        )
        logger.info("Async session factory initialized.")
    return _async_session_factory
