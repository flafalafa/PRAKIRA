"""Business Policies applied after rules."""
from typing import List
from app.decision.result import DecisionResult
from app.decision.state import EngineState

class PolicyEngine:
    @staticmethod
    def apply_policies(state: EngineState, intermediate_result: DecisionResult) -> DecisionResult:
        """
        Applies overarching business policies.
        For example: "If missing data > X, cap confidence at Y."
        """
        if state.missing_data:
            intermediate_result.confidence = min(intermediate_result.confidence, 0.5)
            
        return intermediate_result
