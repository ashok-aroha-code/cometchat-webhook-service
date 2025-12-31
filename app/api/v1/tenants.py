"""Tenant management endpoints"""
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate, TenantUpdate, TenantResponse
from app.core.logging import logger

router = APIRouter(prefix="/api/v1/tenants", tags=["tenants"])


@router.post(
    "",
    response_model=TenantResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new tenant"
)
async def create_tenant(
    tenant_data: TenantCreate,
    db: Session = Depends(get_db)
):
    """Create a new tenant with CometChat credentials"""
    
    # Check if email already exists
    existing = db.query(Tenant).filter(
        Tenant.user_email == tenant_data.user_email
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Tenant with email {tenant_data.user_email} already exists"
        )
    
    # Create new tenant
    tenant = Tenant(**tenant_data.dict())
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    
    logger.info(f"Created tenant: {tenant.user_id} ({tenant.user_email})")
    return tenant


@router.get(
    "",
    response_model=List[TenantResponse],
    summary="List all tenants"
)
async def list_tenants(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
    db: Session = Depends(get_db)
):
    """List all tenants with pagination"""
    query = db.query(Tenant)
    
    if active_only:
        query = query.filter(Tenant.is_active == True)
    
    tenants = query.offset(skip).limit(limit).all()
    return tenants


@router.get(
    "/{user_id}",
    response_model=TenantResponse,
    summary="Get tenant by user_id"
)
async def get_tenant(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get tenant details by user_id (UUID)"""
    tenant = db.query(Tenant).filter(Tenant.user_id == user_id).first()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tenant with user_id {user_id} not found"
        )
    
    return tenant


@router.put(
    "/{user_id}",
    response_model=TenantResponse,
    summary="Update tenant"
)
async def update_tenant(
    user_id: str,
    tenant_data: TenantUpdate,
    db: Session = Depends(get_db)
):
    """Update tenant information"""
    tenant = db.query(Tenant).filter(Tenant.user_id == user_id).first()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tenant with user_id {user_id} not found"
        )
    
    # Update fields
    for field, value in tenant_data.dict(exclude_unset=True).items():
        setattr(tenant, field, value)
    
    db.commit()
    db.refresh(tenant)
    
    logger.info(f"Updated tenant: {user_id}")
    return tenant


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete tenant"
)
async def delete_tenant(
    user_id: str,
    hard_delete: bool = False,
    db: Session = Depends(get_db)
):
    """Delete tenant (soft delete by default)"""
    tenant = db.query(Tenant).filter(Tenant.user_id == user_id).first()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tenant with user_id {user_id} not found"
        )
    
    if hard_delete:
        db.delete(tenant)
        logger.info(f"Hard deleted tenant: {user_id}")
    else:
        tenant.is_active = False
        logger.info(f"Soft deleted tenant: {user_id}")
    
    db.commit()
