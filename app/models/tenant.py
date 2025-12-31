"""Tenant model for storing app credentials (SQLite compatible)"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, JSON, DateTime, Boolean, Text
from app.core.database import Base


class Tenant(Base):
    """
    Tenant model for multi-tenant CometChat application management
    
    Stores user information and their associated CometChat app credentials
    """
    __tablename__ = "tenants"
    
    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # User Info - UUID stored as string for SQLite compatibility
    user_id = Column(
        String(36),
        unique=True,
        index=True,
        nullable=False,
        default=lambda: str(uuid.uuid4()),
        comment="Unique user identifier (UUID)"
    )
    user_first_name = Column(String(100), nullable=True)
    user_last_name = Column(String(100), nullable=True)
    user_email = Column(
        String(255), 
        unique=True, 
        index=True, 
        nullable=False,
        comment="User email address"
    )
    user_phone = Column(String(20), nullable=True)
    
    # CometChat App Credentials (encrypted in production)
    cometchat_app_id = Column(
        String(100), 
        nullable=True,
        comment="CometChat Application ID"
    )
    cometchat_api_key = Column(
        Text, 
        nullable=True,
        comment="CometChat REST API Key"
    )
    cometchat_region = Column(
        String(10), 
        default="us", 
        nullable=False,
        comment="Region: us, eu, in"
    )
    
    # CometChat Account-Level Credentials (for app management)
    cometchat_account_key = Column(
        String(100), 
        nullable=True,
        comment="Account-level key"
    )
    cometchat_account_secret = Column(
        Text, 
        nullable=True,
        comment="Account-level secret"
    )
    
    # Optional: Auth credentials (if needed)
    cometchat_auth_key = Column(
        Text, 
        nullable=True,
        comment="Auth key for client-side"
    )
    
    # Configuration
    cometchat_log_level = Column(
        String(10), 
        default="INFO", 
        nullable=False
    )
    
    # Metadata - RENAMED to avoid conflict with SQLAlchemy's reserved 'metadata'
    extra_metadata = Column(
        JSON, 
        nullable=True,
        comment="Additional tenant-specific data"
    )
    
    # Timestamps
    created_at = Column(
        DateTime, 
        default=datetime.utcnow, 
        nullable=False
    )
    updated_at = Column(
        DateTime, 
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=True
    )
    
    # Status
    is_active = Column(
        Boolean, 
        default=True, 
        nullable=False, 
        index=True
    )
    
    def __repr__(self):
        return f"<Tenant(id={self.id}, user_id={self.user_id}, email={self.user_email}, active={self.is_active})>"
    
    @property
    def full_name(self):
        """Get user's full name"""
        if self.user_first_name and self.user_last_name:
            return f"{self.user_first_name} {self.user_last_name}"
        return self.user_first_name or self.user_last_name or "N/A"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_first_name": self.user_first_name,
            "user_last_name": self.user_last_name,
            "user_email": self.user_email,
            "user_phone": self.user_phone,
            "cometchat_region": self.cometchat_region,
            "cometchat_log_level": self.cometchat_log_level,
            "extra_metadata": self.extra_metadata,  # Changed
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_active": self.is_active
        }
