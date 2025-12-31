"""Roles API endpoints"""
from fastapi import APIRouter, HTTPException, status
from app.schemas.role import RoleCreateRequest, RoleResponse
from app.services.cometchat_client import cometchat_client
from app.utils.exceptions import CometChatAPIError
from app.core.logging import logger

router = APIRouter(prefix="/api/v1/roles", tags=["roles"])

@router.post(
    "",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new role"
)
async def create_role(request: RoleCreateRequest):
    """
    Create a new CometChat role
    
    - **role**: Role UID
    - **name**: Role name
    - **description**: Role description (optional)
    - **metadata**: Role metadata (optional)
    - **settings**: Role settings (optional)
    """
    try:
        result = await cometchat_client.create_role(
            role=request.role,
            name=request.name,
            description=request.description,
            metadata=request.metadata,
            settings=request.settings
        )
        
        return RoleResponse(
            success=True,
            message="Role created successfully",
            data=result
        )
        
    except CometChatAPIError as e:
        logger.error(f"Failed to create role: {str(e)}")
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )

@router.post(
    "/admin",
    response_model=RoleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create admin role"
)
async def create_admin_role():
    """
    Create a new admin role with predefined permissions:
    - role: admin
    - name: Administrator
    - description: Full access administrator
    - accessLevel: 10
    - permissions: read, write, delete
    """
    try:
        # Predefined admin role payload
        admin_metadata = {
            "permissions": ["read", "write", "delete",],
            "accessLevel": 10
        }
        
        admin_settings = {
            "listUsers": "all",
            "sendMessagesTo": "all"
        }

        result = await cometchat_client.create_role(
            role="admin",
            name="Administrator",
            description="Full access administrator",
            metadata=admin_metadata,
            settings=admin_settings
        )
        
        return RoleResponse(
            success=True,
            message="Admin role created successfully",
            data=result
        )
        
    except CometChatAPIError as e:
        logger.error(f"Failed to create admin role: {str(e)}")
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )
