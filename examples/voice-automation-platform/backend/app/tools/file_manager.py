"""File manager tool for file operations."""

import os
from pathlib import Path
from typing import Any

from .base import MCPTool, ToolResult


class FileManagerTool(MCPTool):
    """
    File manager tool for file system operations.
    
    Features:
    - Read/write files
    - List directories
    - Create directories
    - Delete files/directories
    - Safe path validation
    """

    def __init__(self, base_path: str = "/tmp/voice-automation"):
        """Initialize with base path for safety."""
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    @property
    def name(self) -> str:
        """Tool name."""
        return "file_manager"

    @property
    def description(self) -> str:
        """Tool description."""
        return "Manage files and directories safely within workspace"

    async def execute(self, **kwargs) -> ToolResult:
        """
        Execute a file operation.
        
        Args:
            operation: Operation type (read, write, list, create_dir, delete)
            path: File/directory path
            content: Content for write operation
            
        Returns:
            ToolResult with operation outcome
        """
        operation = kwargs.get("operation")
        path = kwargs.get("path")

        if not operation:
            return ToolResult(success=False, error="No operation specified")
        
        if not path:
            return ToolResult(success=False, error="No path specified")

        # Validate path
        safe_path = self._get_safe_path(path)
        if not safe_path:
            return ToolResult(
                success=False,
                error=f"Invalid or unsafe path: {path}",
            )

        try:
            if operation == "read":
                return await self._read_file(safe_path)
            elif operation == "write":
                content = kwargs.get("content", "")
                return await self._write_file(safe_path, content)
            elif operation == "list":
                return await self._list_directory(safe_path)
            elif operation == "create_dir":
                return await self._create_directory(safe_path)
            elif operation == "delete":
                return await self._delete_path(safe_path)
            else:
                return ToolResult(
                    success=False,
                    error=f"Unknown operation: {operation}",
                )

        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Operation failed: {str(e)}",
                data={"operation": operation, "path": str(safe_path)},
            )

    def _get_safe_path(self, path: str) -> Path | None:
        """
        Validate and resolve path within base directory.
        
        Args:
            path: Requested path
            
        Returns:
            Safe resolved path or None if invalid
        """
        try:
            # Resolve path relative to base
            if path.startswith("/"):
                requested = Path(path)
            else:
                requested = self.base_path / path

            resolved = requested.resolve()

            # Ensure within base path
            if self.base_path in resolved.parents or resolved == self.base_path:
                return resolved

            return None

        except Exception:
            return None

    async def _read_file(self, path: Path) -> ToolResult:
        """Read file content."""
        if not path.is_file():
            return ToolResult(
                success=False,
                error=f"File not found: {path}",
            )

        content = path.read_text()
        return ToolResult(
            success=True,
            data={
                "content": content,
                "path": str(path),
                "size": len(content),
            },
        )

    async def _write_file(self, path: Path, content: str) -> ToolResult:
        """Write content to file."""
        # Create parent directories
        path.parent.mkdir(parents=True, exist_ok=True)
        
        path.write_text(content)
        
        return ToolResult(
            success=True,
            data={
                "path": str(path),
                "size": len(content),
            },
        )

    async def _list_directory(self, path: Path) -> ToolResult:
        """List directory contents."""
        if not path.is_dir():
            return ToolResult(
                success=False,
                error=f"Not a directory: {path}",
            )

        items = []
        for item in path.iterdir():
            items.append({
                "name": item.name,
                "path": str(item),
                "type": "directory" if item.is_dir() else "file",
                "size": item.stat().st_size if item.is_file() else 0,
            })

        return ToolResult(
            success=True,
            data={
                "path": str(path),
                "items": items,
                "count": len(items),
            },
        )

    async def _create_directory(self, path: Path) -> ToolResult:
        """Create directory."""
        path.mkdir(parents=True, exist_ok=True)
        
        return ToolResult(
            success=True,
            data={"path": str(path)},
        )

    async def _delete_path(self, path: Path) -> ToolResult:
        """Delete file or directory."""
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            import shutil
            shutil.rmtree(path)
        else:
            return ToolResult(
                success=False,
                error=f"Path not found: {path}",
            )

        return ToolResult(
            success=True,
            data={"path": str(path)},
        )

    def _get_parameters_schema(self) -> dict[str, Any]:
        """Get parameter schema for this tool."""
        return {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "description": "File operation to perform",
                    "enum": ["read", "write", "list", "create_dir", "delete"],
                },
                "path": {
                    "type": "string",
                    "description": "File or directory path",
                },
                "content": {
                    "type": "string",
                    "description": "Content for write operation",
                },
            },
            "required": ["operation", "path"],
        }

