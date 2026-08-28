"""Validation Metrics."""
from pydantic import BaseModel
from typing import Dict, Any

class ValidationMetrics(BaseModel):
    total_scenarios: int = 0
    passed_scenarios: int = 0
    failed_scenarios: int = 0
    notification_success_rate: float = 0.0
    suppression_rate: float = 0.0
    escalation_rate: float = 0.0
    average_latency_ms: float = 0.0
    validation_score: float = 0.0
    
    def calculate_score(self) -> None:
        if self.total_scenarios > 0:
            self.validation_score = (self.passed_scenarios / self.total_scenarios) * 100
