"""User Preference Profile."""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import time

class QuietHoursConfig(BaseModel):
    enabled: bool = False
    start_time: time = time(22, 0) # 22:00
    end_time: time = time(6, 0)    # 06:00
    timezone: str = "Asia/Jakarta"

class UserPreferenceProfile(BaseModel):
    user_id: str
    notifications_enabled: bool = True
    subscribed_areas: List[str] = Field(default_factory=list)
    minimum_severity: str = "WATCH"
    quiet_hours: QuietHoursConfig = Field(default_factory=QuietHoursConfig)
    preferred_channels: List[str] = Field(default_factory=lambda: ["PUSH"])
    categories: List[str] = Field(default_factory=lambda: ["FLOOD_WARNING"])
