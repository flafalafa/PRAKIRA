"""FCM Client Mock."""
import uuid
import asyncio
from typing import Dict, Any
from app.core.logger import get_logger

logger = get_logger(__name__)

class FCMClient:
    async def send(self, payload: Dict[str, Any]) -> str:
        await asyncio.sleep(0.1)
        message_id = f"projects/mock/messages/{uuid.uuid4()}"
        logger.debug(f"FCM Client sent message: {message_id}")
        return message_id
