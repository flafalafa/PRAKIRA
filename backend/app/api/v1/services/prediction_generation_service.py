import uuid
from typing import List
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.collectors.providers.bmkg.collector import BMKGCollector
from app.pipeline.pipeline import EnterprisePipeline
from app.pipeline.canonical import CanonicalRecord
from app.decision.orchestrator.context import OrchestratorContext
from app.decision.orchestrator.workflow import DecisionWorkflow
from app.decision.orchestrator.state import WorkflowState
from app.prediction.generator import PredictionGenerator
from app.domain.entities.flood_prediction import FloodPrediction, RiskClassificationPolicy
from app.domain.value_objects.core import TimestampUTC, Duration
from app.domain.value_objects.hydrology import WaterLevel
from app.domain.value_objects.analysis import PredictionConfidence, RiskScore
from app.persistence.repositories.prediction_repository import SQLPredictionRepository
from app.core.logger import get_logger
from app.prediction.exceptions import PredictionGenerationFailure

logger = get_logger(__name__)

class PredictionGenerationService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = SQLPredictionRepository(session)
        self.policy = RiskClassificationPolicy()
        
    async def generate_prediction_for_area(self, area_id: str) -> FloodPrediction:
        logger.info(f"Generating manual prediction for area: {area_id}")
        
        # Step 2: Fetch Real BMKG Data
        collector = BMKGCollector()
        try:
            await collector.connect()
            raw_payload = await collector.fetch(area_id=area_id)
        except Exception as e:
            logger.error(f"Failed to fetch BMKG data: {e}")
            raise PredictionGenerationFailure(f"BMKG fetch failed: {e}") from e
        finally:
            await collector.disconnect()
            
        # Step 3: Normalize / Run Enterprise Pipeline
        try:
            parsed_data = await collector.parse(raw_payload)
            normalized_data = await collector.normalize(parsed_data)
            await collector.validate(normalized_data)
            
            canonical_records: List[CanonicalRecord] = EnterprisePipeline.process(
                raw_dto=normalized_data,
                provider_id="BMKG"
            )
        except Exception as e:
            logger.error(f"Enterprise Pipeline failed: {e}")
            raise PredictionGenerationFailure(f"Pipeline failed: {e}") from e
            
        if not canonical_records:
            raise PredictionGenerationFailure("Pipeline produced no CanonicalRecords.")
            
        # Step 4: Build Orchestrator Context
        weather_observations = []
        rainfall_observations = []
        
        for record in canonical_records:
            # BMKG transformer now emits canonical names ('rainfall', not 'tp').
            w_meas = [m for m in record.measurements if m.parameter != 'rainfall']
            r_meas = [m for m in record.measurements if m.parameter == 'rainfall']
            
            if w_meas:
                weather_record = record.model_copy(update={'measurements': w_meas})
                weather_observations.append(weather_record)
            if r_meas:
                rainfall_record = record.model_copy(update={'measurements': r_meas})
                rainfall_observations.append(rainfall_record)
                
        workflow_id = str(uuid.uuid4())
        context = OrchestratorContext(
            workflow_id=workflow_id,
            weather_observations=weather_observations,
            rainfall_observations=rainfall_observations,
            river_observations=[],
            radar_observations=[],
            area_metadata={"area_id": area_id},
            historical_metadata={}
        )
        
        # Step 5: Execute Decision Workflow
        orchestrator_result = await DecisionWorkflow.execute(context)
        
        if orchestrator_result.state == WorkflowState.FAILED:
            errors = ", ".join(orchestrator_result.errors)
            raise PredictionGenerationFailure(f"DecisionWorkflow FAILED: {errors}")
            
        # Step 6: Generate Prediction Result
        try:
            prediction_result = PredictionGenerator.generate(orchestrator_result)
        except Exception as e:
            logger.error(f"PredictionGenerator failed: {e}")
            raise PredictionGenerationFailure(f"PredictionGenerator failed: {e}") from e
            
        # Step 7: Resolve Forecast Time Window
        timestamps = [r.timestamp for r in canonical_records]
        min_ts = TimestampUTC(value=min(timestamps))
        max_ts = TimestampUTC(value=max(timestamps))
        
        # Step 8: Map to FloodPrediction Domain Entity
        pred_time = TimestampUTC(value=prediction_result.prediction_time)
        
        flood_depth = WaterLevel(value=prediction_result.estimated_flood_depth) if prediction_result.estimated_flood_depth is not None else None
        duration = Duration(value=prediction_result.estimated_duration) if prediction_result.estimated_duration is not None else None
        eat = TimestampUTC(value=datetime.fromtimestamp(prediction_result.estimated_arrival_time, tz=timezone.utc)) if prediction_result.estimated_arrival_time is not None else None
        
        domain_prediction = FloodPrediction.generate(
            prediction_code=prediction_result.prediction_code,
            area_id=area_id,
            prediction_time=pred_time,
            forecast_start=min_ts,
            forecast_end=max_ts,
            prediction_source="BMKG",
            prediction_method="DecisionWorkflow",
            risk_score=RiskScore(value=prediction_result.risk_score),
            confidence_score=PredictionConfidence(value=prediction_result.confidence),
            recommended_action=prediction_result.recommendation,
            policy=self.policy,
            flood_probability=None,
            estimated_flood_depth=flood_depth,
            expected_duration=duration,
            river_id=None,
            estimated_arrival_time=eat,
            rainfall_reference=None,
            river_reference=None,
            weather_reference=None
        )
        
        # Explanation mapping based on how FloodPrediction handles it
        # Actually `explanation` isn't in FloodPrediction constructor, it's usually not mapped directly, 
        # or it is stored in `supporting_factors` or similar if needed. Wait, in the audit we saw:
        # `explanation` is not natively inside FloodPrediction but keep fallback just in case...
        # So I don't need to explicitly assign it unless required.
        
        # Step 9: Persist to PostgreSQL
        try:
            saved_prediction = await self.repository.save(domain_prediction)
            await self.session.commit()
            logger.info(f"Successfully generated and persisted prediction: {saved_prediction.id}")
            return saved_prediction
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Persistence failed: {e}")
            raise PredictionGenerationFailure(f"Persistence failed: {e}") from e
