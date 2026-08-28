"""Database engine factory and configuration."""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from app.config.settings import settings
from app.core.logger import get_logger

logger = get_logger(__name__)

class DatabaseEngineManager:
    """Manages the SQLAlchemy AsyncEngine lifecycle."""
    
    def __init__(self) -> None:
        self._engine: Optional[AsyncEngine] = None
        
    def get_engine(self) -> AsyncEngine:
        """Get the configured async engine. Lazy initialization."""
        if self._engine is None:
            self._init_engine()
        return self._engine
        
    def _init_engine(self) -> None:
        """Initialize the async engine using application settings."""
        db_settings = settings.db
        
        logger.info(
            "Initializing ORM persistence engine", 
            extra={
                "pool_size": db_settings.pool_size,
                "max_overflow": db_settings.max_overflow,
                "pool_timeout": db_settings.pool_timeout,
                "pool_recycle": db_settings.pool_recycle
            }
        )
        
        # Determine URL safely (sqlite in memory as fallback)
        url = db_settings.uri.get_secret_value() if db_settings.uri else "sqlite+aiosqlite:///:memory:"
        
        # Configure pool args based on backend
        pool_args = {}
        if url.startswith("postgresql"):
            pool_args = {
                "pool_size": db_settings.pool_size,
                "max_overflow": db_settings.max_overflow,
                "pool_timeout": db_settings.pool_timeout,
                "pool_recycle": db_settings.pool_recycle,
                "pool_pre_ping": True,
            }
        
        self._engine = create_async_engine(
            url,
            echo=db_settings.echo_sql or settings.app.debug,
            **pool_args
        )
        
    async def dispose(self) -> None:
        """Dispose of the engine connection pool cleanly."""
        if self._engine is not None:
            logger.info("Disposing persistence engine pool")
            await self._engine.dispose()
            self._engine = None

# Global engine manager
engine_manager = DatabaseEngineManager()
