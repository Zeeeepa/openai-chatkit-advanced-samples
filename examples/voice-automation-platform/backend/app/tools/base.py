"""Base classes for MCP tools."""

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, Field


class ToolResult(BaseModel):
    """Result from tool execution."""

    success: bool
    data: Any | None = None
    error: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class MCPTool(ABC):
    """
    Base class for all MCP tools.
    
    Each tool must implement:
    - name: Unique tool identifier
    - description: What the tool does
    - execute: Main tool logic
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description."""
        pass

    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        """
        Execute the tool.
        
        Args:
            **kwargs: Tool-specific parameters
            
        Returns:
            ToolResult with execution outcome
        """
        pass

    def get_schema(self) -> dict[str, Any]:
        """
        Get JSON schema for tool parameters.
        
        Returns:
            JSON schema dict
        """
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self._get_parameters_schema(),
        }

    def _get_parameters_schema(self) -> dict[str, Any]:
        """
        Get parameter schema. Override in subclasses.
        
        Returns:
            Parameter schema dict
        """
        return {
            "type": "object",
            "properties": {},
            "required": [],
        }

