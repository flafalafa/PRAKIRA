"""Flood Event repository interface."""
from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime
from app.domain.entities.flood_event import FloodEvent

class IFloodEventRepository(ABC):
    """
    Contract for Flood Event persistence.
    Isolates domain logic from persistence framework.
    """
    
    @abstractmethod
    async def save(self, event: FloodEvent) -> FloodEvent:
        pass
        
    @abstractmethod
    async def find_by_id(self, id: str) -> Optional[FloodEvent]:
        pass
        
    @abstractmethod
    async def find_by_area(self, area_id: str) -> List[FloodEvent]:
        pass

    @abstractmethod
    async def find_active(self) -> List[FloodEvent]:
        pass

    @abstractmethod
    async def find_by_severity(self, severity: str) -> List[FloodEvent]:
        pass
        
    @abstractmethod
    async def find_by_time_range(self, start_time: datetime, end_time: datetime) -> List[FloodEvent]:
        pass
        
    @abstractmethod
    async def find_verified(self) -> List[FloodEvent]:
        pass
        
    @abstractmethod
    async def find_ground_truth(self) -> List[FloodEvent]:
        pass
        
    @abstractmethod
    async def exists(self, id: str) -> bool:
        pass
        
    @abstractmethod
    async def list(self) -> List[FloodEvent]:
        pass
        
    @abstractmethod
    async def soft_delete(self, id: str) -> None:
        pass
