"""Prediction Dependencies."""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.interfaces.prediction_repository import IPredictionRepository as PredictionRepository
from app.persistence.repositories.prediction_repository import SQLPredictionRepository
from app.api.v1.services.prediction_service import PredictionApplicationService
from app.persistence.dependency import get_session_dependency

def get_prediction_repository(session: AsyncSession = Depends(get_session_dependency)) -> PredictionRepository:
    return SQLPredictionRepository(session)

def get_prediction_service(repository: PredictionRepository = Depends(get_prediction_repository)) -> PredictionApplicationService:
    return PredictionApplicationService(repository)
