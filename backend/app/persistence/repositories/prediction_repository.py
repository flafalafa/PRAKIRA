"""SQL Prediction Repository."""
from typing import Optional, List
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.domain.entities.flood_prediction import FloodPrediction, RiskLevel, PredictionStatus
from app.domain.interfaces.prediction_repository import IPredictionRepository
from app.persistence.models.prediction import FloodPredictionModel
from app.persistence.mappers.prediction_mapper import PredictionPersistenceMapper
from app.repositories.generic import GenericRepository
from app.repositories.exceptions import RepositoryError

class SQLPredictionRepository(GenericRepository, IPredictionRepository):
    """PostgreSQL implementation of IPredictionRepository."""
    
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, FloodPredictionModel)
        
    async def save(self, prediction: FloodPrediction) -> FloodPrediction:
        self.logger.debug(f"Saving prediction {prediction.id}")
        model = PredictionPersistenceMapper.to_model(prediction)
        try:
            merged = await self.session.merge(model)
            await self.session.flush()
            return PredictionPersistenceMapper.to_domain(merged)
        except SQLAlchemyError as e:
            self.logger.error(f"Error saving prediction: {e}")
            raise RepositoryError(f"Error saving prediction: {e}")

    async def find_by_id(self, id: str) -> Optional[FloodPrediction]:
        stmt = select(FloodPredictionModel).where(FloodPredictionModel.id == id)
        result = await self.session.execute(stmt)
        model = result.scalars().first()
        if model:
            return PredictionPersistenceMapper.to_domain(model)
        return None

    async def find_latest(self, area_id: str) -> Optional[FloodPrediction]:
        # "newest valid prediction for the area"
        # ordering by prediction_time DESC.
        stmt = select(FloodPredictionModel).where(
            FloodPredictionModel.area_id == area_id,
            FloodPredictionModel.status.in_([PredictionStatus.VALIDATED, PredictionStatus.GENERATED, PredictionStatus.DRAFT])
        ).order_by(FloodPredictionModel.prediction_time.desc()).limit(1)
        
        result = await self.session.execute(stmt)
        model = result.scalars().first()
        if model:
            return PredictionPersistenceMapper.to_domain(model)
        return None

    async def find_by_area(self, area_id: str) -> List[FloodPrediction]:
        stmt = select(FloodPredictionModel).where(FloodPredictionModel.area_id == area_id)
        result = await self.session.execute(stmt)
        return [PredictionPersistenceMapper.to_domain(m) for m in result.scalars().all()]

    async def find_active(self) -> List[FloodPrediction]:
        # Active means VALIDATED or GENERATED (not EXPIRED/CANCELLED)
        stmt = select(FloodPredictionModel).where(
            FloodPredictionModel.status.in_([PredictionStatus.VALIDATED, PredictionStatus.GENERATED])
        )
        result = await self.session.execute(stmt)
        return [PredictionPersistenceMapper.to_domain(m) for m in result.scalars().all()]

    async def find_by_risk_level(self, risk_level: str) -> List[FloodPrediction]:
        stmt = select(FloodPredictionModel).where(FloodPredictionModel.risk_level == risk_level)
        result = await self.session.execute(stmt)
        return [PredictionPersistenceMapper.to_domain(m) for m in result.scalars().all()]

    async def find_critical(self) -> List[FloodPrediction]:
        # HIGH, VERY_HIGH, EXTREME based on domain entity `is_critical` logic
        stmt = select(FloodPredictionModel).where(
            FloodPredictionModel.risk_level.in_([RiskLevel.HIGH, RiskLevel.VERY_HIGH, RiskLevel.EXTREME]),
            FloodPredictionModel.status.in_([PredictionStatus.VALIDATED, PredictionStatus.GENERATED])
        )
        result = await self.session.execute(stmt)
        return [PredictionPersistenceMapper.to_domain(m) for m in result.scalars().all()]

    async def find_by_time_range(self, start_time: datetime, end_time: datetime) -> List[FloodPrediction]:
        stmt = select(FloodPredictionModel).where(
            FloodPredictionModel.prediction_time >= start_time,
            FloodPredictionModel.prediction_time <= end_time
        )
        result = await self.session.execute(stmt)
        return [PredictionPersistenceMapper.to_domain(m) for m in result.scalars().all()]

    async def exists(self, id: str) -> bool:
        stmt = select(FloodPredictionModel.id).where(FloodPredictionModel.id == id)
        result = await self.session.execute(stmt)
        return result.scalars().first() is not None

    async def list(self) -> List[FloodPrediction]:
        stmt = select(FloodPredictionModel)
        result = await self.session.execute(stmt)
        return [PredictionPersistenceMapper.to_domain(m) for m in result.scalars().all()]

    async def soft_delete(self, id: str) -> None:
        # Since FloodPredictionModel does not contain `is_deleted` or `deleted_at`,
        # soft deletion maps to cancelling the prediction (status = CANCELLED)
        stmt = select(FloodPredictionModel).where(FloodPredictionModel.id == id)
        result = await self.session.execute(stmt)
        model = result.scalars().first()
        if model:
            model.status = PredictionStatus.CANCELLED
            await self.session.flush()
