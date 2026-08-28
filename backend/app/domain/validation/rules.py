"""Atomic validation rules."""
from app.domain.validation.base import ValidationResult
from app.domain.validation.context import ValidationContext

def check_prediction_confidence(prediction, context: ValidationContext) -> ValidationResult:
    result = ValidationResult()
    from app.domain.entities.flood_prediction import PredictionStatus
    if prediction.status == PredictionStatus.VALIDATED:
        # Business rule: Prediction cannot become VALIDATED if Confidence is too low (e.g., < 0.5)
        if prediction.confidence_score.value < 0.5:
            result.add_error("LOW_CONFIDENCE_VALIDATION", "Cannot validate prediction with confidence score < 0.5.")
    return result

def check_event_verification_dependency(event, context: ValidationContext) -> ValidationResult:
    result = ValidationResult()
    from app.domain.entities.flood_event import VerificationStatus
    # Business rule: FloodEvent cannot become VERIFIED before event exists.
    # While typically caught during DB insert, we can enforce it logically here.
    if event.verification_status != VerificationStatus.UNVERIFIED and not event.id:
        result.add_error("EARLY_VERIFICATION", "Cannot verify an unsaved/non-existent event.")
    return result
