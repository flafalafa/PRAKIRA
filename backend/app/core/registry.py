"""Centralized Dependency Registry."""
from app.core.container import container, Lifetime
from app.core.interfaces import (
    ILogger, IConfiguration, IDatabase, IRedis,
    INotifier, IWeatherProvider, IRepository,
    IDecisionEngine, IPredictionEngine, IStorage
)
from app.core.providers import (
    ConfigurationProvider, LoggerProvider, DatabaseProvider,
    RedisProvider, NotificationProvider, WeatherProvider,
    RepositoryProvider, DecisionEngineProvider, PredictionEngineProvider,
    StorageProvider
)

def register_dependencies() -> None:
    """Register all application dependencies to the container."""
    
    # Infrastructure Providers
    container.register(IConfiguration, lambda c: ConfigurationProvider(), Lifetime.SINGLETON)
    container.register(ILogger, lambda c: LoggerProvider(), Lifetime.SINGLETON)
    container.register(IDatabase, lambda c: DatabaseProvider(), Lifetime.SINGLETON)
    container.register(IRedis, lambda c: RedisProvider(), Lifetime.SINGLETON)
    container.register(IStorage, lambda c: StorageProvider(), Lifetime.SINGLETON)
    
    # External Providers
    container.register(IWeatherProvider, lambda c: WeatherProvider(), Lifetime.SINGLETON)
    container.register(INotifier, lambda c: NotificationProvider(), Lifetime.SINGLETON)
    
    # Repositories (Data Access)
    container.register(IRepository, lambda c: RepositoryProvider(), Lifetime.TRANSIENT)
    
    # Domain Engines (Business Logic)
    container.register(IDecisionEngine, lambda c: DecisionEngineProvider(), Lifetime.TRANSIENT)
    container.register(IPredictionEngine, lambda c: PredictionEngineProvider(), Lifetime.TRANSIENT)
