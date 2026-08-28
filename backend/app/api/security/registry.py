"""Authentication Provider Registry."""
from typing import List
from app.api.security.authentication import BaseAuthenticationProvider

class AuthenticationRegistry:
    _providers: List[BaseAuthenticationProvider] = []
    
    @classmethod
    def register(cls, provider: BaseAuthenticationProvider) -> None:
        cls._providers.append(provider)
        
    @classmethod
    def get_providers(cls) -> List[BaseAuthenticationProvider]:
        return cls._providers
