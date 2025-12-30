"""Webhook API endpoints"""
from fastapi import APIRouter, HTTPException, status
from app.schemas.webhook import WebhookCreateRequest, WebhookResponse
from app.services.cometchat_client import cometchat_client
from app.utils.exceptions import CometChatAPIError
from app.core.logging import logger

router = APIRouter(prefix="/api/v1/webhooks", tags=["webhooks"])

@router.post(
    "",
    response_model=WebhookResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new webhook"
)
async def create_webhook(request: WebhookCreateRequest):
    """
    Create a new CometChat webhook
    
    - **webhook_id**: Unique identifier
    - **name**: Descriptive name
    - **url**: HTTPS webhook endpoint
    """
    try:
        result = await cometchat_client.create_webhook(
            webhook_id=request.webhook_id,
            name=request.name,
            url=str(request.url),
            basic_auth=request.basic_auth,
            username=request.username,
            password=request.password,
            enabled=request.enabled,
            retry_on_failure=request.retry_on_failure
        )
        
        return WebhookResponse(
            success=True,
            message="Webhook created successfully",
            data=result
        )
        
    except CometChatAPIError as e:
        logger.error(f"Failed to create webhook: {str(e)}")
        raise HTTPException(
            status_code=e.status_code,
            detail=e.message
        )
