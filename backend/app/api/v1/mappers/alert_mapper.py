"""Alert Mapper."""
from typing import Dict, Any
from app.api.v1.schemas.alert import AlertResponse, AlertDetailResponse, AlertExplanation
# Note: Since the exact Alert domain entity might vary, we map from a generic dict/object representing the alert
# In a real implementation, this maps from app.domain.entities.alert.Alert

class AlertMapper:
    @staticmethod
    def to_response(alert: Any) -> AlertResponse:
        return AlertResponse(
            alert_id=getattr(alert, "id", "UNKNOWN"),
            area_id=getattr(alert, "area_id", "UNKNOWN"),
            alert_level=getattr(alert, "level", "UNKNOWN"),
            risk_score=getattr(alert, "risk_score", 0.0),
            confidence=getattr(alert, "confidence", None),
            prediction_id=getattr(alert, "prediction_id", "UNKNOWN"),
            title=getattr(alert, "title", ""),
            message=getattr(alert, "message", ""),
            recommendation=getattr(alert, "recommendation", None),
            issued_at=getattr(alert, "issued_at", None),
            updated_at=getattr(alert, "updated_at", None),
            expires_at=getattr(alert, "expires_at", None),
            estimated_arrival_time=getattr(alert, "estimated_arrival_time", None),
            alert_status=getattr(alert, "status", "UNKNOWN")
        )

    @staticmethod
    def to_detail_response(alert: Any) -> AlertDetailResponse:
        explanation_data = getattr(alert, "explanation", {})
        explanation = AlertExplanation(
            primary_risk_factors=explanation_data.get("primary_risk_factors", []),
            supporting_observations=explanation_data.get("supporting_observations", []),
            triggered_rules=explanation_data.get("triggered_rules", []),
            confidence_explanation=explanation_data.get("confidence_explanation", ""),
            missing_data=explanation_data.get("missing_data", [])
        )
        
        return AlertDetailResponse(
            alert_id=getattr(alert, "id", "UNKNOWN"),
            area_id=getattr(alert, "area_id", "UNKNOWN"),
            alert_level=getattr(alert, "level", "UNKNOWN"),
            risk_score=getattr(alert, "risk_score", 0.0),
            confidence=getattr(alert, "confidence", None),
            prediction_id=getattr(alert, "prediction_id", "UNKNOWN"),
            title=getattr(alert, "title", ""),
            message=getattr(alert, "message", ""),
            recommendation=getattr(alert, "recommendation", None),
            issued_at=getattr(alert, "issued_at", None),
            updated_at=getattr(alert, "updated_at", None),
            expires_at=getattr(alert, "expires_at", None),
            estimated_arrival_time=getattr(alert, "estimated_arrival_time", None),
            alert_status=getattr(alert, "status", "UNKNOWN"),
            explanation=explanation
        )
