"""Apps API endpoints"""
from fastapi import APIRouter, HTTPException, status
from app.schemas.app import AppCreateRequest, AppResponse
from app.services.cometchat_client import cometchat_client
from app.utils.exceptions import CometChatAPIError
from app.core.logging import logger

router = APIRouter(prefix="/api/v1/apps", tags=["apps"])

@router.post(
    "",
    response_model=AppResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new app"
)
async def create_app(request: AppCreateRequest):
    """
    Create a new CometChat app
    
    - **name**: App name
    - **region**: App region (us or eu)
    - **caseSensitive**: Enable case sensitivity
    """
    try:
        result = await cometchat_client.create_app(
            name=request.name,
            region=request.region,
            case_sensitive=request.case_sensitive
        )
        
        return AppResponse(
            success=True,
            message="App created successfully",
            data=result
        )
        
    except CometChatAPIError as e:
        logger.error(f"Failed to create app: {str(e)}")
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )
