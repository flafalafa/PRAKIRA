"""Configuration validators."""
from typing import Any
import os

def mask_secret(value: Any) -> str:
    """Mask a secret value for safe logging."""
    if not value:
        return ""
    val_str = str(value)
    if len(val_str) <= 4:
        return "****"
    return f"{val_str[:2]}{'*' * (len(val_str) - 4)}{val_str[-2:]}"

def get_boolean_env(key: str, default: bool = False) -> bool:
    """Safely parse boolean environment variables."""
    val = os.getenv(key, str(default)).lower()
    return val in ("true", "1", "yes", "y", "t")
