# app/main.py

from fastapi import FastAPI, Header, Depends
from fastapi.openapi.models import APIKey
from fastapi.openapi.utils import get_openapi
from app.api.routes.users import router as user_router
from app.api.routes.companies import router as company_router
from app.db.database import engine
from app.models.user import Base as UserBase
from app.models.company import Base as CompanyBase
from app.middlewares.api_key_middleware import APIKeyMiddleware
from app.core.config import settings

from fastapi_limiter import FastAPILimiter
import aioredis

# Create the tables in the database
UserBase.metadata.create_all(bind=engine)
CompanyBase.metadata.create_all(bind=engine)

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

# Add the API Key middleware
app.add_middleware(APIKeyMiddleware)

# Include API routes
app.include_router(user_router, prefix="/users")
app.include_router(company_router, prefix="/companies")

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
                    "schema": {"type": "string", "default": settings.API_KEY},  # Set default value for swagger
                    "description": "API key required for authorization",
                }
            ] + method.get("parameters", [])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
