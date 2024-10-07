# app/main.py

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.api.routes.users import router as user_router
from app.db.database import engine
from app.models.user import Base as UserBase
from app.middlewares.api_key_middleware import APIKeyMiddleware
from app.core.config import settings
from starlette.middleware.sessions import SessionMiddleware

from fastapi_limiter import FastAPILimiter
import aioredis

UserBase.metadata.create_all(bind=engine)

app = FastAPI()

# Start Rate Limit
@app.on_event("startup")
async def startup():
    redis = await aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis)

@app.on_event("shutdown")
async def shutdown():
    redis.close()
    await redis.wait_closed()
# End Rate Limit

# SessionMiddleware first
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

# API Key middleware
app.add_middleware(APIKeyMiddleware)


app.include_router(user_router, prefix="/users")

# Custom OpenAPI schema to include X-API-KEY header globally
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI Authentication System",
        version="1.0.0",
        description="API with X-API-KEY header for authorization",
        routes=app.routes,
    )
    # Add X-API-KEY header to each path in OpenAPI schema
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["parameters"] = [
                {
                    "name": "X-API-KEY",
                    "in": "header",
                    "required": True,
                    "schema": {"type": "string", "default": settings.API_KEY},
                    "description": "API key required for authorization",
                }
            ] + method.get("parameters", [])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
