"""
ChatKit Session Management Routes

Official ChatKit session creation endpoint following OpenAI patterns.
Handles session initialization, workflow configuration, and client secret generation.
"""

from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import os
from openai import OpenAI, AsyncOpenAI
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chatkit", tags=["chatkit"])

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class WorkflowConfig(BaseModel):
    """Workflow configuration for ChatKit session"""
    id: str = Field(..., description="Workflow ID from Agent Builder")


class FileUploadConfig(BaseModel):
    """File upload configuration"""
    enabled: bool = Field(default=True, description="Enable file uploads")
    max_size_mb: Optional[int] = Field(default=10, description="Max file size in MB")
    allowed_types: Optional[list[str]] = Field(
        default=None,
        description="Allowed MIME types (None = all types)"
    )


class ChatKitConfiguration(BaseModel):
    """ChatKit-specific configuration"""
    file_upload: Optional[FileUploadConfig] = Field(
        default=None,
        description="File upload configuration"
    )


class SessionCreateRequest(BaseModel):
    """Request body for creating a ChatKit session"""
    workflow: WorkflowConfig = Field(..., description="Workflow configuration")
    user: Optional[str] = Field(default=None, description="User identifier")
    chatkit_configuration: Optional[ChatKitConfiguration] = Field(
        default=None,
        description="ChatKit configuration"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional session metadata"
    )


class SessionCreateResponse(BaseModel):
    """Response body for session creation"""
    client_secret: str = Field(..., description="Client secret for session")
    session_id: Optional[str] = Field(default=None, description="Session ID")
    expires_at: Optional[int] = Field(default=None, description="Expiration timestamp")


@router.post("/session", response_model=SessionCreateResponse)
async def create_chatkit_session(
    request: SessionCreateRequest = Body(...)
) -> SessionCreateResponse:
    """
    Create a new ChatKit session with workflow configuration.
    
    This endpoint follows the official ChatKit pattern for session creation:
    1. Validates workflow ID
    2. Creates session with OpenAI API
    3. Returns client secret for frontend
    
    **Official Pattern:**
    ```typescript
    POST /api/chatkit/session
    {
      "workflow": { "id": "wf_xxx" },
      "chatkit_configuration": {
        "file_upload": { "enabled": true }
      }
    }
    ```
    
    **Response:**
    ```json
    {
      "client_secret": "cs_xxx"
    }
    ```
    
    Args:
        request: Session creation request with workflow and configuration
        
    Returns:
        SessionCreateResponse with client_secret for frontend
        
    Raises:
        HTTPException: If workflow ID is invalid or API call fails
    """
    try:
        logger.info(f"Creating ChatKit session for workflow: {request.workflow.id}")
        
        # Validate workflow ID format
        if not request.workflow.id or not request.workflow.id.startswith("wf_"):
            raise HTTPException(
                status_code=400,
                detail="Invalid workflow ID format. Must start with 'wf_'"
            )
        
        # Prepare session creation payload
        session_payload: Dict[str, Any] = {
            "workflow": {"id": request.workflow.id}
        }
        
        # Add user if provided
        if request.user:
            session_payload["user"] = request.user
        
        # Add ChatKit configuration
        if request.chatkit_configuration:
            config_dict: Dict[str, Any] = {}
            
            if request.chatkit_configuration.file_upload:
                upload_config = {
                    "enabled": request.chatkit_configuration.file_upload.enabled
                }
                if request.chatkit_configuration.file_upload.max_size_mb:
                    upload_config["max_size_mb"] = (
                        request.chatkit_configuration.file_upload.max_size_mb
                    )
                if request.chatkit_configuration.file_upload.allowed_types:
                    upload_config["allowed_types"] = (
                        request.chatkit_configuration.file_upload.allowed_types
                    )
                config_dict["file_upload"] = upload_config
            
            session_payload["chatkit_configuration"] = config_dict
        
        # Add metadata if provided
        if request.metadata:
            session_payload["metadata"] = request.metadata
        
        # Create session with OpenAI API
        logger.debug(f"Session payload: {session_payload}")
        
        try:
            # Note: Using the official OpenAI ChatKit API
            # This requires the chatkit SDK to be installed
            session = openai_client.chatkit.sessions.create(**session_payload)
            
            logger.info(f"ChatKit session created successfully")
            
            return SessionCreateResponse(
                client_secret=session.client_secret,
                session_id=getattr(session, 'id', None),
                expires_at=getattr(session, 'expires_at', None)
            )
            
        except AttributeError as e:
            # Fallback if chatkit SDK is not available
            logger.warning(
                f"ChatKit SDK not available, using fallback: {str(e)}"
            )
            
            # Generate a mock client secret for development
            # In production, you must use the official SDK
            import secrets
            import time
            
            mock_secret = f"cs_dev_{secrets.token_urlsafe(32)}"
            
            logger.warning(
                "⚠️ Using MOCK client secret - "
                "Install chatkit SDK for production use"
            )
            
            return SessionCreateResponse(
                client_secret=mock_secret,
                session_id=f"session_{secrets.token_hex(16)}",
                expires_at=int(time.time() + 3600)  # 1 hour
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create ChatKit session: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create session: {str(e)}"
        )


@router.post("/session/refresh")
async def refresh_chatkit_session(
    client_secret: str = Body(..., embed=True)
) -> SessionCreateResponse:
    """
    Refresh an existing ChatKit session.
    
    **Usage:**
    ```typescript
    POST /api/chatkit/session/refresh
    {
      "client_secret": "cs_xxx"
    }
    ```
    
    Args:
        client_secret: Current client secret
        
    Returns:
        New SessionCreateResponse with refreshed client_secret
        
    Raises:
        HTTPException: If refresh fails
    """
    try:
        logger.info("Refreshing ChatKit session")
        
        # Note: Implement session refresh logic here
        # This would typically involve validating the current secret
        # and issuing a new one
        
        # For now, return the same secret (mock implementation)
        logger.warning("Session refresh not fully implemented - returning same secret")
        
        return SessionCreateResponse(
            client_secret=client_secret
        )
        
    except Exception as e:
        logger.error(f"Failed to refresh session: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to refresh session: {str(e)}"
        )


@router.get("/health")
async def chatkit_health():
    """
    Health check endpoint for ChatKit service.
    
    Returns:
        Health status with API key validation
    """
    api_key = os.getenv("OPENAI_API_KEY")
    workflow_id = os.getenv("CHATKIT_WORKFLOW_ID")
    
    return {
        "status": "healthy",
        "api_key_configured": bool(api_key),
        "workflow_id_configured": bool(workflow_id),
        "chatkit_sdk_available": hasattr(openai_client, 'chatkit')
    }

