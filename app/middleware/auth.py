from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.config import settings


class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in ("/demo", "/health", "/"):
            return await call_next(request)

        api_key = request.headers.get("X-API-Key")
        if not api_key or api_key not in settings.api_keys:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or missing API Key"},
            )

        return await call_next(request)
