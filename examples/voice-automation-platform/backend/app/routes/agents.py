"""Agent management endpoints."""

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..agents.base import AgentRole, AgentStatus, BaseAgent, AgentMetadata
from ..agents.main_agent import MainAgent
from ..agents.research_agent import ResearchAgent
from ..agents.code_agent import CodeAgent
from ..agents.validator_agent import ValidatorAgent

router = APIRouter()

# Active agents registry
_active_agents: dict[str, BaseAgent] = {}
_agent_classes: dict[AgentRole, type[BaseAgent]] = {
    AgentRole.ORCHESTRATOR: MainAgent,
    AgentRole.RESEARCH: ResearchAgent,
    AgentRole.CODE: CodeAgent,
    AgentRole.VALIDATOR: ValidatorAgent,
}


class AgentSpawnRequest(BaseModel):
    """Request model for spawning an agent."""

    role: AgentRole = Field(..., description="Agent role to spawn")
    custom_name: str | None = Field(default=None, description="Custom agent name")
    model: str | None = Field(default=None, description="LLM model to use")
    temperature: float | None = Field(default=None, ge=0.0, le=2.0, description="Temperature")
    max_tokens: int | None = Field(default=None, ge=1, description="Max tokens")


class AgentResponse(BaseModel):
    """Response model for agent operations."""

    agent_id: str
    role: str
    name: str
    description: str
    status: str
    model: str
    current_task: str | None = None
    completed_tasks: int
    failed_tasks: int
    created_at: str
    tools: list[str]


class AgentListResponse(BaseModel):
    """Response model for listing agents."""

    agents: list[AgentResponse]
    total: int


class AgentStats(BaseModel):
    """Agent statistics response."""

    total: int
    active: int
    idle: int
    executing: int
    by_role: dict[str, int]


def agent_to_response(agent: BaseAgent) -> AgentResponse:
    """Convert agent to response model."""
    return AgentResponse(
        agent_id=agent.metadata.id,
        role=agent.metadata.role.value,
        name=agent.metadata.name,
        description=agent.metadata.description,
        status=agent.metadata.status.value,
        model=agent.metadata.model,
        current_task=agent.metadata.current_task,
        completed_tasks=agent.metadata.completed_tasks,
        failed_tasks=agent.metadata.failed_tasks,
        created_at=agent.metadata.created_at.isoformat(),
        tools=agent.metadata.tools,
    )


@router.post("", response_model=AgentResponse, status_code=201)
async def spawn_agent(request: AgentSpawnRequest) -> AgentResponse:
    """
    Spawn a new agent of the specified role.
    
    The agent will be initialized and registered as active.
    Custom configuration can be provided via optional parameters.
    """
    # Get agent class
    if request.role not in _agent_classes:
        raise HTTPException(
            status_code=400,
            detail=f"Agent role '{request.role}' not supported",
        )
    
    agent_class = _agent_classes[request.role]
    
    # Create agent instance
    try:
        agent = agent_class()
        
        # Apply custom configuration if provided
        if request.custom_name:
            agent.metadata.name = request.custom_name
        if request.model:
            agent.metadata.model = request.model
        if request.temperature is not None:
            agent.metadata.temperature = request.temperature
        if request.max_tokens:
            agent.metadata.max_tokens = request.max_tokens
        
        # Register agent
        _active_agents[agent.metadata.id] = agent
        
        return agent_to_response(agent)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to spawn agent: {str(e)}",
        )


@router.get("", response_model=AgentListResponse)
async def list_agents() -> AgentListResponse:
    """
    List all active agents.
    
    Returns metadata for all currently active agents in the system.
    """
    agent_responses = [agent_to_response(agent) for agent in _active_agents.values()]
    
    return AgentListResponse(
        agents=agent_responses,
        total=len(agent_responses),
    )


@router.get("/stats", response_model=AgentStats)
async def get_agent_stats() -> AgentStats:
    """
    Get agent statistics.
    
    Provides overview of active agents, their statuses, and distribution by role.
    """
    agents = list(_active_agents.values())
    
    by_role: dict[str, int] = {}
    for agent in agents:
        role = agent.metadata.role.value
        by_role[role] = by_role.get(role, 0) + 1
    
    return AgentStats(
        total=len(agents),
        active=sum(1 for a in agents if a.metadata.status != AgentStatus.IDLE),
        idle=sum(1 for a in agents if a.metadata.status == AgentStatus.IDLE),
        executing=sum(1 for a in agents if a.metadata.status == AgentStatus.EXECUTING),
        by_role=by_role,
    )


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str) -> AgentResponse:
    """
    Get details of a specific agent.
    """
    if agent_id not in _active_agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    agent = _active_agents[agent_id]
    return agent_to_response(agent)


@router.get("/{agent_id}/status")
async def get_agent_status(agent_id: str) -> dict[str, Any]:
    """
    Get detailed status of an agent.
    
    Includes current task, recent activity, and performance metrics.
    """
    if agent_id not in _active_agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    agent = _active_agents[agent_id]
    
    return {
        "agent_id": agent.metadata.id,
        "status": agent.metadata.status.value,
        "current_task": agent.metadata.current_task,
        "completed_tasks": agent.metadata.completed_tasks,
        "failed_tasks": agent.metadata.failed_tasks,
        "success_rate": (
            agent.metadata.completed_tasks / 
            (agent.metadata.completed_tasks + agent.metadata.failed_tasks)
            if (agent.metadata.completed_tasks + agent.metadata.failed_tasks) > 0
            else 0.0
        ),
        "tools": agent.metadata.tools,
        "uptime_seconds": (
            asyncio.get_event_loop().time() - agent.metadata.created_at.timestamp()
        ),
    }


@router.delete("/{agent_id}", status_code=204)
async def remove_agent(agent_id: str):
    """
    Remove an agent from the active pool.
    
    The agent will be gracefully shut down and removed from the registry.
    Cannot remove agents that are currently executing tasks.
    """
    if agent_id not in _active_agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    agent = _active_agents[agent_id]
    
    # Check if agent is executing
    if agent.metadata.status == AgentStatus.EXECUTING:
        raise HTTPException(
            status_code=400,
            detail="Cannot remove agent while executing task",
        )
    
    # Remove agent
    del _active_agents[agent_id]
    
    return None


# Import asyncio for uptime calculation
import asyncio

