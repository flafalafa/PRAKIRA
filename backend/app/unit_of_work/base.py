"""Base Unit of Work Implementation."""
from typing import Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.unit_of_work.interfaces import IUnitOfWork
from app.unit_of_work.exceptions import TransactionError
from app.persistence.session import get_session_factory
from app.core.logger import get_logger

logger = get_logger(__name__)

class BaseUnitOfWork(IUnitOfWork):
    """
    Base implementation of the Unit of Work.
    Manages the AsyncSession lifecycle and guarantees atomic transactions 
    across multiple injected repositories.
    """
    def __init__(self, session_factory=None):
        self._session_factory = session_factory or get_session_factory()
        self.session: Optional[AsyncSession] = None
        
        # Placeholders for Repositories (To be instantiated in __aenter__)
        # self.users = None
        # self.rivers = None

    async def __aenter__(self) -> "BaseUnitOfWork":
        self.session = self._session_factory()
        logger.debug("UnitOfWork Started. Database Session initialized.")
        
        # TODO: Instantiate specific repositories here, passing in `self.session`
        # self.users = UserRepository(self.session)
        # self.rivers = RiverRepository(self.session)
        
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        try:
            if exc_type is not None:
                # An exception occurred inside the UoW block
                await self.rollback()
                logger.error(f"Unexpected Exception during UoW execution. Transaction Rolled Back. Cause: {exc_val}")
            else:
                # The block executed successfully.
                # UoW pattern usually expects an explicit .commit() call in the Business Logic.
                # If the business logic forgot to call commit(), it is safer to rollback rather than auto-commit
                # to prevent partial/unintended state changes.
                pass
        except Exception as e:
            logger.critical(f"Failed to rollback transaction during UoW teardown: {e}")
            raise TransactionError(f"Failed to rollback transaction: {e}")
        finally:
            if self.session:
                await self.session.close()
                logger.debug("UnitOfWork Closed. Session resources freed.")

    async def commit(self) -> None:
        """Persists all changes made across all repositories in this UoW."""
        if not self.session:
            raise TransactionError("Cannot commit. Session not initialized.")
        try:
            await self.session.commit()
            logger.info("Transaction Committed successfully.")
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Transaction Commit Failed. Automatically Rolled back. Cause: {e}")
            raise TransactionError(f"Commit failed: {e}")

    async def rollback(self) -> None:
        """Discards all changes made across all repositories in this UoW."""
        if not self.session:
            return
        try:
            await self.session.rollback()
            logger.info("Transaction Rolled Back.")
        except Exception as e:
            logger.error(f"Manual rollback failed: {e}")
            raise TransactionError(f"Rollback failed: {e}")
