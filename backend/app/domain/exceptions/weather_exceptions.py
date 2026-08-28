"""Weather domain exceptions."""
from app.exceptions.base import AppException

class WeatherDomainError(AppException):
    """Base exception for all weather domain errors."""
    pass

class WeatherValidationError(WeatherDomainError):
    """Raised when a weather observation violates a business rule."""
    pass

class InvalidObservationTime(WeatherValidationError):
    pass

class InvalidTemperature(WeatherValidationError):
    pass

class InvalidHumidity(WeatherValidationError):
    pass

class InvalidPressure(WeatherValidationError):
    pass

class InvalidRainfall(WeatherValidationError):
    pass

class InvalidWindSpeed(WeatherValidationError):
    pass

class InvalidConfidenceScore(WeatherValidationError):
    pass

class ObservationNotValidated(WeatherDomainError):
    """Raised when an operation requires a validated observation, but it is not."""
    pass
