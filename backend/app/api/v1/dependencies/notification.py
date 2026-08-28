"""Notification & Alert Dependencies."""
from fastapi import Depends
from typing import Any
# Stub for repositories
class MockRepository:
    async def get_active_for_area(self, area_id: str) -> Any: pass
    async def get_by_id(self, id: str) -> Any: pass
    async def list_by_area(self, area_id: str) -> Any: return []
    async def list_by_area_and_user(self, area_id: str, user_id: str) -> Any: return []

from app.api.v1.services.alert_service import AlertApplicationService
from app.api.v1.services.notification_service import NotificationApplicationService

def get_alert_service() -> AlertApplicationService:
    return AlertApplicationService(MockRepository())

def get_notification_service() -> NotificationApplicationService:
    return NotificationApplicationService(MockRepository())
