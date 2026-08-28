import asyncio
from datetime import datetime, timezone
import uuid
from app.persistence.manager import transaction_manager
from app.persistence.repositories.prediction_repository import SQLPredictionRepository
from app.domain.entities.flood_prediction import FloodPrediction, RiskLevel, PredictionStatus
from app.domain.value_objects.hydrology import WaterLevel
from app.domain.value_objects.analysis import PredictionConfidence, RiskScore
from app.domain.value_objects.core import TimestampUTC, Duration

async def seed_test_prediction():
    async with transaction_manager.session() as session:
        repo = SQLPredictionRepository(session)
        
        # Check if already exists for area-1
        existing = await repo.find_latest("area-1")
        if existing:
            print("Test prediction for area-1 already exists.")
            return

        now = datetime.now(timezone.utc)
        
        prediction = FloodPrediction(
            id=str(uuid.uuid4()),
            prediction_code="PRED-TEST-AREA-1",
            area_id="area-1",
            river_id=None,
            prediction_time=TimestampUTC(value=now),
            forecast_start=TimestampUTC(value=now),
            forecast_end=TimestampUTC(value=now),
            prediction_source="Development Test",
            prediction_method="Static Seed",
            risk_score=RiskScore(value=85.0),
            confidence_score=PredictionConfidence(value=0.90),
            flood_probability=0.85,
            estimated_flood_depth=WaterLevel(value=1.5),
            estimated_arrival_time=None,
            expected_duration=Duration(value=3600),
            rainfall_reference=None,
            river_reference=None,
            weather_reference=None,
            recommended_action="Evacuate to higher ground.",
            risk_level=RiskLevel.HIGH,
            status=PredictionStatus.VALIDATED
        )
        
        saved = await repo.save(prediction)
        await session.commit()
        print(f"Successfully seeded test prediction {saved.id} for area-1")

if __name__ == "__main__":
    asyncio.run(seed_test_prediction())
