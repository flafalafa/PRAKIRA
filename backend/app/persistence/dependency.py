"""FastAPI Session Dependency."""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.persistence.lifecycle import session_lifecycle

async def get_session_dependency() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI Depends() generator for database sessions.
    
    Yields a session that is fully transaction-managed and injected 
    into the current context variable. Guarantees no connection leaks.
    
    Usage:
        @router.get("/users")
        async def get_users(session: AsyncSession = Depends(get_session_dependency)):
            ...
    """
    async with session_lifecycle() as session:
        yield session
