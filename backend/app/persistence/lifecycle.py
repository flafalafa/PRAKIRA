"""Lifecycle orchestrator for Database Sessions."""
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from app.persistence.manager import transaction_manager
from app.persistence.context import set_current_session, reset_current_session
from app.core.logger import get_logger

logger = get_logger(__name__)

@asynccontextmanager
async def session_lifecycle() -> AsyncGenerator[AsyncSession, None]:
    """
    Governs the absolute lifecycle of a database session within an execution flow.
    
    1. Creates session and wraps in transaction.
    2. Injects session into ContextVar for background workers / UoW.
    3. Yields session to the caller.
    4. Cleans up ContextVar and closes session.
    """
    async with transaction_manager.session() as session:
        # Inject into global context variable
        token = set_current_session(session)
        logger.debug("Session injected into ContextVar.")
        try:
            yield session
        finally:
            # Clean up context variable
            reset_current_session(token)
            logger.debug("Session removed from ContextVar.")
