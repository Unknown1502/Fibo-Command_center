"""
Application Configuration
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    
    # FIBO API Configuration (Bria V2 Endpoints)
    FIBO_API_KEY: str = ""
    FIBO_API_URL: str = "https://engine.prod.bria-api.com/v2/image/generate"
    
    # Alternative FIBO endpoints
    FAL_API_KEY: str = ""
    FAL_API_URL: str = "https://fal.ai/models/bria/fibo/generate"
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    
    # Database Configuration
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/fibo_command_center"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600
    
    # Celery Configuration
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # Security
    SECRET_KEY: str = "change_this_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application Settings
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    
    # CORS Settings
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    # File Storage
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "webp"]
    
    # API Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Image Generation Settings
    DEFAULT_IMAGE_WIDTH: int = 1024
    DEFAULT_IMAGE_HEIGHT: int = 1024
    MAX_BATCH_SIZE: int = 50
    DEFAULT_QUALITY: float = 0.95
    
    # HDR Settings
    HDR_ENABLED: bool = True
    DEFAULT_COLOR_DEPTH: int = 16
    DEFAULT_COLOR_SPACE: str = "rec2020"
    
    # Monitoring
    SENTRY_DSN: str = ""
    ENABLE_METRICS: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()


# Validate critical settings
def validate_settings():
    """
    Validate that required settings are configured
    """
    errors = []
    
    if not settings.FIBO_API_KEY and not settings.FAL_API_KEY:
        errors.append("FIBO_API_KEY or FAL_API_KEY must be set")
    
    if not settings.OPENAI_API_KEY:
        errors.append("OPENAI_API_KEY must be set")
    
    if settings.ENVIRONMENT == "production" and settings.SECRET_KEY == "change_this_in_production":
        errors.append("SECRET_KEY must be changed in production")
    
    if errors:
        raise ValueError("Configuration errors: " + "; ".join(errors))


# Validate on import
if os.getenv("SKIP_VALIDATION") != "true":
    try:
        validate_settings()
    except ValueError as e:
        print(f"Warning: {e}")
        print("Set environment variables before running the application")
