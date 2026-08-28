import asyncio
from datetime import datetime, timezone
from app.config.settings import settings
from app.persistence.engine import engine_manager
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.flood_prediction import FloodPrediction, RiskClassificationPolicy, PredictionStatus, RiskLevel
from app.domain.value_objects.core import TimestampUTC, Duration
from app.domain.value_objects.analysis import RiskScore, PredictionConfidence
from app.domain.value_objects.hydrology import WaterLevel
from app.persistence.repositories.prediction_repository import SQLPredictionRepository

async def run_test():
    engine = engine_manager.get_engine()
    
    SessionLocal = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    
    policy = RiskClassificationPolicy()
    
    # Create test prediction
    test_prediction = FloodPrediction.generate(
        prediction_code="TEST-PRED-123",
        area_id="test-area-1",
        prediction_time=TimestampUTC(value=datetime.now(timezone.utc)),
        forecast_start=TimestampUTC(value=datetime.now(timezone.utc)),
        forecast_end=TimestampUTC(value=datetime.now(timezone.utc)),
        prediction_source="Test Source",
        prediction_method="Test Method",
        risk_score=RiskScore(value=85.0), # VERY_HIGH
        confidence_score=PredictionConfidence(value=0.9),
        flood_probability=0.8,
        estimated_flood_depth=WaterLevel(value=1.5),
        expected_duration=Duration(value=3600),
        recommended_action="Evacuate TEST",
        policy=policy
    )
    # validate it to make it ACTIVE and CRITICAL
    test_prediction = test_prediction.validate()
    print("Test Prediction Risk Level:", test_prediction.risk_level.value)
    
    async with SessionLocal() as session:
        repo = SQLPredictionRepository(session)
        try:
            print("1. Save one FloodPrediction")
            saved = await repo.save(test_prediction)
            await session.commit()
            print("   -> Saved ID:", saved.id)
            
            print("2. Find by ID")
            found = await repo.find_by_id(test_prediction.id)
            print("   -> Found ID:", found.id if found else None)
            
            print("3. Find latest prediction for area")
            latest = await repo.find_latest("test-area-1")
            print("   -> Latest ID:", latest.id if latest else None)
            
            print("4. Find predictions by area")
            by_area = await repo.find_by_area("test-area-1")
            print("   -> Count:", len(by_area))
            
            print("5. Find by risk level")
            by_risk = await repo.find_by_risk_level(RiskLevel.VERY_HIGH)
            print("   -> Count VERY_HIGH:", len(by_risk))
            
            print("6. Check exists")
            does_exist = await repo.exists(test_prediction.id)
            print("   -> Exists:", does_exist)
            
            print("7. List predictions")
            all_preds = await repo.list()
            print("   -> Total Count:", len(all_preds))
            
            print("8. Find critical predictions")
            criticals = await repo.find_critical()
            print("   -> Critical Count:", len(criticals))
            
            print("9. Soft delete")
            await repo.soft_delete(test_prediction.id)
            await session.commit()
            print("   -> Deleted.")
            
            print("10. Confirm deleted records behave according to project conventions")
            deleted = await repo.find_by_id(test_prediction.id)
            print("   -> Found after soft delete status:", deleted.status.value if deleted else None)
            
            active = await repo.find_active()
            active_ids = [p.id for p in active]
            print("   -> In active list?", test_prediction.id in active_ids)
            
            # Clean up test data entirely
            print("11. Clean up test records")
            from sqlalchemy import text
            await session.execute(text(f"DELETE FROM flood_predictions WHERE id = '{test_prediction.id}'"))
            await session.commit()
            print("   -> Cleanup completed.")
            
        except Exception as e:
            await session.rollback()
            print("Error:", e)

if __name__ == "__main__":
    asyncio.run(run_test())
