"""Task management endpoints."""

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from ..agents.base import Task, AgentStatus
from ..config import settings

router = APIRouter()

# In-memory task storage (replace with database in production)
_tasks: dict[str, Task] = {}


class TaskCreateRequest(BaseModel):
    """Request model for creating a task."""

    type: str = Field(..., description="Task type", min_length=1)
    description: str = Field(..., description="Task description", min_length=1)
    params: dict[str, Any] = Field(default_factory=dict, description="Task parameters")
    priority: int = Field(default=5, ge=0, le=10, description="Priority (0-10)")
    depends_on: list[str] = Field(default_factory=list, description="Task dependencies")


class TaskUpdateRequest(BaseModel):
    """Request model for updating a task."""

    description: str | None = Field(default=None, description="New description")
    params: dict[str, Any] | None = Field(default=None, description="Updated parameters")
    priority: int | None = Field(default=None, ge=0, le=10, description="New priority")
    status: AgentStatus | None = Field(default=None, description="New status")


class TaskResponse(BaseModel):
    """Response model for task operations."""

    task_id: str
    type: str
    description: str
    status: str
    priority: int
    created_at: str
    started_at: str | None = None
    completed_at: str | None = None
    result: Any | None = None
    error: str | None = None


class TaskListResponse(BaseModel):
    """Response model for task listing."""

    tasks: list[TaskResponse]
    total: int
    page: int
    page_size: int


class TaskStats(BaseModel):
    """Task statistics response."""

    total: int
    idle: int
    executing: int
    completed: int
    failed: int
    cancelled: int


@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(request: TaskCreateRequest) -> TaskResponse:
    """
    Create a new task.
    
    The task will be queued and processed based on priority and dependencies.
    """
    # Validate dependencies exist
    for dep_id in request.depends_on:
        if dep_id not in _tasks:
            raise HTTPException(
                status_code=400,
                detail=f"Dependency task '{dep_id}' not found",
            )
    
    # Create task
    task = Task(
        type=request.type,
        description=request.description,
        params=request.params,
        priority=request.priority,
        depends_on=request.depends_on,
    )
    
    # Store task
    _tasks[task.id] = task
    
    return TaskResponse(
        task_id=task.id,
        type=task.type,
        description=task.description,
        status=task.status.value,
        priority=task.priority,
        created_at=task.created_at.isoformat(),
    )


@router.get("", response_model=TaskListResponse)
async def list_tasks(
    status: AgentStatus | None = Query(default=None, description="Filter by status"),
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=20, ge=1, le=100, description="Items per page"),
) -> TaskListResponse:
    """
    List all tasks with optional filtering and pagination.
    """
    # Filter tasks
    filtered = list(_tasks.values())
    if status:
        filtered = [t for t in filtered if t.status == status]
    
    # Sort by created_at descending
    filtered.sort(key=lambda t: t.created_at, reverse=True)
    
    # Paginate
    total = len(filtered)
    start = (page - 1) * page_size
    end = start + page_size
    page_tasks = filtered[start:end]
    
    # Convert to response models
    task_responses = [
        TaskResponse(
            task_id=t.id,
            type=t.type,
            description=t.description,
            status=t.status.value,
            priority=t.priority,
            created_at=t.created_at.isoformat(),
            started_at=t.started_at.isoformat() if t.started_at else None,
            completed_at=t.completed_at.isoformat() if t.completed_at else None,
            result=t.result,
            error=t.error,
        )
        for t in page_tasks
    ]
    
    return TaskListResponse(
        tasks=task_responses,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/stats", response_model=TaskStats)
async def get_task_stats() -> TaskStats:
    """
    Get task statistics across all statuses.
    """
    tasks = list(_tasks.values())
    return TaskStats(
        total=len(tasks),
        idle=sum(1 for t in tasks if t.status == AgentStatus.IDLE),
        executing=sum(1 for t in tasks if t.status == AgentStatus.EXECUTING),
        completed=sum(1 for t in tasks if t.status == AgentStatus.COMPLETED),
        failed=sum(1 for t in tasks if t.status == AgentStatus.FAILED),
        cancelled=sum(1 for t in tasks if t.status == AgentStatus.CANCELLED),
    )


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str) -> TaskResponse:
    """
    Get details of a specific task.
    """
    if task_id not in _tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = _tasks[task_id]
    return TaskResponse(
        task_id=task.id,
        type=task.type,
        description=task.description,
        status=task.status.value,
        priority=task.priority,
        created_at=task.created_at.isoformat(),
        started_at=task.started_at.isoformat() if task.started_at else None,
        completed_at=task.completed_at.isoformat() if task.completed_at else None,
        result=task.result,
        error=task.error,
    )


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, request: TaskUpdateRequest) -> TaskResponse:
    """
    Update a task's properties.
    
    Only tasks in IDLE or FAILED status can be updated.
    """
    if task_id not in _tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = _tasks[task_id]
    
    # Check if task can be updated
    if task.status not in [AgentStatus.IDLE, AgentStatus.FAILED]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot update task in {task.status.value} status",
        )
    
    # Update fields
    if request.description is not None:
        task.description = request.description
    if request.params is not None:
        task.params = request.params
    if request.priority is not None:
        task.priority = request.priority
    if request.status is not None:
        task.status = request.status
    
    return TaskResponse(
        task_id=task.id,
        type=task.type,
        description=task.description,
        status=task.status.value,
        priority=task.priority,
        created_at=task.created_at.isoformat(),
        started_at=task.started_at.isoformat() if task.started_at else None,
        completed_at=task.completed_at.isoformat() if task.completed_at else None,
        result=task.result,
        error=task.error,
    )


@router.delete("/{task_id}", status_code=204)
async def cancel_task(task_id: str):
    """
    Cancel a task.
    
    Running tasks will be marked for cancellation.
    Completed/failed tasks cannot be cancelled.
    """
    if task_id not in _tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = _tasks[task_id]
    
    # Check if task can be cancelled
    if task.status in [AgentStatus.COMPLETED, AgentStatus.FAILED, AgentStatus.CANCELLED]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel task in {task.status.value} status",
        )
    
    # Mark as cancelled
    task.status = AgentStatus.CANCELLED
    
    return None

