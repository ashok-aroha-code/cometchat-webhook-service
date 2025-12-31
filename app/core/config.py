"""Service configuration"""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings"""
    # Service
    SERVICE_NAME: str = "cometchat-webhook-service"
    SERVICE_VERSION: str = "1.0.0"
    
    # CometChat
    COMETCHAT_APP_ID: str
    COMETCHAT_API_KEY: str
    COMETCHAT_REGION: str = "us"
    COMETCHAT_AUTH_KEY: str | None = None
    COMETCHAT_AUTH_SECRET: str | None = None
    
    # CORS
    ALLOWED_ORIGINS: list[str] = ["*"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
