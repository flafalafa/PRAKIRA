"""Decision State tracker."""
from enum import Enum
from typing import Dict, Any

class DecisionStatus(str, Enum):
    PENDING = "PENDING"
    EVALUATING = "EVALUATING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class EngineState:
    def __init__(self, context_id: str):
        self.context_id = context_id
        self.status = DecisionStatus.PENDING
        self.triggered_rules: list = []
        self.evidence: dict = {}
        self.missing_data: list = []
