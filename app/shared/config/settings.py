from pydantic_settings import BaseSettings
from typing import List, Optional
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
    DATABASE_URL: str
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    # PayPal
    PAYPAL_CLIENT_ID: str
    PAYPAL_CLIENT_SECRET: str
    PAYPAL_MODE: str
    
    # Redis
    REDIS_URL: str
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Jubla API"
    PROJECT_VERSION: str = "1.0.0"

    # Google configuration
    GOOGLE_DRIVE_FOLDER_ID: str
    GOOGLE_SERVICE_ACCOUNT: str
    
    # Environment
    ENVIRONMENT: str
    DEBUG: bool

    # Resend (email delivery) - opcionales
    RESEND_API_KEY: Optional[str] = None
    RESEND_FROM_EMAIL: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()