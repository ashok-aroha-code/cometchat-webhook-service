"""Logging configuration"""
import logging
import sys
from app.core.config import get_settings

settings = get_settings()

def setup_logging():
    """Configure structured logging"""
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format='{"time":"%(asctime)s","level":"%(levelname)s","service":"%(name)s","message":"%(message)s"}',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    return logging.getLogger(settings.SERVICE_NAME)

logger = setup_logging()
