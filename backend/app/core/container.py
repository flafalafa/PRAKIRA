"""Dependency Injection Container."""
from enum import Enum
from typing import Any, Callable, TypeVar, Type

T = TypeVar("T")

class Lifetime(Enum):
    """Lifecycle definition for registered dependencies."""
    SINGLETON = "singleton"    # One instance per application lifetime
    TRANSIENT = "transient"    # New instance every time it is requested
    SCOPED = "scoped"          # One instance per request (relies on FastAPI Depends context)

class DependencyRegistration:
    def __init__(self, interface: Type, factory: Callable[..., Any], lifetime: Lifetime):
        self.interface = interface
        self.factory = factory
        self.lifetime = lifetime
        self.instance: Any = None

class DIContainer:
    """Central Dependency Injection Container."""
    def __init__(self) -> None:
        self._registrations: dict[Type, DependencyRegistration] = {}
    
    def register(self, interface: Type, factory: Callable[..., Any], lifetime: Lifetime = Lifetime.TRANSIENT) -> None:
        """Register a dependency with a specific lifetime."""
        if interface in self._registrations:
            raise ValueError(f"Dependency {interface.__name__} is already registered.")
        self._registrations[interface] = DependencyRegistration(interface, factory, lifetime)
        
    def resolve(self, interface: Type[T]) -> T:
        """Resolve a dependency, creating it if necessary according to its lifetime."""
        if interface not in self._registrations:
            raise ValueError(f"Dependency {interface.__name__} is not registered.")
            
        reg = self._registrations[interface]
        
        if reg.lifetime == Lifetime.SINGLETON:
            if reg.instance is None:
                # Pass container to factory for sub-dependency resolution
                reg.instance = reg.factory(self)
            return reg.instance
            
        # TRANSIENT and SCOPED (Scoped relies on FastAPI Depends to manage per request caching implicitly)
        return reg.factory(self)
        
    def is_registered(self, interface: Type) -> bool:
        """Check if an interface is registered."""
        return interface in self._registrations

    def clear(self) -> None:
        """Clear all registrations (useful for testing)."""
        self._registrations.clear()
        
# Global DI Container instance
container = DIContainer()
