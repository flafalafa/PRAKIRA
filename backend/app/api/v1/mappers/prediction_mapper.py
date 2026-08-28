"""Prediction Mappers."""
from app.domain.entities.flood_prediction import FloodPrediction as Prediction
from app.api.v1.schemas.prediction import PredictionResponse, PredictionSummaryResponse, PredictionExplanation
from app.api.v1.schemas.flood_status import FloodStatusResponse

class PredictionMapper:
    @staticmethod
    def to_response(prediction: Prediction) -> PredictionResponse:
        explanation = None
        # explanation is not natively inside FloodPrediction but keep fallback just in case
        if hasattr(prediction, "explanation") and prediction.explanation:
            explanation = PredictionExplanation(
                primary_risk_factors=prediction.explanation.get("primary_risk_factors", []),
                supporting_observations=prediction.explanation.get("supporting_observations", []),
                triggered_rules=prediction.explanation.get("triggered_rules", []),
                confidence_explanation=prediction.explanation.get("confidence_explanation", ""),
                missing_data=prediction.explanation.get("missing_data", []),
                reason_summary=prediction.explanation.get("reason_summary", "")
            )
            
        return PredictionResponse(
            prediction_id=prediction.id,
            area_id=prediction.area_id,
            prediction_time=prediction.prediction_time.value,
            risk_score=prediction.risk_score.value,
            risk_level=prediction.risk_level.value,
            confidence=prediction.confidence_score.value,
            prediction_status=prediction.status.value,
            estimated_arrival_time=prediction.estimated_arrival_time.value if getattr(prediction, "estimated_arrival_time", None) else None,
            estimated_flood_depth=prediction.estimated_flood_depth.value if getattr(prediction, "estimated_flood_depth", None) else None,
            estimated_duration=int(prediction.expected_duration.value) if getattr(prediction, "expected_duration", None) else None,
            recommendation=getattr(prediction, "recommended_action", None),
            explanation=explanation,
            supporting_factors=getattr(prediction, "supporting_factors", {}),
            prediction_version=getattr(prediction, "version", "1.0"),
            created_at=prediction.created_at.value
        )

    @staticmethod
    def to_summary_response(prediction: Prediction) -> PredictionSummaryResponse:
        return PredictionSummaryResponse(
            prediction_id=prediction.id,
            area_id=prediction.area_id,
            prediction_time=prediction.prediction_time.value,
            risk_score=prediction.risk_score.value,
            risk_level=prediction.risk_level.value,
            prediction_status=prediction.status.value,
            created_at=prediction.created_at.value
        )

    @staticmethod
    def to_flood_status(prediction: Prediction, area_name: str) -> FloodStatusResponse:
        return FloodStatusResponse(
            area_id=prediction.area_id,
            area_name=area_name,
            current_risk_level=prediction.risk_level.value,
            risk_score=prediction.risk_score.value,
            confidence=prediction.confidence_score.value,
            prediction_status=prediction.status.value,
            last_updated=prediction.updated_at.value,
            prediction_timestamp=prediction.prediction_time.value,
            estimated_arrival_time=prediction.estimated_arrival_time.value if getattr(prediction, "estimated_arrival_time", None) else None,
            primary_risk_factor=prediction.explanation.get("primary_risk_factors", [None])[0] if hasattr(prediction, "explanation") and prediction.explanation else None,
            recommended_action=getattr(prediction, "recommended_action", None)
        )
