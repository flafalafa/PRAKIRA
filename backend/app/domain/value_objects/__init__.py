"""Value Objects package."""
from .exceptions import DomainError, ValueObjectValidationError
from .base import BaseValueObject
from .geography import Coordinate, Latitude, Longitude, Distance, AreaCode, RiverCode
from .hydrology import Rainfall, RainfallIntensity, WaterLevel, RiverFlowRate
from .weather import WindSpeed, WindDirection, Temperature, Humidity, Pressure
from .analysis import RiskScore, PredictionConfidence, NotificationPriority
from .core import TimestampUTC, Duration

__all__ = [
    "DomainError",
    "ValueObjectValidationError",
    "BaseValueObject",
    
    # Geography
    "Coordinate", "Latitude", "Longitude", "Distance", "AreaCode", "RiverCode",
    
    # Hydrology
    "Rainfall", "RainfallIntensity", "WaterLevel", "RiverFlowRate",
    
    # Weather
    "WindSpeed", "WindDirection", "Temperature", "Humidity", "Pressure",
    
    # Analysis
    "RiskScore", "PredictionConfidence", "NotificationPriority",
    
    # Core
    "TimestampUTC", "Duration"
]
