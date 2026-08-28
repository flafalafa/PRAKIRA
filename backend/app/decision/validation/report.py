"""Validation Report."""
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from app.decision.validation.metrics import ValidationMetrics

class ValidationReport(BaseModel):
    passed_checks: List[str] = Field(default_factory=list)
    failed_checks: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    metrics: Dict[str, Any] = Field(default_factory=dict)
