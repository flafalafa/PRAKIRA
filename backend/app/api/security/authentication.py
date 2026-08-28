"""Authentication Abstraction."""
from abc import ABC, abstractmethod
from typing import Optional
from fastapi import Request
from app.api.security.context import SecurityContext

class BaseAuthenticationProvider(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass
        
    @abstractmethod
    async def authenticate(self, request: Request) -> Optional[SecurityContext]:
        pass
