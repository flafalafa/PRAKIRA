"""Scoring Engine."""
from typing import Dict, Any, Tuple, List
from app.decision.risk.weighting import WeightConfig

class ScoringEngine:
    @staticmethod
    def calculate_sub_scores(factors: Dict[str, Any]) -> Dict[str, float]:
        """Converts raw factors to 0-100 scores."""
        scores = {}
        rain = factors.get("rainfall_intensity")
        scores["weather"] = min(100.0, rain * 5) if rain is not None else None
        
        river = factors.get("river_capacity_usage")
        scores["hydrology"] = min(100.0, river) if river is not None else None
        
        radar_conf = factors.get("radar_confidence", 0.0)
        if radar_conf == 0.0:
            scores["radar"] = None
        else:
            eta = factors.get("storm_eta")
            scores["radar"] = 100.0 if eta is not None and eta <= 30 else 0.0
        
        scores["historical"] = factors.get("historical_susceptibility", 0.0)
        return scores

    @staticmethod
    def calculate_overall_risk(sub_scores: Dict[str, float]) -> Tuple[float, Dict[str, float]]:
        active = [k for k, v in sub_scores.items() if v is not None]
        weights = WeightConfig.normalize_weights(active)
        
        overall = 0.0
        contributions = {}
        for factor, weight in weights.items():
            contrib = sub_scores.get(factor, 0.0) * weight
            contributions[factor] = contrib
            overall += contrib
            
        return overall, contributions
