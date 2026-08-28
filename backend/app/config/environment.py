"""Environment definitions."""
from enum import Enum


class EnvironmentType(str, Enum):
    """Supported application environments."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"

    @property
    def is_development(self) -> bool:
        return self == EnvironmentType.DEVELOPMENT
        
    @property
    def is_testing(self) -> bool:
        return self == EnvironmentType.TESTING
        
    @property
    def is_production(self) -> bool:
        return self == EnvironmentType.PRODUCTION
