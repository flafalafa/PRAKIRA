"""Weather repository interface."""
from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime
from app.domain.entities.weather_observation import WeatherObservation

class IWeatherRepository(ABC):
    """
    Contract for Weather Observation persistence.
    Shields the domain from database logic.
    """
    
    @abstractmethod
    async def save(self, observation: WeatherObservation) -> WeatherObservation:
        pass
        
    @abstractmethod
    async def find_by_id(self, id: str) -> Optional[WeatherObservation]:
        pass
        
    @abstractmethod
    async def find_latest(self, area_id: str) -> Optional[WeatherObservation]:
        pass

    @abstractmethod
    async def find_by_area(self, area_id: str) -> List[WeatherObservation]:
        pass
        
    @abstractmethod
    async def find_by_station(self, station_id: str) -> List[WeatherObservation]:
        pass
        
    @abstractmethod
    async def find_by_time_range(self, area_id: str, start_time: datetime, end_time: datetime) -> List[WeatherObservation]:
        pass
        
    @abstractmethod
    async def find_validated(self, area_id: str) -> List[WeatherObservation]:
        pass
        
    @abstractmethod
    async def exists(self, id: str) -> bool:
        pass
        
    @abstractmethod
    async def list(self) -> List[WeatherObservation]:
        pass
        
    @abstractmethod
    async def soft_delete(self, id: str) -> None:
        pass
