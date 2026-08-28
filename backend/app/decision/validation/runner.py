"""Validation Framework Runner."""
from typing import List
import time
from app.decision.validation.registry import ScenarioRegistry
from app.decision.validation.simulator import SimulationRunner
from app.decision.validation.validator import ScenarioValidator
from app.decision.validation.report import ValidationReport
from app.decision.validation.metrics import ValidationMetrics
from app.core.logger import get_logger

logger = get_logger(__name__)

class ValidationFramework:
    @staticmethod
    async def run_all() -> ValidationReport:
        logger.info("Validation Framework Started")
        
        scenarios = ScenarioRegistry.get_all()
        report = ValidationReport()
        metrics = ValidationMetrics(total_scenarios=len(scenarios))
        
        execution_times = []
        
        for scenario in scenarios:
            try:
                start = time.time()
                prediction = await SimulationRunner.run_scenario(scenario)
                ScenarioValidator.validate_scenario(scenario, prediction)
                
                execution_times.append(time.time() - start)
                report.passed_checks.append(scenario.name)
                metrics.passed_scenarios += 1
                logger.info(f"Scenario Passed: {scenario.name}")
            except Exception as e:
                report.failed_checks.append(f"{scenario.name}: {str(e)}")
                metrics.failed_scenarios += 1
                logger.error(f"Scenario Failed: {scenario.name} - {str(e)}")
                
        if execution_times:
            metrics.average_execution_time_ms = (sum(execution_times) / len(execution_times)) * 1000
            
        metrics.consistency_score = (metrics.passed_scenarios / max(1, metrics.total_scenarios)) * 100.0
        
        report.metrics = {
            "total_scenarios": metrics.total_scenarios,
            "success_rate": metrics.success_rate,
            "consistency_score": metrics.consistency_score,
            "avg_execution_ms": metrics.average_execution_time_ms
        }
        
        logger.info("Validation Framework Completed")
        return report
