"""Consistency Checker."""
from typing import Dict, Any, List
from app.notification.validation.scenario import ScenarioContext

class ConsistencyChecker:
    @staticmethod
    def verify(context: ScenarioContext, execution_result: Dict[str, Any]) -> List[str]:
        errors = []
        
        if execution_result.get("override_active"):
            if execution_result.get("priority") != "high":
                errors.append("Consistency Failure: Emergency override active but priority is not high")
                
        status = execution_result.get("status")
        if status not in ["DELIVERED", "SUPPRESSED", "FAILED"]:
            errors.append(f"Consistency Failure: Unknown final status '{status}'")
            
        return errors
