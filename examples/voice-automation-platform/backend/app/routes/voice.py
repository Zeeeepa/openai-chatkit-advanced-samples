"""Voice command processing endpoints."""

import asyncio
from typing import Any

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field

from ..agents.main_agent import MainAgent
from ..agents.base import Task, AgentStatus
from ..config import settings

router = APIRouter()

# Global agent instance (in production, use dependency injection)
_main_agent: MainAgent | None = None
_active_tasks: dict[str, Task] = {}


def get_main_agent() -> MainAgent:
    """Get or create the main agent instance."""
    global _main_agent
    if _main_agent is None:
        _main_agent = MainAgent()
    return _main_agent


class VoiceCommandRequest(BaseModel):
    """Request model for voice commands."""

    command: str = Field(..., description="Voice command text", min_length=1)
    language: str = Field(default="en-US", description="Language code")
    user_id: str | None = Field(default=None, description="User identifier")
    context: dict[str, Any] = Field(default_factory=dict, description="Additional context")


class VoiceCommandResponse(BaseModel):
    """Response model for voice commands."""

    task_id: str = Field(..., description="Task identifier for tracking")
    status: str = Field(..., description="Initial task status")
    message: str = Field(..., description="Status message")
    estimated_duration: int | None = Field(default=None, description="Estimated seconds")


class VoiceStatusResponse(BaseModel):
    """Voice service status response."""

    enabled: bool = Field(..., description="Whether voice input is enabled")
    provider: str = Field(..., description="Voice provider being used")
    languages: list[str] = Field(..., description="Supported languages")
    active_tasks: int = Field(..., description="Number of active tasks")


async def process_voice_command_background(task: Task):
    """Background task to process voice command."""
    try:
        agent = get_main_agent()
        task.status = AgentStatus.EXECUTING
        task.started_at = asyncio.get_event_loop().time()
        
        result = await agent.process_task(task)
        
        task.status = AgentStatus.COMPLETED
        task.completed_at = asyncio.get_event_loop().time()
        task.result = result
        
    except Exception as e:
        task.status = AgentStatus.FAILED
        task.error = str(e)
        task.completed_at = asyncio.get_event_loop().time()


@router.post("/command", response_model=VoiceCommandResponse)
async def process_voice_command(
    request: VoiceCommandRequest,
    background_tasks: BackgroundTasks,
) -> VoiceCommandResponse:
    """
    Process a voice command and create a task.
    
    The command is parsed by the main agent and executed asynchronously.
    Use the returned task_id to track progress via WebSocket or polling.
    """
    if not settings.enable_voice_input:
        raise HTTPException(
            status_code=503,
            detail="Voice input is currently disabled",
        )
    
    # Create task from voice command
    task = Task(
        type="voice_command",
        description=request.command,
        params={
            "language": request.language,
            "user_id": request.user_id,
            "context": request.context,
        },
    )
    
    # Store task
    _active_tasks[task.id] = task
    
    # Process in background
    background_tasks.add_task(process_voice_command_background, task)
    
    return VoiceCommandResponse(
        task_id=task.id,
        status=task.status.value,
        message=f"Processing command: '{request.command[:50]}...'",
        estimated_duration=30,  # Rough estimate
    )


@router.get("/status", response_model=VoiceStatusResponse)
async def get_voice_status() -> VoiceStatusResponse:
    """
    Get voice service status and configuration.
    """
    return VoiceStatusResponse(
        enabled=settings.enable_voice_input,
        provider=settings.voice_provider,
        languages=["en-US", "es-ES", "fr-FR", "de-DE", "ja-JP"],
        active_tasks=len([t for t in _active_tasks.values() if t.status == AgentStatus.EXECUTING]),
    )


@router.get("/tasks/{task_id}")
async def get_voice_task(task_id: str) -> dict[str, Any]:
    """
    Get status of a voice command task.
    """
    if task_id not in _active_tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = _active_tasks[task_id]
    return {
        "task_id": task.id,
        "status": task.status.value,
        "description": task.description,
        "created_at": task.created_at.isoformat(),
        "started_at": task.started_at.isoformat() if task.started_at else None,
        "completed_at": task.completed_at.isoformat() if task.completed_at else None,
        "result": task.result,
        "error": task.error,
    }

