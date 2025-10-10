"""Base agent class for all specialized agents."""

import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AgentRole(str, Enum):
    """Agent role types."""

    ORCHESTRATOR = "orchestrator"
    RESEARCH = "research"
    CODE = "code"
    DATA = "data"
    VALIDATOR = "validator"
    BROWSER = "browser"
    CUSTOM = "custom"


class AgentStatus(str, Enum):
    """Agent execution status."""

    IDLE = "idle"
    THINKING = "thinking"
    EXECUTING = "executing"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Task(BaseModel):
    """Task definition for agents."""

    id: str = Field(default_factory=lambda: f"task_{uuid.uuid4().hex[:12]}")
    type: str
    description: str
    params: dict[str, Any] = Field(default_factory=dict)
    priority: int = Field(default=0, ge=0, le=10)
    depends_on: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    status: AgentStatus = AgentStatus.IDLE
    result: Any | None = None
    error: str | None = None


class AgentMetadata(BaseModel):
    """Metadata about an agent instance."""

    id: str = Field(default_factory=lambda: f"agent_{uuid.uuid4().hex[:12]}")
    role: AgentRole
    name: str
    description: str
    model: str = "gpt-4"
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=2000, ge=1)
    tools: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    status: AgentStatus = AgentStatus.IDLE
    current_task: str | None = None
    completed_tasks: int = 0
    failed_tasks: int = 0


class BaseAgent(ABC):
    """
    Base class for all agents in the platform.
    
    Each agent has:
    - A specific role (research, code, validator, etc.)
    - Access to MCP tools
    - Ability to communicate via webhooks
    - Task execution capabilities
    """

    def __init__(
        self,
        name: str,
        description: str,
        role: AgentRole,
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        tools: list[str] | None = None,
    ):
        """Initialize the agent."""
        self.metadata = AgentMetadata(
            role=role,
            name=name,
            description=description,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            tools=tools or [],
        )
        self._current_task: Task | None = None

    @property
    def id(self) -> str:
        """Get agent ID."""
        return self.metadata.id

    @property
    def name(self) -> str:
        """Get agent name."""
        return self.metadata.name

    @property
    def role(self) -> AgentRole:
        """Get agent role."""
        return self.metadata.role

    @property
    def status(self) -> AgentStatus:
        """Get current agent status."""
        return self.metadata.status

    @abstractmethod
    async def process_task(self, task: Task) -> Any:
        """
        Process a task and return the result.
        
        Args:
            task: Task to process
            
        Returns:
            Task result
            
        Raises:
            Exception: If task processing fails
        """
        pass

    @abstractmethod
    async def validate_task(self, task: Task) -> bool:
        """
        Validate if this agent can handle the given task.
        
        Args:
            task: Task to validate
            
        Returns:
            True if agent can handle the task
        """
        pass

    async def execute_task(self, task: Task) -> Task:
        """
        Execute a task with proper state management.
        
        Args:
            task: Task to execute
            
        Returns:
            Completed task with result or error
        """
        # Validate task
        if not await self.validate_task(task):
            task.status = AgentStatus.FAILED
            task.error = f"Agent {self.name} cannot handle task type {task.type}"
            return task

        # Update status
        self._current_task = task
        self.metadata.status = AgentStatus.EXECUTING
        self.metadata.current_task = task.id
        task.status = AgentStatus.EXECUTING
        task.started_at = datetime.now()

        try:
            # Process the task
            result = await self.process_task(task)
            
            # Mark as completed
            task.result = result
            task.status = AgentStatus.COMPLETED
            task.completed_at = datetime.now()
            self.metadata.completed_tasks += 1

        except Exception as e:
            # Mark as failed
            task.error = str(e)
            task.status = AgentStatus.FAILED
            task.completed_at = datetime.now()
            self.metadata.failed_tasks += 1

        finally:
            # Reset agent status
            self.metadata.status = AgentStatus.IDLE
            self.metadata.current_task = None
            self._current_task = None

        return task

    def get_system_prompt(self) -> str:
        """
        Get the system prompt for this agent.
        
        Returns:
            System prompt string
        """
        return f"""You are {self.name}, a {self.role.value} agent.

Description: {self.metadata.description}

Available tools: {', '.join(self.metadata.tools) if self.metadata.tools else 'None'}

Your role is to {self.role.value} tasks efficiently and accurately.
Always provide clear, actionable results."""

    def to_dict(self) -> dict[str, Any]:
        """Convert agent to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role.value,
            "status": self.status.value,
            "current_task": self.metadata.current_task,
            "completed_tasks": self.metadata.completed_tasks,
            "failed_tasks": self.metadata.failed_tasks,
            "created_at": self.metadata.created_at.isoformat(),
        }

