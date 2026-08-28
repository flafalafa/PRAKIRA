"""Central API v1 Router."""
from fastapi import APIRouter
from app.api.v1.routers import health, system, areas, predictions, notifications, flood_status, alerts

api_v1_router = APIRouter()

api_v1_router.include_router(health.router)
api_v1_router.include_router(system.router)
api_v1_router.include_router(areas.router)
api_v1_router.include_router(flood_status.router, prefix="/areas")
api_v1_router.include_router(predictions.router)
api_v1_router.include_router(notifications.router)
api_v1_router.include_router(alerts.router)
api_v1_router.include_router(alerts.area_alerts_router, prefix="/areas")
api_v1_router.include_router(notifications.area_notifications_router, prefix="/areas")
