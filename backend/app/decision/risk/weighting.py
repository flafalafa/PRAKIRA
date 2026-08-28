"""Risk Weighting Configuration."""
from typing import Dict, List
from app.core.logger import get_logger

logger = get_logger(__name__)

class WeightConfig:
    WEIGHTS = {
        "weather": 0.3,
        "hydrology": 0.4,
        "radar": 0.2,
        "historical": 0.1
    }

    @classmethod
    def get_weights(cls) -> Dict[str, float]:
        return cls.WEIGHTS
        
    @classmethod
    def normalize_weights(cls, active_factors: List[str]) -> Dict[str, float]:
        """Recalculate weights if some factors are missing."""
        total = sum(cls.WEIGHTS.get(f, 0.0) for f in active_factors)
        if total == 0:
            return {}
        return {f: cls.WEIGHTS.get(f, 0.0) / total for f in active_factors}
