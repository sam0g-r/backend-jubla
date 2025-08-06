from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",      # Next.js dev
        "http://localhost:3001",      # Next.js prod
        "https://jubla-app.vercel.app", # Producción
        "https://*.jubla.org",        # Subdominios
    ]
    
    # Database
    DATABASE_URL: str = "postgresql://user:pass@localhost:5556/jubla_db"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # PayPal
    PAYPAL_CLIENT_ID: str = ""
    PAYPAL_CLIENT_SECRET: str = ""
    PAYPAL_MODE: str = "sandbox"  # or "live"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Jubla API"
    PROJECT_VERSION: str = "1.0.0"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 