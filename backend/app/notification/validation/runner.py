"""Validation Runner."""
from typing import List
from app.notification.validation.simulator import Simulator
from app.notification.validation.registry import ScenarioRegistry
from app.notification.validation.report import ValidationReport
from app.notification.validation.metrics import ValidationMetrics
from app.notification.validation.scenario import WatchNotificationScenario, EmergencyOverrideScenario
from app.core.logger import get_logger

logger = get_logger(__name__)

# Register default scenarios
ScenarioRegistry.register(WatchNotificationScenario())
ScenarioRegistry.register(EmergencyOverrideScenario())

class ValidationRunner:
    @staticmethod
    async def run_all() -> ValidationReport:
        logger.info("Starting End-to-End Notification Validation")
        scenarios = ScenarioRegistry.get_all()
        report = ValidationReport()
        metrics = ValidationMetrics(total_scenarios=len(scenarios))
        
        latencies = []
        
        for scenario in scenarios:
            result = await Simulator.run_scenario(scenario)
            report.results.append(result)
            
            if result.passed:
                metrics.passed_scenarios += 1
            else:
                metrics.failed_scenarios += 1
                
            latency = result.details.get("latency", 0)
            if latency:
                latencies.append(latency)
                
        if latencies:
            metrics.average_latency_ms = sum(latencies) / len(latencies)
            
        metrics.calculate_score()
        report.metrics = metrics
        
        if metrics.validation_score < 100:
            report.warnings.append("Some scenarios failed validation")
            
        logger.info(report.generate_summary())
        return report
