"""MCP server management endpoints."""

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..tools.base import BaseTool
from ..tools.cli_executor import CLIExecutor
from ..tools.web_search import WebSearch
from ..tools.file_manager import FileManager

router = APIRouter()

# Available MCP tools
_available_tools: dict[str, type[BaseTool]] = {
    "cli_executor": CLIExecutor,
    "web_search": WebSearch,
    "file_manager": FileManager,
}

# Active tool instances
_active_tools: dict[str, BaseTool] = {}


class MCPServer(BaseModel):
    """MCP server information."""

    server_id: str
    name: str
    description: str
    version: str
    status: str
    capabilities: list[str]


class MCPToolInfo(BaseModel):
    """MCP tool information."""

    tool_id: str
    name: str
    description: str
    parameters: dict[str, Any]
    examples: list[str]


class MCPExecuteRequest(BaseModel):
    """Request model for executing an MCP tool."""

    tool_id: str = Field(..., description="Tool identifier")
    params: dict[str, Any] = Field(default_factory=dict, description="Tool parameters")


class MCPExecuteResponse(BaseModel):
    """Response model for tool execution."""

    tool_id: str
    success: bool
    result: Any | None = None
    error: str | None = None
    execution_time_ms: float


class MCPListResponse(BaseModel):
    """Response model for listing MCP servers/tools."""

    servers: list[MCPServer] | None = None
    tools: list[MCPToolInfo] | None = None
    total: int


def get_tool_instance(tool_id: str) -> BaseTool:
    """Get or create tool instance."""
    if tool_id not in _active_tools:
        if tool_id not in _available_tools:
            raise HTTPException(
                status_code=404,
                detail=f"Tool '{tool_id}' not found",
            )
        
        tool_class = _available_tools[tool_id]
        _active_tools[tool_id] = tool_class()
    
    return _active_tools[tool_id]


@router.get("/servers", response_model=MCPListResponse)
async def list_mcp_servers() -> MCPListResponse:
    """
    List all available MCP servers.
    
    In this implementation, tools are exposed as "servers" for consistency
    with the MCP protocol terminology.
    """
    servers = []
    
    for tool_id, tool_class in _available_tools.items():
        # Create temporary instance to get metadata
        tool = tool_class()
        
        servers.append(
            MCPServer(
                server_id=tool_id,
                name=tool.name,
                description=tool.description,
                version="1.0.0",
                status="active",
                capabilities=tool.capabilities,
            )
        )
    
    return MCPListResponse(
        servers=servers,
        tools=None,
        total=len(servers),
    )


@router.get("/tools", response_model=MCPListResponse)
async def list_mcp_tools() -> MCPListResponse:
    """
    List all available MCP tools with their metadata.
    """
    tools = []
    
    for tool_id, tool_class in _available_tools.items():
        tool = tool_class()
        
        tools.append(
            MCPToolInfo(
                tool_id=tool_id,
                name=tool.name,
                description=tool.description,
                parameters=tool.get_parameters(),
                examples=getattr(tool, "examples", []),
            )
        )
    
    return MCPListResponse(
        servers=None,
        tools=tools,
        total=len(tools),
    )


@router.get("/tools/{tool_id}", response_model=MCPToolInfo)
async def get_mcp_tool(tool_id: str) -> MCPToolInfo:
    """
    Get detailed information about a specific MCP tool.
    """
    if tool_id not in _available_tools:
        raise HTTPException(status_code=404, detail="Tool not found")
    
    tool = get_tool_instance(tool_id)
    
    return MCPToolInfo(
        tool_id=tool_id,
        name=tool.name,
        description=tool.description,
        parameters=tool.get_parameters(),
        examples=getattr(tool, "examples", []),
    )


@router.post("/execute", response_model=MCPExecuteResponse)
async def execute_mcp_tool(request: MCPExecuteRequest) -> MCPExecuteResponse:
    """
    Execute an MCP tool with provided parameters.
    
    This endpoint allows direct invocation of MCP tools for testing
    and development purposes.
    """
    import time
    
    start_time = time.time()
    
    try:
        tool = get_tool_instance(request.tool_id)
        
        # Validate parameters
        validation_result = await tool.validate_params(request.params)
        if not validation_result["valid"]:
            return MCPExecuteResponse(
                tool_id=request.tool_id,
                success=False,
                result=None,
                error=validation_result.get("error", "Invalid parameters"),
                execution_time_ms=(time.time() - start_time) * 1000,
            )
        
        # Execute tool
        result = await tool.execute(request.params)
        
        return MCPExecuteResponse(
            tool_id=request.tool_id,
            success=True,
            result=result,
            error=None,
            execution_time_ms=(time.time() - start_time) * 1000,
        )
        
    except Exception as e:
        return MCPExecuteResponse(
            tool_id=request.tool_id,
            success=False,
            result=None,
            error=str(e),
            execution_time_ms=(time.time() - start_time) * 1000,
        )


@router.post("/servers/{server_id}/start")
async def start_mcp_server(server_id: str) -> dict[str, Any]:
    """
    Start an MCP server (tool).
    
    In this implementation, tools are lazy-loaded, so this
    ensures the tool instance is initialized.
    """
    if server_id not in _available_tools:
        raise HTTPException(status_code=404, detail="Server not found")
    
    tool = get_tool_instance(server_id)
    
    return {
        "server_id": server_id,
        "name": tool.name,
        "status": "active",
        "message": "Server is active",
    }


@router.post("/servers/{server_id}/stop")
async def stop_mcp_server(server_id: str) -> dict[str, Any]:
    """
    Stop an MCP server (tool).
    
    Removes the tool instance from the active pool.
    """
    if server_id not in _available_tools:
        raise HTTPException(status_code=404, detail="Server not found")
    
    if server_id in _active_tools:
        del _active_tools[server_id]
    
    return {
        "server_id": server_id,
        "status": "stopped",
        "message": "Server stopped successfully",
    }


@router.get("/servers/{server_id}/status")
async def get_mcp_server_status(server_id: str) -> dict[str, Any]:
    """
    Get status of an MCP server (tool).
    """
    if server_id not in _available_tools:
        raise HTTPException(status_code=404, detail="Server not found")
    
    is_active = server_id in _active_tools
    
    return {
        "server_id": server_id,
        "status": "active" if is_active else "stopped",
        "uptime_seconds": 0 if not is_active else 0,  # Could track this
    }

