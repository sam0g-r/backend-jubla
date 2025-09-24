from app.supertokens import init_supertokens
init_supertokens()
from supertokens_python.framework.fastapi import get_middleware
from app.infrastructure.database.prisma_client import prisma_client
from fastapi import FastAPI
from app.presentation.middleware.cors_middleware import CORSMiddleware as CustomCORSMiddleware
from app.presentation.api import auth_routes, user_routes, event_routes, reservation_routes, user_medical_information_routes, location_routes, user_role_routes, role_permission_routes 
from app.shared.config.settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para gestión de eventos Jubla",
    version=settings.PROJECT_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(get_middleware())

@app.on_event("startup")
async def startup():
    await prisma_client.connect()

@app.on_event("shutdown")
async def shutdown():
    await prisma_client.disconnect()

# Middlewares
app.add_middleware(
    CustomCORSMiddleware,
    allowed_origins=settings.ALLOWED_ORIGINS,
    allowed_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allowed_headers=["*"]
)

# Rutas
app.include_router(user_routes.router, prefix="/api/v1")
app.include_router(event_routes.router, prefix="/api/v1")
app.include_router(auth_routes.router, prefix="/api/v1")
app.include_router(reservation_routes.router, prefix="/api/v1")
app.include_router(user_medical_information_routes.router, prefix="/api/v1")
app.include_router(location_routes.router, prefix="/api/v1")
app.include_router(role_permission_routes.router, prefix="/api/v1")
app.include_router(user_role_routes.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Jubla API",
        "version": settings.PROJECT_VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )