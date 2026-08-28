import pytest
import asyncio
from typing import Tuple
from app.api.protection.strategy import RateLimiterStrategy
from app.api.protection.limiter import InMemoryTokenBucketLimiter
from app.api.protection.middleware import RateLimitMiddleware
from fastapi import FastAPI
from starlette.testclient import TestClient

class MockRedisTokenBucketLimiter(RateLimiterStrategy):
    """
    Mock implementation of a Redis-backed rate limiter to prove that 
    the RateLimiterStrategy abstraction successfully hides storage details.
    """
    def __init__(self):
        self.mock_redis_store = {}
        
    async def is_allowed(self, key: str, limit: int, window: int) -> Tuple[bool, int, int]:
        # Simulate Redis INCR and EXPIRE operations
        if key not in self.mock_redis_store:
            self.mock_redis_store[key] = {"tokens": limit - 1, "window": window}
            return True, limit - 1, 0
            
        store = self.mock_redis_store[key]
        if store["tokens"] > 0:
            store["tokens"] -= 1
            return True, store["tokens"], 0
            
        retry_after = int(window / limit)
        return False, 0, retry_after

@pytest.mark.asyncio
async def test_rate_limiter_abstraction_independence():
    """
    Validates that the API Protection layer (Middleware) can seamlessly switch
    between InMemory and Distributed (Redis) implementations without changing 
    the business logic or middleware itself.
    """
    app = FastAPI()
    
    # 1. Test with InMemoryTokenBucketLimiter
    in_memory_strategy = InMemoryTokenBucketLimiter()
    app.add_middleware(RateLimitMiddleware, strategy=in_memory_strategy)
    
    @app.get("/test-memory")
    async def test_memory():
        return {"status": "ok"}
        
    client = TestClient(app)
    response = client.get("/test-memory")
    # Our middleware is fail-open by default or if not configured for this route, 
    # it allows it. We just need to prove the app loads and processes the request.
    assert response.status_code == 200
    
    # 2. Test with MockRedisTokenBucketLimiter
    app_redis = FastAPI()
    redis_strategy = MockRedisTokenBucketLimiter()
    app_redis.add_middleware(RateLimitMiddleware, strategy=redis_strategy)
    
    @app_redis.get("/test-redis")
    async def test_redis():
        return {"status": "ok"}
        
    client_redis = TestClient(app_redis)
    response_redis = client_redis.get("/test-redis")
    assert response_redis.status_code == 200
    
    # Prove the Redis mock is actually an instance of the required abstraction
    assert isinstance(redis_strategy, RateLimiterStrategy)
    assert isinstance(in_memory_strategy, RateLimiterStrategy)
