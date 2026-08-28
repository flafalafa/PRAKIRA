"""Collector interfaces."""
from abc import ABC, abstractmethod
from typing import Any, Dict

class IProvider(ABC):
    """Contract that all external providers must implement."""
    
    @abstractmethod
    async def connect(self) -> None:
        pass
        
    @abstractmethod
    async def fetch(self, **kwargs) -> Any:
        pass
        
    @abstractmethod
    async def parse(self, raw_data: Any) -> Any:
        pass
        
    @abstractmethod
    async def normalize(self, parsed_data: Any) -> Any:
        pass
        
    @abstractmethod
    async def validate(self, normalized_data: Any) -> bool:
        pass
        
    @abstractmethod
    async def health(self) -> bool:
        pass
        
    @abstractmethod
    async def metadata(self) -> Dict[str, Any]:
        pass
        
    @abstractmethod
    async def disconnect(self) -> None:
        pass
