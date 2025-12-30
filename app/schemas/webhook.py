"""Webhook data models"""
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, Any

class WebhookCreateRequest(BaseModel):
    """Request schema for webhook creation"""
    webhook_id: str = Field(..., description="Unique webhook identifier", min_length=1)
    name: str = Field(..., min_length=1, max_length=100)
    url: HttpUrl = Field(..., description="Webhook URL (HTTPS required)")
    basic_auth: bool = Field(default=False)
    username: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None)
    enabled: bool = Field(default=True)
    retry_on_failure: bool = Field(default=True)
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "webhook_id": "webhook_prod_001",
                "name": "Production Webhook",
                "url": "https://api.example.com/webhooks/cometchat",
                "basic_auth": True,
                "username": "webhook_user",
                "password": "secure_password",
                "enabled": True,
                "retry_on_failure": True
            }
        }
    }

class WebhookResponse(BaseModel):
    """Response schema for webhook operations"""
    success: bool
    message: str
    data: Optional[Any] = None
