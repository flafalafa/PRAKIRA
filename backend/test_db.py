import asyncio
from app.config.settings import settings
from app.persistence.engine import engine_manager

async def test():
    print('URI:', settings.db.uri.get_secret_value() if settings.db.uri else 'None')
    engine = engine_manager.get_engine()
    print('Engine:', engine)
    async with engine.begin() as conn:
        print('Connected!')

asyncio.run(test())
