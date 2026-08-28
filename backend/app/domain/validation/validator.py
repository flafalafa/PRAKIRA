"""Central Validator executing policies and rules."""
from typing import Any, List
from app.domain.validation.base import ValidationResult
from app.domain.validation.context import ValidationContext
from app.domain.validation.policies import BaseDomainPolicy
from app.core.logger import get_logger
from app.domain.validation.exceptions import PolicyViolationError

logger = get_logger(__name__)

class DomainValidator:
    """Executes a chain of policies against an entity and its context."""
    
    def __init__(self, policies: List[BaseDomainPolicy], rules: List[callable] = None):
        self.policies = policies
        self.rules = rules or []
        
    def validate(self, entity: Any, context: ValidationContext, raise_on_error: bool = False) -> ValidationResult:
        entity_name = type(entity).__name__
        logger.info(f"Validation Started for {entity_name}")
        
        final_result = ValidationResult()
        
        # Execute atomic rules
        for rule in self.rules:
            res = rule(entity, context)
            final_result.merge(res)
            
        # Execute complex policies
        for policy in self.policies:
            res = policy.evaluate(entity, context)
            final_result.merge(res)
            if not res.is_valid:
                logger.warning(f"Policy Violation for {entity_name}: {res.messages}")
                
        # Handle results
        if not final_result.is_valid:
            error_count = len([m for m in final_result.messages if m.level.value == 'ERROR'])
            logger.error(f"Validation Failure for {entity_name}. Errors: {error_count}")
            if raise_on_error:
                raise PolicyViolationError(f"Validation failed for {entity_name}. Result: {final_result.model_dump_json()}")
        else:
            logger.info(f"Validation Success for {entity_name}")
            
        return final_result
