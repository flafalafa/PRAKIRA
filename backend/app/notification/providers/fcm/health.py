"""FCM Health Check."""
from datetime import datetime, timezone
from app.notification.providers.base.models import ProviderHealth, ProviderHealthStatus
import time

class FCMHealthChecker:
    @staticmethod
    async def check() -> ProviderHealth:
        # Mock health check
        start = time.time()
        latency = (time.time() - start) * 1000
        return ProviderHealth(
            status=ProviderHealthStatus.AVAILABLE,
            latency_ms=latency,
            auth_status="AUTHORIZED",
            config_status="VALID",
            timestamp=datetime.now(timezone.utc)
        )
