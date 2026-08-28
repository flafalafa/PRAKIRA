"""Provider Factory."""
from app.notification.providers.base.registry import ProviderRegistry
from app.notification.providers.base.provider import BasePushProvider

class ProviderFactory:
    @staticmethod
    def get_primary_provider() -> BasePushProvider:
        providers = ProviderRegistry.get_all_enabled()
        if not providers:
            raise RuntimeError("No active push providers available")
        return providers[0]
