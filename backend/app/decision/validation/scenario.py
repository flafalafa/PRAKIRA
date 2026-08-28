"""Validation Scenarios."""
from dataclasses import dataclass, field
from typing import Dict, Any, List
from app.decision.orchestrator.context import OrchestratorContext

@dataclass
class ValidationScenario:
    name: str
    description: str
    context: OrchestratorContext
    expected_status: str
    expected_recommendations: List[str] = field(default_factory=list)
