"""Rule Executor."""
from app.decision.context import DecisionContext
from app.decision.state import EngineState
from app.decision.registry import RuleRegistry
from app.decision.exceptions import RuleExecutionFailure
from app.core.logger import get_logger

logger = get_logger(__name__)

class RuleExecutor:
    @staticmethod
    async def execute_all(context: DecisionContext, state: EngineState) -> None:
        rules = RuleRegistry.get_all_rules()
        for rule in rules:
            try:
                triggered = await rule.evaluate(context, state)
                if triggered:
                    state.triggered_rules.append(rule.name)
            except Exception as e:
                logger.error(f"Rule {rule.name} failed: {str(e)}")
                raise RuleExecutionFailure(f"Execution failed for {rule.name}")
