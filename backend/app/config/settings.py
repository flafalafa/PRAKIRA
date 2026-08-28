"""Enterprise configuration system."""
import json
import logging
from functools import lru_cache
from typing import Any
from pydantic import BaseModel, Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.config.environment import EnvironmentType
from app.config.constants import PROJECT_NAME, PROJECT_VERSION, PROJECT_DESCRIPTION, DEFAULT_API_PREFIX
from app.config.paths import ensure_directories
from app.config.validators import mask_secret

logger = logging.getLogger(__name__)

class AppSettings(BaseModel):
    """Core application settings."""
    name: str = Field(default=PROJECT_NAME)
    version: str = Field(default=PROJECT_VERSION)
    description: str = Field(default=PROJECT_DESCRIPTION)
    environment: EnvironmentType = Field(default=EnvironmentType.DEVELOPMENT)
    debug: bool = Field(default=False)
    
class APISettings(BaseModel):
    """API specific settings."""
    prefix: str = Field(default=DEFAULT_API_PREFIX)
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)

class LoggingSettings(BaseModel):
    """Logging configuration."""
    level: str = Field(default="INFO")
    format: str = Field(default="json")
    log_to_file: bool = Field(default=False)
    log_to_console: bool = Field(default=True)
    log_file_path: str = Field(default="logs/app.log")
    
    @field_validator("level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        v_upper = v.upper()
        if v_upper not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError(f"Invalid log level: {v}")
        return v_upper

class DatabaseSettings(BaseModel):
    """Database connection and pooling configuration."""
    uri: SecretStr | None = None
    pool_size: int = Field(default=10)
    max_overflow: int = Field(default=20)
    pool_timeout: int = Field(default=30)
    pool_recycle: int = Field(default=1800)
    echo_sql: bool = Field(default=False)
    auto_flush: bool = Field(default=False)
    expire_on_commit: bool = Field(default=False)
    
    # Health Monitoring Settings
    health_timeout: float = Field(default=5.0)
    enable_health_check: bool = Field(default=True)
    health_cache_duration: int = Field(default=10)

class RedisSettings(BaseModel):
    """Redis configuration placeholders."""
    url: str | None = None
    
class JWTSettings(BaseModel):
    """JWT configuration placeholders."""
    secret_key: SecretStr | None = None
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)
    
class NotificationSettings(BaseModel):
    """Notification placeholders."""
    fcm_server_key: SecretStr | None = None
    
class WeatherProviderSettings(BaseModel):
    """Weather API configuration placeholders."""
    api_key: SecretStr | None = None
    base_url: str | None = None

class StorageSettings(BaseModel):
    """Storage placeholders (e.g. S3)."""
    bucket_name: str | None = None
    access_key: SecretStr | None = None
    secret_key: SecretStr | None = None
    
class SecuritySettings(BaseModel):
    """Security configuration."""
    allowed_hosts: list[str] = Field(default=["*"])
    cors_origins: list[str] = Field(default=["*"])
    content_type_options: str = Field(default="nosniff")
    frame_options: str = Field(default="DENY")
    referrer_policy: str = Field(default="strict-origin-when-cross-origin")
    content_security_policy: str = Field(default="default-src 'self'")
    permissions_policy: str = Field(default="geolocation=(), microphone=()")
    strict_transport_security: str = Field(default="max-age=31536000; includeSubDomains")

class PerformanceSettings(BaseModel):
    """Performance metrics configuration."""
    slow_request_threshold_ms: int = Field(default=1000)

class FeatureFlags(BaseModel):
    """Runtime feature toggles."""
    enable_notification: bool = Field(default=False)
    enable_ai: bool = Field(default=False)
    enable_community_report: bool = Field(default=False)
    enable_weather_collector: bool = Field(default=False)
    enable_radar: bool = Field(default=False)
    enable_river: bool = Field(default=False)
    enable_analytics: bool = Field(default=False)
    enable_maintenance_mode: bool = Field(default=False)

class Settings(BaseSettings):
    """Main settings class mapping to environment variables and nested models."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
        case_sensitive=False
    )
    
    app: AppSettings = Field(default_factory=AppSettings)
    api: APISettings = Field(default_factory=APISettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    jwt: JWTSettings = Field(default_factory=JWTSettings)
    notification: NotificationSettings = Field(default_factory=NotificationSettings)
    weather: WeatherProviderSettings = Field(default_factory=WeatherProviderSettings)
    storage: StorageSettings = Field(default_factory=StorageSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    performance: PerformanceSettings = Field(default_factory=PerformanceSettings)
    features: FeatureFlags = Field(default_factory=FeatureFlags)

    def get_safe_config(self) -> dict[str, Any]:
        """Dump configuration safely without exposing secrets."""
        data = self.model_dump()
        safe_data = data.copy()
        
        for category, config in safe_data.items():
            if isinstance(config, dict):
                for k, v in config.items():
                    # Mask sensitive keys
                    if any(secret_term in k.lower() for secret_term in ["secret", "key", "password", "token", "url"]):
                        if isinstance(v, SecretStr):
                            safe_data[category][k] = mask_secret(v.get_secret_value())
                        elif v:
                            safe_data[category][k] = mask_secret(v)
                            
        return safe_data

    def log_config(self) -> None:
        """Safely logs the application configuration at startup."""
        safe_config = self.get_safe_config()
        # Ensure directory is ready
        ensure_directories()
        logger.info(f"Loaded Settings: {json.dumps(safe_config)}")

@lru_cache()
def get_settings() -> Settings:
    """Lazy load settings using Singleton pattern via lru_cache."""
    return Settings()

# Global settings instance
settings = get_settings()
