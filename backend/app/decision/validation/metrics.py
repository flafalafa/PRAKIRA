"""Validation Metrics."""
from dataclasses import dataclass
from typing import List

@dataclass
class ValidationMetrics:
    total_scenarios: int = 0
    passed_scenarios: int = 0
    failed_scenarios: int = 0
    average_execution_time_ms: float = 0.0
    consistency_score: float = 0.0
    
    @property
    def success_rate(self) -> float:
        if self.total_scenarios == 0:
            return 0.0
        return (self.passed_scenarios / self.total_scenarios) * 100.0
