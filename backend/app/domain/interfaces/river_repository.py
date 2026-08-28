"""River repository interface."""
from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.river import River

class IRiverRepository(ABC):
    """
    Contract for River persistence.
    Domain layer depends on this interface, shielding it from SQLAlchemy/Databases.
    """
    
    @abstractmethod
    async def save(self, river: River) -> River:
        pass
        
    @abstractmethod
    async def find_by_id(self, id: str) -> Optional[River]:
        pass
        
    @abstractmethod
    async def find_by_code(self, code: str) -> Optional[River]:
        pass
        
    @abstractmethod
    async def find_by_area(self, area_id: str) -> List[River]:
        pass

    @abstractmethod
    async def find_active(self) -> List[River]:
        pass
        
    @abstractmethod
    async def exists(self, id: str) -> bool:
        pass
        
    @abstractmethod
    async def list(self) -> List[River]:
        pass
        
    @abstractmethod
    async def soft_delete(self, id: str) -> None:
        pass
