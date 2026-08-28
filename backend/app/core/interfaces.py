"""Abstract interfaces for Dependency Injection."""
from typing import Protocol, Any

class ILogger(Protocol):
    """Protocol for logging provider."""
    def info(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    def error(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None: ...
    def critical(self, msg: str, *args: Any, **kwargs: Any) -> None: ...

class IConfiguration(Protocol):
    """Protocol for configuration provider."""
    pass

class IDatabase(Protocol):
    """Protocol for database connection provider."""
    pass

class IRedis(Protocol):
    """Protocol for redis connection provider."""
    pass

class IRepository(Protocol):
    """Protocol for data repositories."""
    pass

class ICollector(Protocol):
    """Protocol for external data collectors."""
    pass

class IService(Protocol):
    """Protocol for business services."""
    pass

class INotifier(Protocol):
    """Protocol for notification engine."""
    pass

class IStorage(Protocol):
    """Protocol for blob/file storage."""
    pass

class IWeatherProvider(Protocol):
    """Protocol for external weather APIs."""
    pass

class IPredictionEngine(Protocol):
    """Protocol for flood prediction algorithms."""
    pass

class IDecisionEngine(Protocol):
    """Protocol for state machine and risk evaluation."""
    pass
