"""FastAPI microservice for CometChat webhook management"""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import time

from app.api.v1 import webhooks
from app.core.config import get_settings
from app.core.logging import logger
from app.services.cometchat_client import cometchat_client

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events"""
    logger.info("Starting CometChat Webhook Service")
    yield
    logger.info("Shutting down CometChat Webhook Service")

app = FastAPI(
    title="CometChat Webhook Service",
    description="Microservice for managing CometChat webhooks",
    version="1.0.0",
    lifespan=lifespan
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
    """Log all requests"""
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
    """Health check endpoint"""
    return {"status": "healthy", "service": "cometchat-webhook-service"}

@app.get("/health/ready", tags=["health"])
async def readiness_check():
    """Readiness check with CometChat API validation"""
    is_ready = await cometchat_client.health_check()
    
    if not is_ready:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not ready", "reason": "CometChat API unreachable"}
        )
    
    return {"status": "ready"}

# Include routers
app.include_router(webhooks.router)

@app.get("/", tags=["root"])
async def root():
    """Root endpoint"""
    return {
        "service": "CometChat Webhook Service",
        "version": "1.0.0",
        "status": "running"
    }
