"""Database pool metrics definitions."""
from pydantic import BaseModel

class DatabasePoolMetrics(BaseModel):
    """Metrics regarding the SQLAlchemy connection pool."""
    pool_size: int = 0
    checked_out_connections: int = 0
    idle_connections: int = 0
    overflow: int = 0
    pool_timeout: int = 0
