from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from starlette.responses import JSONResponse
from app.core.config import settings

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Bypass API key check for specific paths
        if request.url.path in ["/docs", "/openapi.json", "/redoc", "/users/login/email-password", "/users/login/google", "/users/login/facebook"]:
            return await call_next(request)

        api_key = request.headers.get("X-API-KEY")
        if api_key != settings.API_KEY:
            return JSONResponse(
                status_code=403,
                content={"message": "Invalid or missing API key"},
            )

        response = await call_next(request)
        return response
