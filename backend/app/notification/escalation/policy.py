"""Escalation Policy Settings."""
from pydantic import BaseModel

class EscalationPolicyConfig(BaseModel):
    duplicate_window_minutes: int = 15
    escalation_window_minutes: int = 60
    confidence_delta_threshold: float = 0.2
    eta_delta_minutes: int = 15
    merge_strategy: str = "LATEST_WINS"
    emergency_override_enabled: bool = True
