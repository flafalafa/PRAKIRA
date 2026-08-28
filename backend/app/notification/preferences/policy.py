"""Preferences Policy Configuration."""
from pydantic import BaseModel
from typing import List

class PreferencePolicyConfig(BaseModel):
    default_notifications_enabled: bool = True
    default_minimum_severity: str = "WATCH"
    emergency_override_enabled: bool = True
    supported_channels: List[str] = ["PUSH", "SMS"]
    default_quiet_hours_enabled: bool = False
