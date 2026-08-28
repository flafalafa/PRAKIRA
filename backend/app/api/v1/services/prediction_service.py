"""Prediction Application Service."""
from typing import List, Tuple
from app.domain.entities.flood_prediction import FloodPrediction as Prediction
from app.domain.interfaces.prediction_repository import IPredictionRepository as PredictionRepository
from app.api.v1.schemas.prediction import PredictionHistoryFilterParams
from app.api.v1.schemas.pagination import PaginationMeta
from app.exceptions.not_found import NotFoundException

class PredictionApplicationService:
    def __init__(self, repository: PredictionRepository):
        self.repository = repository
        
    async def get_current_prediction(self, area_id: str) -> Prediction:
        prediction = await self.repository.find_latest(area_id)
        if not prediction:
            raise NotFoundException(f"No active prediction found for area {area_id}")
        return prediction
        
    async def get_prediction_by_id(self, prediction_id: str) -> Prediction:
        prediction = await self.repository.find_by_id(prediction_id)
        if not prediction:
            raise NotFoundException(f"Prediction {prediction_id} not found")
        return prediction
        
    async def list_prediction_history(self, area_id: str, filters: PredictionHistoryFilterParams) -> Tuple[List[Prediction], PaginationMeta]:
        # For stub purposes, assume repository has a `list_by_area` method
        predictions = await self.repository.find_by_area(area_id)
        
        # Apply filters
        if filters.risk_level:
            predictions = [p for p in predictions if p.risk_level.value == filters.risk_level]
        if filters.prediction_status:
            predictions = [p for p in predictions if p.status.value == filters.prediction_status]
        if filters.from_date:
            predictions = [p for p in predictions if p.prediction_time.value >= filters.from_date]
        if filters.to_date:
            predictions = [p for p in predictions if p.prediction_time.value <= filters.to_date]
            
        total = len(predictions)
        start = (filters.page - 1) * filters.page_size
        end = start + filters.page_size
        paginated_predictions = predictions[start:end]
        
        total_pages = max(1, (total + filters.page_size - 1) // filters.page_size)
        
        pagination = PaginationMeta(
            page=filters.page,
            page_size=filters.page_size,
            total=total,
            total_pages=total_pages,
            has_next=filters.page < total_pages,
            has_previous=filters.page > 1
        )
        
        return paginated_predictions, pagination
