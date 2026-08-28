"""Rainfall repository interface."""
from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime
from app.domain.entities.rainfall import RainfallEntity

class IRainfallRepository(ABC):
    """Contract for Rainfall persistence."""
    
    @abstractmethod
    async def save(self, rainfall: RainfallEntity) -> RainfallEntity:
        pass
        
    @abstractmethod
    async def find_by_id(self, id: str) -> Optional[RainfallEntity]:
        pass
        
    @abstractmethod
    async def find_latest(self, area_id: str) -> Optional[RainfallEntity]:
        pass

    @abstractmethod
    async def find_by_area(self, area_id: str) -> List[RainfallEntity]:
        pass

    @abstractmethod
    async def find_by_river(self, river_id: str) -> List[RainfallEntity]:
        pass
        
    @abstractmethod
    async def find_by_time_range(self, area_id: str, start_time: datetime, end_time: datetime) -> List[RainfallEntity]:
        pass
        
    @abstractmethod
    async def find_validated(self, area_id: str) -> List[RainfallEntity]:
        pass
        
    @abstractmethod
    async def exists(self, id: str) -> bool:
        pass
        
    @abstractmethod
    async def list(self) -> List[RainfallEntity]:
        pass
        
    @abstractmethod
    async def soft_delete(self, id: str) -> None:
        pass
