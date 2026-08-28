import pytest
from datetime import datetime, timezone
from app.domain.entities.prediction import Prediction, RiskLevel, PredictionStatus
from app.api.v1.mappers.prediction_mapper import PredictionMapper

def test_prediction_mapper_to_response():
    now = datetime.now(timezone.utc)
    pred = Prediction(
        id="pred_123",
        area_id="area_123",
        timestamp=now,
        risk_score=75.5,
        risk_level=RiskLevel.WARNING,
        confidence=0.85,
        status=PredictionStatus.VALIDATED,
        created_at=now
    )
    
    resp = PredictionMapper.to_response(pred)
    assert resp.prediction_id == "pred_123"
    assert resp.risk_level == "WARNING"
    assert resp.risk_score == 75.5
    assert resp.confidence == 0.85
    assert resp.prediction_status == "VALIDATED"
    assert resp.explanation is None

def test_prediction_mapper_to_summary():
    now = datetime.now(timezone.utc)
    pred = Prediction(
        id="pred_123",
        area_id="area_123",
        timestamp=now,
        risk_score=90.0,
        risk_level=RiskLevel.DANGER,
        confidence=0.90,
        status=PredictionStatus.VALIDATED,
        created_at=now
    )
    
    resp = PredictionMapper.to_summary_response(pred)
    assert resp.prediction_id == "pred_123"
    assert resp.risk_level == "DANGER"
    assert not hasattr(resp, "explanation")

def test_prediction_mapper_to_flood_status():
    now = datetime.now(timezone.utc)
    pred = Prediction(
        id="pred_123",
        area_id="area_123",
        timestamp=now,
        risk_score=45.0,
        risk_level=RiskLevel.WATCH,
        confidence=0.70,
        status=PredictionStatus.VALIDATED,
        created_at=now
    )
    
    resp = PredictionMapper.to_flood_status(pred, "Pondok Kacang")
    assert resp.area_id == "area_123"
    assert resp.area_name == "Pondok Kacang"
    assert resp.current_risk_level == "WATCH"
