"""Prediction repository interface."""
from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime
from app.domain.entities.flood_prediction import FloodPrediction

class IPredictionRepository(ABC):
    @abstractmethod
    async def save(self, prediction: FloodPrediction) -> FloodPrediction:
        pass
        
    @abstractmethod
    async def find_by_id(self, id: str) -> Optional[FloodPrediction]:
        pass
        
    @abstractmethod
    async def find_latest(self, area_id: str) -> Optional[FloodPrediction]:
        pass

    @abstractmethod
    async def find_by_area(self, area_id: str) -> List[FloodPrediction]:
        pass

    @abstractmethod
    async def find_active(self) -> List[FloodPrediction]:
        pass

    @abstractmethod
    async def find_by_risk_level(self, risk_level: str) -> List[FloodPrediction]:
        pass
        
    @abstractmethod
    async def find_critical(self) -> List[FloodPrediction]:
        pass

    @abstractmethod
    async def find_by_time_range(self, start_time: datetime, end_time: datetime) -> List[FloodPrediction]:
        pass
        
    @abstractmethod
    async def exists(self, id: str) -> bool:
        pass
        
    @abstractmethod
    async def list(self) -> List[FloodPrediction]:
        pass
        
    @abstractmethod
    async def soft_delete(self, id: str) -> None:
        pass
