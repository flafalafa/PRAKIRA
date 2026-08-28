"""Database diagnostic utilities."""
from app.persistence.engine import engine_manager
from app.persistence.session import get_session_factory
from app.database.metrics import DatabasePoolMetrics
from sqlalchemy.pool import QueuePool

def get_pool_metrics() -> DatabasePoolMetrics:
    """Extracts connection pool metrics safely without exposing credentials."""
    metrics = DatabasePoolMetrics()
    try:
        engine = engine_manager.get_engine()
        sync_engine = engine.sync_engine
        pool = sync_engine.pool
        
        # Only QueuePool natively supports these fine-grained stats
        if isinstance(pool, QueuePool):
            metrics.pool_size = pool.size()
            metrics.checked_out_connections = pool.checkedout()
            metrics.idle_connections = pool.checkedin()
            metrics.overflow = pool.overflow()
            metrics.pool_timeout = pool.timeout()
    except Exception:
        # If engine is not fully initialized, return zeroed metrics safely
        pass
        
    return metrics

def is_metadata_loaded() -> bool:
    """Validates that SQLAlchemy metadata is properly initialized."""
    try:
        from app.persistence.metadata import metadata
        return len(metadata.tables) > 0
    except Exception:
        return False

def is_session_factory_ready() -> bool:
    """Validates that the session factory can be built."""
    try:
        factory = get_session_factory()
        return factory is not None
    except Exception:
        return False
