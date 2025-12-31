"""FastAPI microservice for CometChat webhook management"""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import time

from app.api.v1 import webhooks, apps, roles, tenants
from app.core.config import get_settings
from app.core.logging import logger
from app.core.init_db import init_db
from app.services.cometchat_client import cometchat_client

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events"""
    logger.info("Starting CometChat Management Service")
    
    # Initialize database on startup
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise
    
    yield
    
    logger.info("Shutting down CometChat Management Service")


app = FastAPI(
    title="CometChat Management Service",
    description="Microservice for managing CometChat webhooks, apps, roles, and tenants",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)


# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests with timing"""
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(
        "Request processed",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "process_time": f"{process_time:.3f}s"
        }
    )
    
    return response


# Health check endpoints
@app.get("/health", tags=["health"])
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "service": "cometchat-management-service",
        "version": "1.0.0"
    }


@app.get("/health/ready", tags=["health"])
async def readiness_check():
    """
    Readiness check with CometChat API validation
    
    Checks if the service can connect to CometChat API
    """
    is_ready = await cometchat_client.health_check()
    
    if not is_ready:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "not ready",
                "reason": "CometChat API unreachable",
                "service": "cometchat-management-service"
            }
        )
    
    return {
        "status": "ready",
        "service": "cometchat-management-service",
        "cometchat_api": "connected"
    }


@app.get("/health/database", tags=["health"])
async def database_check():
    """Database health check"""
    try:
        from app.core.database import SessionLocal
        from app.models.tenant import Tenant
        
        db = SessionLocal()
        # Try to query database
        count = db.query(Tenant).count()
        db.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "tenant_count": count
        }
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "database": "disconnected",
                "error": str(e)
            }
        )


# Include routers
app.include_router(tenants.router)  # NEW: Tenant management
app.include_router(webhooks.router)
app.include_router(apps.router)
app.include_router(roles.router)


@app.get("/", tags=["root"])
async def root():
    """Root endpoint with service information"""
    return {
        "service": "CometChat Management Service",
        "version": "1.0.0",
        "status": "running",
        "description": "Microservice for managing CometChat webhooks, apps, roles, and tenants",
        "endpoints": {
            "tenants": "/api/v1/tenants",
            "webhooks": "/api/v1/webhooks",
            "apps": "/api/v1/apps",
            "roles": "/api/v1/roles"
        },
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "health_checks": {
            "basic": "/health",
            "readiness": "/health/ready",
            "database": "/health/database"
        }
    }


@app.get("/api/v1", tags=["root"])
async def api_info():
    """API version information"""
    return {
        "version": "1.0.0",
        "available_endpoints": [
            "/api/v1/tenants",
            "/api/v1/webhooks",
            "/api/v1/apps",
            "/api/v1/roles"
        ],
        "features": [
            "Multi-tenant support",
            "Dynamic CometChat credentials",
            "Webhook management",
            "App creation",
            "Role management"
        ]
    }


# Optional: Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(
        f"Unhandled exception: {str(exc)}",
        extra={
            "path": request.url.path,
            "method": request.method
        },
        exc_info=True
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.LOG_LEVEL == "DEBUG" else "An error occurred",
            "path": request.url.path
        }
    )
