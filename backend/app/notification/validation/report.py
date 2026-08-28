"""Validation Report Builder."""
from typing import List, Dict, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from app.notification.validation.metrics import ValidationMetrics

class ScenarioResult(BaseModel):
    scenario_name: str
    passed: bool
    details: Dict[str, Any] = Field(default_factory=dict)
    errors: List[str] = Field(default_factory=list)

class ValidationReport(BaseModel):
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metrics: ValidationMetrics = Field(default_factory=ValidationMetrics)
    results: List[ScenarioResult] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    
    def generate_summary(self) -> str:
        status = "PASSED" if self.metrics.validation_score == 100 else "FAILED"
        return f"Validation {status} - Score: {self.metrics.validation_score:.1f}% ({self.metrics.passed_scenarios}/{self.metrics.total_scenarios} passed)"
