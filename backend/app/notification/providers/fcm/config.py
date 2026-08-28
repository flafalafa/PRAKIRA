"""FCM Configuration."""
from pydantic import BaseModel

class FCMConfig(BaseModel):
    enabled: bool = True
    default_ttl_seconds: int = 3600
    high_priority_ttl_seconds: int = 86400
    max_batch_size: int = 500
    retryable_errors: list = ["unavailable", "internal-error"]
    credentials_path: str = "google-services.json"
