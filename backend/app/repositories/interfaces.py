"""Repository Interfaces (Contracts)."""
from typing import TypeVar, Generic, Optional
from abc import ABC, abstractmethod
from app.repositories.pagination import PaginationParams, PaginatedResult
from app.repositories.sorting import SortingParams
from app.repositories.filters import FilterParams
from app.repositories.specification import Specification

T = TypeVar("T")
ID = TypeVar("ID")

class IRepository(Generic[T, ID], ABC):
    """Base generic repository contract for Flood Guardian."""
    
    @abstractmethod
    async def get_by_id(self, id: ID) -> Optional[T]:
        """Fetch an entity by its primary key."""
        pass

    @abstractmethod
    async def exists(self, id: ID) -> bool:
        """Check if an entity exists by its primary key."""
        pass

    @abstractmethod
    async def create(self, entity: T) -> T:
        """Persist a new entity."""
        pass

    @abstractmethod
    async def update(self, entity: T) -> T:
        """Update an existing entity."""
        pass

    @abstractmethod
    async def delete(self, id: ID) -> None:
        """Hard delete an entity by ID."""
        pass

    @abstractmethod
    async def soft_delete(self, id: ID, user_id: Optional[str] = None) -> None:
        """Soft delete an entity by ID, optionally tracking the user who deleted it."""
        pass

    @abstractmethod
    async def restore(self, id: ID) -> None:
        """Restore a soft-deleted entity."""
        pass

    @abstractmethod
    async def count(self, spec: Optional[Specification] = None) -> int:
        """Count entities, optionally matching a specification."""
        pass

    @abstractmethod
    async def find_one(self, spec: Specification) -> Optional[T]:
        """Find a single entity matching a specification."""
        pass

    @abstractmethod
    async def list(
        self,
        filters: Optional[FilterParams] = None,
        sorting: Optional[SortingParams] = None,
        pagination: Optional[PaginationParams] = None,
        spec: Optional[Specification] = None,
        include_deleted: bool = False
    ) -> PaginatedResult[T]:
        """List entities with full support for pagination, sorting, filtering, and specifications."""
        pass
