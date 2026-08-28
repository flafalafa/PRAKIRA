"""Transaction Context and Savepoints."""
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logger import get_logger

logger = get_logger(__name__)

@asynccontextmanager
async def transactional(session: AsyncSession) -> AsyncGenerator[AsyncSession, None]:
    """
    Wraps database operations in a strict transaction.
    Automatically handles commits, rollbacks, and nested savepoints.
    """
    if session.in_nested_transaction():
        # Already inside a savepoint, create a deeper nested savepoint
        async with session.begin_nested():
            logger.debug("Nested transaction (Savepoint) started.")
            try:
                yield session
            except Exception as e:
                logger.error(f"Nested transaction failed, rolling back savepoint. Error: {str(e)}")
                raise
    elif session.in_transaction():
        # Already inside a transaction, use a savepoint to prevent ruining the parent transaction
        async with session.begin_nested():
            logger.debug("Transaction active. Using Savepoint for current block.")
            try:
                yield session
            except Exception as e:
                logger.error(f"Savepoint failed, rolling back block. Error: {str(e)}")
                raise
    else:
        # Start a brand new transaction
        logger.debug("Transaction started.")
        try:
            yield session
            await session.commit()
            logger.debug("Transaction committed successfully.")
        except Exception as e:
            await session.rollback()
            logger.error(f"Transaction failed, rolling back completely. Error: {str(e)}")
            raise
