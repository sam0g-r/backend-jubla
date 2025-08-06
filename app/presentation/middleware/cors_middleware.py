from fastapi import Request
from fastapi.responses import JSONResponse
from typing import List, Optional
import re
from app.shared.config.settings import settings
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

class CORSMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        allowed_origins: List[str] = None,
        allowed_methods: List[str] = None,
        allowed_headers: List[str] = None,
        max_age: int = 86400
    ):
        super().__init__(app)
        self.allowed_origins = allowed_origins or settings.ALLOWED_ORIGINS
        self.allowed_methods = allowed_methods or ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        self.allowed_headers = allowed_headers or ["*"]
        self.max_age = max_age

    async def dispatch(self, request: Request, call_next):
        origin = request.headers.get("origin")
        
        # Manejar preflight requests
        if request.method == "OPTIONS":
            return self._handle_preflight_request(origin)
        
        # Verificar origen para requests normales
        if origin and not self._is_origin_allowed(origin):
            print(f"Origin recibido: {origin}")
            print(f"Allowed origins: {self.allowed_origins}")
            return JSONResponse(
                status_code=403,
                content={"detail": "Origin not allowed"}
            )

        # Procesar request
        response = await call_next(request)

        # Agregar headers CORS
        if origin and self._is_origin_allowed(origin):
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Methods"] = ", ".join(self.allowed_methods)
            response.headers["Access-Control-Allow-Headers"] = ", ".join(self.allowed_headers)
            response.headers["Access-Control-Max-Age"] = str(self.max_age)
            response.headers["Access-Control-Allow-Credentials"] = "true"

        return response

    def _handle_preflight_request(self, origin: Optional[str]) -> Response:
        """Maneja las requests OPTIONS (preflight)"""
        if origin and self._is_origin_allowed(origin):
            headers = {
                "Access-Control-Allow-Origin": origin,
                "Access-Control-Allow-Methods": ", ".join(self.allowed_methods),
                "Access-Control-Allow-Headers": ", ".join(self.allowed_headers),
                "Access-Control-Max-Age": str(self.max_age),
                "Access-Control-Allow-Credentials": "true"
            }
            return Response(status_code=200, headers=headers)
        else:
            return JSONResponse(
                status_code=403,
                content={"detail": "Origin not allowed"}
            )

    def _is_origin_allowed(self, origin: str) -> bool:
        for allowed_origin in self.allowed_origins:
            if allowed_origin == "*":
                return True
            if re.match(allowed_origin, origin):
                return True
        return False 