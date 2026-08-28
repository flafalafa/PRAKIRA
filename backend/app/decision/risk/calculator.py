"""Risk Calculator Facade."""
from app.decision.risk.context import RiskContext
from app.decision.risk.aggregator import RiskAggregator
from app.decision.risk.scoring import ScoringEngine
from typing import Dict, Any

class RiskCalculator:
    @staticmethod
    def calculate(context: RiskContext) -> Dict[str, Any]:
        factors = RiskAggregator.aggregate_factors(context)
        sub_scores = ScoringEngine.calculate_sub_scores(factors)
        overall_score, contributions = ScoringEngine.calculate_overall_risk(sub_scores)
        
        return {
            "factors": factors,
            "overall_score": overall_score,
            "contributions": contributions
        }
