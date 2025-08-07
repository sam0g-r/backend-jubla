from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from jose import JWTError, jwt
from fastapi.responses import Response
from app.shared.config.settings import settings

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
        public_paths = [
            "/api/v1/auth/login", 
            "/api/v1/auth/register", 
            "/api/v1/events",
            "/api/v1/events/{slug}"
            "/health",
            "/docs",
            "/redoc",
            "/openapi.json"
        ]

        if any(request.url.path.startswith(path) for path in public_paths):
            return await call_next(request)

        # Leer header Authorization directamente
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authorization header missing or malformed")

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
            request.state.user_id = payload.get("sub")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        return await call_next(request)
