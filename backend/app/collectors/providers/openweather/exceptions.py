"""OpenWeather Collector specific exceptions."""
from app.collectors.exceptions import CollectorException

class OpenWeatherException(CollectorException):
    pass

class OpenWeatherConnectionError(OpenWeatherException):
    pass

class OpenWeatherTimeoutError(OpenWeatherException):
    pass

class OpenWeatherInvalidResponse(OpenWeatherException):
    pass

class OpenWeatherParsingError(OpenWeatherException):
    pass

class OpenWeatherAuthError(OpenWeatherException):
    pass

class OpenWeatherRateLimitError(OpenWeatherException):
    pass
