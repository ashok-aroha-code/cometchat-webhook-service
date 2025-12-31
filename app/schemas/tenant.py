"""Tenant schemas for API requests/responses"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from datetime import datetime


class TenantBase(BaseModel):
    """Base tenant schema"""
    user_first_name: Optional[str] = Field(None, max_length=100)
    user_last_name: Optional[str] = Field(None, max_length=100)
    user_email: EmailStr
    user_phone: Optional[str] = Field(None, max_length=20)
    cometchat_region: str = Field(default="us", max_length=10)
    cometchat_log_level: str = Field(default="INFO", max_length=10)


class TenantCreate(TenantBase):
    """Schema for creating a tenant"""
    cometchat_app_id: Optional[str] = None
    cometchat_api_key: Optional[str] = None
    cometchat_account_key: Optional[str] = None
    cometchat_account_secret: Optional[str] = None
    cometchat_auth_key: Optional[str] = None
    extra_metadata: Optional[Dict[str, Any]] = None  # Changed from 'metadata'


class TenantUpdate(BaseModel):
    """Schema for updating a tenant"""
    user_first_name: Optional[str] = None
    user_last_name: Optional[str] = None
    user_phone: Optional[str] = None
    cometchat_app_id: Optional[str] = None
    cometchat_api_key: Optional[str] = None
    cometchat_account_key: Optional[str] = None
    cometchat_account_secret: Optional[str] = None
    is_active: Optional[bool] = None
    extra_metadata: Optional[Dict[str, Any]] = None  # Changed from 'metadata'


class TenantResponse(TenantBase):
    """Schema for tenant response"""
    id: int
    user_id: str  # UUID as string for SQLite
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    extra_metadata: Optional[Dict[str, Any]] = None  # Changed from 'metadata'
    
    class Config:
        from_attributes = True
