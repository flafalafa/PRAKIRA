"""Main Flood Decision Engine."""
import uuid
from typing import Optional
from app.decision.context import DecisionContext
from app.decision.state import EngineState, DecisionStatus
from app.decision.executor import RuleExecutor
from app.decision.policy import PolicyEngine
from app.decision.result import DecisionResult, RiskLevel
from app.decision.explanation import DecisionExplanation
from app.decision.exceptions import InvalidDecisionContext
from app.core.logger import get_logger

logger = get_logger(__name__)

class FloodDecisionEngine:
    @staticmethod
    async def evaluate(context: DecisionContext) -> DecisionResult:
        decision_id = str(uuid.uuid4())
        logger.info(f"Decision Started: {decision_id} for context: {context.context_id}")
        
        state = EngineState(context_id=context.context_id)
        state.status = DecisionStatus.EVALUATING
        
        try:
            # 1. Validate Context
            if not context:
                raise InvalidDecisionContext("Context cannot be empty.")
            logger.debug("Context Validated")
            
            # 2. Execute Rules
            await RuleExecutor.execute_all(context, state)
            logger.debug(f"Rules Executed. Triggered: {len(state.triggered_rules)}")
            
            # 3. Aggregate Results
            intermediate = DecisionResult(
                decision_id=decision_id,
                status=DecisionStatus.COMPLETED,
                triggered_rules=state.triggered_rules,
                supporting_evidence=state.evidence
            )
            
            # 4. Apply Policies
            final_result = PolicyEngine.apply_policies(state, intermediate)
            
            # 5. Generate Explanation
            explanation = DecisionExplanation(
                reasons=[],
                supporting_data_refs=list(state.evidence.keys()),
                missing_data=state.missing_data,
                confidence_summary="Confidence calculated by rules."
            )
            final_result.explanation = explanation
            
            logger.info(f"Decision Completed: {decision_id}")
            return final_result
            
        except Exception as e:
            logger.error(f"Decision Failed: {decision_id}. Reason: {str(e)}")
            return DecisionResult(
                decision_id=decision_id,
                status=DecisionStatus.FAILED
            )
