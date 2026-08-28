"""Weather Analysis Rules."""
from abc import ABC, abstractmethod
from typing import List
from app.decision.weather.context import WeatherContext
from app.decision.weather.metrics import WeatherMetrics

class BaseWeatherRule(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass
        
    @abstractmethod
    async def evaluate(self, context: WeatherContext) -> bool:
        pass

class HeavyRainRule(BaseWeatherRule):
    name = "HEAVY_RAIN"
    async def evaluate(self, context: WeatherContext) -> bool:
        avg = WeatherMetrics.calculate_average_rainfall(context.rainfall_observations)
        return avg > 10.0
