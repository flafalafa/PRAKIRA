"""Persistence mapper for FloodPrediction."""
from app.domain.entities.flood_prediction import FloodPrediction
from app.persistence.models.prediction import FloodPredictionModel
from app.domain.value_objects.core import TimestampUTC, Duration
from app.domain.value_objects.hydrology import WaterLevel
from app.domain.value_objects.analysis import PredictionConfidence, RiskScore
from datetime import timezone

class PredictionPersistenceMapper:
    @staticmethod
    def to_model(domain_entity: FloodPrediction) -> FloodPredictionModel:
        return FloodPredictionModel(
            id=domain_entity.id,
            prediction_code=domain_entity.prediction_code,
            area_id=domain_entity.area_id,
            river_id=domain_entity.river_id,
            prediction_time=domain_entity.prediction_time.value,
            forecast_start=domain_entity.forecast_start.value,
            forecast_end=domain_entity.forecast_end.value,
            prediction_source=domain_entity.prediction_source,
            prediction_method=domain_entity.prediction_method,
            risk_score=domain_entity.risk_score.value,
            confidence_score=domain_entity.confidence_score.value,
            flood_probability=domain_entity.flood_probability,
            estimated_flood_depth=domain_entity.estimated_flood_depth.value if domain_entity.estimated_flood_depth else None,
            estimated_arrival_time=domain_entity.estimated_arrival_time.value if domain_entity.estimated_arrival_time else None,
            expected_duration_seconds=domain_entity.expected_duration.value if domain_entity.expected_duration else None,
            rainfall_reference=domain_entity.rainfall_reference,
            river_reference=domain_entity.river_reference,
            weather_reference=domain_entity.weather_reference,
            recommended_action=domain_entity.recommended_action,
            risk_level=domain_entity.risk_level,
            status=domain_entity.status,
            created_at=domain_entity.created_at.value,
            updated_at=domain_entity.updated_at.value
        )

    @staticmethod
    def to_domain(model: FloodPredictionModel) -> FloodPrediction:
        # Convert naive datetimes to UTC if they are naive
        pt = model.prediction_time.replace(tzinfo=timezone.utc) if model.prediction_time.tzinfo is None else model.prediction_time
        fs = model.forecast_start.replace(tzinfo=timezone.utc) if model.forecast_start.tzinfo is None else model.forecast_start
        fe = model.forecast_end.replace(tzinfo=timezone.utc) if model.forecast_end.tzinfo is None else model.forecast_end
        eat = None
        if model.estimated_arrival_time:
            eat = model.estimated_arrival_time.replace(tzinfo=timezone.utc) if model.estimated_arrival_time.tzinfo is None else model.estimated_arrival_time
        ca = model.created_at.replace(tzinfo=timezone.utc) if model.created_at.tzinfo is None else model.created_at
        ua = model.updated_at.replace(tzinfo=timezone.utc) if model.updated_at.tzinfo is None else model.updated_at

        return FloodPrediction(
            id=str(model.id),
            prediction_code=model.prediction_code,
            area_id=model.area_id,
            river_id=model.river_id,
            prediction_time=TimestampUTC(value=pt),
            forecast_start=TimestampUTC(value=fs),
            forecast_end=TimestampUTC(value=fe),
            prediction_source=model.prediction_source,
            prediction_method=model.prediction_method,
            risk_score=RiskScore(value=model.risk_score),
            confidence_score=PredictionConfidence(value=model.confidence_score),
            flood_probability=model.flood_probability,
            estimated_flood_depth=WaterLevel(value=model.estimated_flood_depth) if model.estimated_flood_depth is not None else None,
            estimated_arrival_time=TimestampUTC(value=eat) if eat else None,
            expected_duration=Duration(value=model.expected_duration_seconds) if model.expected_duration_seconds is not None else None,
            rainfall_reference=model.rainfall_reference,
            river_reference=model.river_reference,
            weather_reference=model.weather_reference,
            recommended_action=model.recommended_action,
            risk_level=model.risk_level,
            status=model.status,
            created_at=TimestampUTC(value=ca),
            updated_at=TimestampUTC(value=ua)
        )
