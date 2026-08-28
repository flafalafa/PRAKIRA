"""Unit of Work Interfaces."""
from abc import ABC, abstractmethod
from typing import Any

class IUnitOfWork(ABC):
    """
    Abstract Unit of Work contract.
    Ensures that multiple repositories can be used within a single transactional boundary.
    """
    
    # Placeholders for future repositories
    # users: IUserRepository
    # rivers: IRiverRepository
    # weather: IWeatherRepository
    # predictions: IPredictionRepository
    # notifications: INotificationRepository
    # reports: ICommunityReportRepository
    # areas: IAreaRepository

    @abstractmethod
    async def __aenter__(self) -> "IUnitOfWork":
        """Start the transactional boundary context."""
        pass

    @abstractmethod
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit the transactional boundary context and cleanup resources."""
        pass

    @abstractmethod
    async def commit(self) -> None:
        """Commit the underlying transaction."""
        pass

    @abstractmethod
    async def rollback(self) -> None:
        """Rollback the underlying transaction."""
        pass
