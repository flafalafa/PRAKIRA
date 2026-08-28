"""Abstract Base Repository."""
from typing import TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logger import get_logger
from app.repositories.interfaces import IRepository

T = TypeVar("T")
ID = TypeVar("ID")

class BaseRepository(IRepository[T, ID]):
    """
    Abstract Base Repository.
    Integrates the injected AsyncSession and provides base logging capabilities.
    All Generic or Specific repositories must inherit from this.
    """
    
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.logger = get_logger(f"repository.{self.__class__.__name__}")
        self.logger.debug("Repository Instantiated")
