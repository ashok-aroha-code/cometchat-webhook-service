"""CometChat client service for webhook operations"""
import httpx
from typing import Optional, Dict, Any
from app.core.config import get_settings
from app.core.logging import logger
from app.utils.exceptions import CometChatAPIError


settings = get_settings()


class CometChatClient:
    """Client for CometChat API operations"""
    
    def __init__(self):
        # FIXED: Correct endpoint format with appId as subdomain
        self.base_url = f"https://{settings.COMETCHAT_APP_ID}.api-{settings.COMETCHAT_REGION}.cometchat.io/v3"
        self.timeout = httpx.Timeout(30.0, connect=10.0)
    
    def _get_headers(self) -> Dict[str, str]:
        """Generate request headers"""
        # FIXED: Use lowercase 'apikey' header only
        return {
            "apikey": settings.COMETCHAT_API_KEY,  # Changed from 'apiKey'
            "Content-Type": "application/json",
            "onBehalfOf": settings.COMETCHAT_APP_ID,  # Added for Management API
            "X-Webhook-Version": "2"
        }
    
    async def create_webhook(
        self,
        webhook_id: str,
        name: str,
        url: str,
        basic_auth: bool = False,
        username: Optional[str] = None,
        password: Optional[str] = None,
        enabled: bool = True,
        retry_on_failure: bool = True
    ) -> Dict[str, Any]:
        """
        Create a new webhook in CometChat
        
        Args:
            webhook_id: Unique identifier for the webhook
            name: Webhook name
            url: Webhook URL (HTTPS required)
            basic_auth: Enable basic authentication
            username: Basic auth username
            password: Basic auth password
            enabled: Enable webhook immediately
            retry_on_failure: Retry failed deliveries
            
        Returns:
            Dict containing webhook creation response
            
        Raises:
            CometChatAPIError: If API request fails
        """
        # FIXED: Correct endpoint without /apps/{app_id}
        endpoint = f"{self.base_url}/webhooks"
        
        payload = {
            "id": webhook_id,
            "name": name,
            "url": url,
            "basicAuth": basic_auth,
            "enabled": enabled,
            "retryOnFailure": retry_on_failure
        }
        
        if basic_auth and username and password:
            payload["username"] = username
            payload["password"] = password
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    endpoint,
                    headers=self._get_headers(),
                    json=payload
                )
                response.raise_for_status()
                
                logger.info(
                    "Webhook created successfully",
                    extra={
                        "webhook_id": webhook_id,
                        "webhook_name": name,
                        "status_code": response.status_code
                    }
                )
                return response.json()
                
            except httpx.HTTPStatusError as e:
                logger.error(
                    "HTTP error creating webhook",
                    extra={
                        "webhook_id": webhook_id,
                        "status_code": e.response.status_code,
                        "response": e.response.text
                    }
                )
                raise CometChatAPIError(
                    message=f"Failed to create webhook: {e.response.text}",
                    status_code=e.response.status_code
                )
            
            except httpx.RequestError as e:
                logger.error(
                    "Request error creating webhook",
                    extra={"webhook_id": webhook_id, "error": str(e)}
                )
                raise CometChatAPIError(
                    message=f"Request failed: {str(e)}",
                    status_code=500
                )
    
    async def create_app(
        self,
        name: str,
        region: str = "us",
        case_sensitive: bool = True
    ) -> Dict[str, Any]:
        """
        Create a new app in CometChat
        
        Args:
            name: App name
            region: App region (us or eu)
            case_sensitive: Enable case sensitivity
            
        Returns:
            Dict containing app creation response
            
        Raises:
            CometChatAPIError: If API request fails
        """
        endpoint = "https://apimgmt.cometchat.io/apps"
        
        if not settings.COMETCHAT_AUTH_KEY or not settings.COMETCHAT_AUTH_SECRET:
            raise CometChatAPIError(
                message="COMETCHAT_AUTH_KEY and COMETCHAT_AUTH_SECRET are required for this operation",
                status_code=500
            )

        headers = {
            "key": settings.COMETCHAT_AUTH_KEY,
            "secret": settings.COMETCHAT_AUTH_SECRET,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "name": name,
            "region": region,
            "caseSensitive": case_sensitive
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    endpoint,
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                
                logger.info(
                    "App created successfully",
                    extra={
                        "app_name": name,
                        "region": region,
                        "status_code": response.status_code
                    }
                )
                return response.json()
                
            except httpx.HTTPStatusError as e:
                logger.error(
                    "HTTP error creating app",
                    extra={
                        "app_name": name,
                        "status_code": e.response.status_code,
                        "response": e.response.text
                    }
                )
                raise CometChatAPIError(
                    message=f"Failed to create app: {e.response.text}",
                    status_code=e.response.status_code
                )
            
            except httpx.RequestError as e:
                logger.error(
                    "Request error creating app",
                    extra={"app_name": name, "error": str(e)}
                )
                raise CometChatAPIError(
                    message=f"Request failed: {str(e)}",
                    status_code=500
                )

    async def create_role(
        self,
        role: str,
        name: str,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        settings: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new role in CometChat
        
        Args:
            role: Role UID
            name: Role name
            description: Role description
            metadata: Role metadata
            settings: Role settings
            
        Returns:
            Dict containing role creation response
            
        Raises:
            CometChatAPIError: If API request fails
        """
        endpoint = f"{self.base_url}/roles"
        
        payload = {
            "role": role,
            "name": name
        }
        
        if description:
            payload["description"] = description
            
        if metadata:
            payload["metadata"] = metadata

        if settings:
            payload["settings"] = settings
            
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    endpoint,
                    headers=self._get_headers(),
                    json=payload
                )
                response.raise_for_status()
                
                logger.info(
                    "Role created successfully",
                    extra={
                        "role_uid": role,
                        "role_name": name,
                        "status_code": response.status_code
                    }
                )
                return response.json()
                
            except httpx.HTTPStatusError as e:
                logger.error(
                    "HTTP error creating role",
                    extra={
                        "role_uid": role,
                        "status_code": e.response.status_code,
                        "response": e.response.text
                    }
                )
                raise CometChatAPIError(
                    message=f"Failed to create role: {e.response.text}",
                    status_code=e.response.status_code
                )
            
            except httpx.RequestError as e:
                logger.error(
                    "Request error creating role",
                    extra={"role_uid": role, "error": str(e)}
                )
                raise CometChatAPIError(
                    message=f"Request failed: {str(e)}",
                    status_code=500
                )

    async def health_check(self) -> bool:
        """Check if CometChat API is reachable"""
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(5.0)) as client:
                # FIXED: Correct health check endpoint
                response = await client.get(
                    f"{self.base_url}/appSettings",
                    headers=self._get_headers()
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return False


# Singleton instance
cometchat_client = CometChatClient()
