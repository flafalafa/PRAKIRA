"""Area repository interface."""
from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.area import Area

class IAreaRepository(ABC):
    """
    Contract for Area persistence.
    Domain layer depends on this interface, not the actual database implementation.
    """
    
    @abstractmethod
    async def save(self, area: Area) -> Area:
        pass
        
    @abstractmethod
    async def find_by_id(self, id: str) -> Optional[Area]:
        pass
        
    @abstractmethod
    async def find_by_code(self, code: str) -> Optional[Area]:
        pass
        
    @abstractmethod
    async def exists(self, id: str) -> bool:
        pass
        
    @abstractmethod
    async def list(self) -> List[Area]:
        pass
        
    @abstractmethod
    async def delete(self, id: str) -> None:
        """Preparation for soft delete."""
        pass
