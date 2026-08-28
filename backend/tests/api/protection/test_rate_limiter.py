import pytest
import asyncio
from app.api.protection.limiter import InMemoryTokenBucketLimiter

@pytest.mark.asyncio
async def test_token_bucket_allows_burst():
    limiter = InMemoryTokenBucketLimiter()
    # 5 requests per 60 seconds
    key = "test_key"
    limit = 5
    window = 60
    
    # Burst 5 requests immediately
    for _ in range(5):
        allowed, remaining, retry = await limiter.is_allowed(key, limit, window)
        assert allowed is True
        
    # 6th request should fail
    allowed, remaining, retry = await limiter.is_allowed(key, limit, window)
    assert allowed is False
    assert retry > 0

@pytest.mark.asyncio
async def test_token_bucket_isolation():
    limiter = InMemoryTokenBucketLimiter()
    limit = 5
    window = 60
    
    # Key A exhausts tokens
    for _ in range(5):
        await limiter.is_allowed("A", limit, window)
        
    allowed_a, _, _ = await limiter.is_allowed("A", limit, window)
    assert allowed_a is False
    
    # Key B should still have tokens
    allowed_b, _, _ = await limiter.is_allowed("B", limit, window)
    assert allowed_b is True
