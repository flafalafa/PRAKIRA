"""Application entry point."""
from app.application import create_app
from app.api.v1.error_handler import setup_exception_handlers
from app.api.protection.middleware import RateLimitMiddleware

app = create_app()

# Add rate limiter middleware (executed before routers)
app.add_middleware(RateLimitMiddleware, fail_open=True)

# Register Exception Handlers
setup_exception_handlers(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
