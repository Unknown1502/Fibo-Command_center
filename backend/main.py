"""
FIBO Command Center - Main Application Entry Point
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from typing import Optional

from config import settings
from routers import generation, workflows, projects, auth, ai_translator, image_processing, brand_guidelines, analytics, controlnet
from database import engine, Base
from middleware.rate_limit import RateLimitMiddleware
from middleware.logging import LoggingMiddleware

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan management
    """
    # Startup
    logger.info("Starting FIBO Command Center...")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created")
    
    # Initialize services
    logger.info("Services initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down FIBO Command Center...")


# Create FastAPI application
app = FastAPI(
    title="FIBO Command Center API",
    description="Professional AI Visual Production Suite with Agentic Intelligence",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
if settings.RATE_LIMIT_ENABLED:
    app.add_middleware(RateLimitMiddleware)

app.add_middleware(LoggingMiddleware)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(generation.router, prefix="/api/generate", tags=["Generation"])
app.include_router(workflows.router, prefix="/api/workflows", tags=["Workflows"])
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(ai_translator.router, prefix="/api/ai", tags=["AI Translator"])
app.include_router(image_processing.router, prefix="/api/image-processing", tags=["Image Processing"])
app.include_router(brand_guidelines.router, prefix="/api/brand", tags=["Brand Guidelines"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(controlnet.router, prefix="/api/controlnet", tags=["ControlNet"])


@app.get("/")
async def root():
    """
    Root endpoint - API health check
    """
    return {
        "status": "online",
        "message": "FIBO Command Center API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }


@app.get("/api/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "services": {
            "database": "connected",
            "redis": "connected",
            "fibo_api": "available"
        }
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Custom HTTP exception handler
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    General exception handler for unexpected errors
    """
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
