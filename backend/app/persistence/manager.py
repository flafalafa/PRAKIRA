"""Enterprise Transaction Manager."""
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.persistence.session import get_session_factory
from app.persistence.transaction import transactional
from app.core.logger import get_logger

logger = get_logger(__name__)

class TransactionManager:
    """
    Central manager orchestrating the creation of sessions and 
    wrapping them securely in transactional contexts.
    """
    
    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Creates a new session, executes it within a transactional wrapper,
        and guarantees the session is closed cleanly afterwards.
        """
        factory = get_session_factory()
        session: AsyncSession = factory()
        logger.debug("Database Session created.")
        
        try:
            # Yield control to the transactional boundary
            async with transactional(session) as tx_session:
                yield tx_session
        finally:
            await session.close()
            logger.debug("Database Session closed. Resources freed.")

# Singleton instance
transaction_manager = TransactionManager()
