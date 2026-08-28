"""Core Simulator Engine."""
from typing import Dict, Any
from app.notification.validation.scenario import BaseScenario
from app.notification.validation.validator import ResultValidator
from app.notification.validation.report import ScenarioResult
from app.core.logger import get_logger

logger = get_logger(__name__)

class Simulator:
    @staticmethod
    async def run_scenario(scenario: BaseScenario) -> ScenarioResult:
        logger.info(f"Simulating scenario: {scenario.context.name}")
        
        try:
            await scenario.setup()
            result_data = await scenario.execute()
            
            passed, errors = ResultValidator.validate(scenario.context, result_data)
            
            return ScenarioResult(
                scenario_name=scenario.context.name,
                passed=passed,
                details=result_data,
                errors=errors
            )
        except Exception as e:
            logger.error(f"Simulation failed for {scenario.context.name}: {str(e)}")
            return ScenarioResult(
                scenario_name=scenario.context.name,
                passed=False,
                errors=[f"Execution exception: {str(e)}"]
            )
        finally:
            await scenario.teardown()
