"""Dependency resolution factory and FastAPI integration."""
from typing import Type, TypeVar, Callable, Any
from app.core.container import container

T = TypeVar("T")

def inject(interface: Type[T]) -> Callable[[], T]:
    """
    FastAPI Depends() helper for lazy injection.
    
    Usage:
        @router.get("/data")
        def get_data(repo: IRepository = Depends(inject(IRepository))):
            pass
    """
    def _resolver() -> T:
        return container.resolve(interface)
    return _resolver

def resolve(interface: Type[T]) -> T:
    """
    Resolve a dependency manually outside of FastAPI request lifecycle.
    Useful for Background Workers, Kafka consumers, or setup scripts.
    """
    return container.resolve(interface)
