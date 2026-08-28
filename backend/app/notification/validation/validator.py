"""Result Validator."""
from typing import Dict, Any, List, Tuple
from app.notification.validation.scenario import ScenarioContext
from app.notification.validation.consistency import ConsistencyChecker

class ResultValidator:
    @staticmethod
    def validate(context: ScenarioContext, execution_result: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors = ConsistencyChecker.verify(context, execution_result)
        
        for expected in context.expected_outcomes:
            if expected == "DELIVERED" and execution_result.get("status") != "DELIVERED":
                errors.append(f"Expected outcome {expected} not met")
                
        passed = len(errors) == 0
        return passed, errors
