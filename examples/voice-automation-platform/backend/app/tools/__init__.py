"""MCP tools system for extending agent capabilities."""

from .base import MCPTool, ToolResult
from .cli_executor import CLIExecutorTool
from .web_search import WebSearchTool
from .file_manager import FileManagerTool

__all__ = [
    "MCPTool",
    "ToolResult",
    "CLIExecutorTool",
    "WebSearchTool",
    "FileManagerTool",
]

