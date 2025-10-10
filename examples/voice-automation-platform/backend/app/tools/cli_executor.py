"""CLI executor tool for running shell commands safely."""

import asyncio
import shlex
from typing import Any

from .base import MCPTool, ToolResult


class CLIExecutorTool(MCPTool):
    """
    CLI executor tool for running shell commands.
    
    Features:
    - Safe command execution with timeout
    - Output capture (stdout/stderr)
    - Return code tracking
    - Command validation
    """

    # Blacklisted commands for security
    BLACKLIST = [
        "rm -rf",
        "mkfs",
        "dd",
        "fork",
        ":()",
        ">",
        "wget",
        "curl",
    ]

    @property
    def name(self) -> str:
        """Tool name."""
        return "cli_executor"

    @property
    def description(self) -> str:
        """Tool description."""
        return "Execute shell commands safely with timeout and output capture"

    async def execute(self, **kwargs) -> ToolResult:
        """
        Execute a shell command.
        
        Args:
            command: Command to execute
            timeout: Timeout in seconds (default: 30)
            capture_output: Whether to capture output (default: True)
            
        Returns:
            ToolResult with command output
        """
        command = kwargs.get("command")
        timeout = kwargs.get("timeout", 30)
        capture_output = kwargs.get("capture_output", True)

        if not command:
            return ToolResult(
                success=False,
                error="No command provided",
            )

        # Validate command
        if not self._is_safe_command(command):
            return ToolResult(
                success=False,
                error=f"Command contains blacklisted operations: {command}",
            )

        try:
            # Execute command
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE if capture_output else None,
                stderr=asyncio.subprocess.PIPE if capture_output else None,
            )

            # Wait with timeout
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout,
            )

            return ToolResult(
                success=process.returncode == 0,
                data={
                    "stdout": stdout.decode() if stdout else "",
                    "stderr": stderr.decode() if stderr else "",
                    "return_code": process.returncode,
                    "command": command,
                },
                metadata={
                    "timeout": timeout,
                    "capture_output": capture_output,
                },
            )

        except asyncio.TimeoutError:
            return ToolResult(
                success=False,
                error=f"Command timed out after {timeout} seconds",
                data={"command": command},
            )
        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Command execution failed: {str(e)}",
                data={"command": command},
            )

    def _is_safe_command(self, command: str) -> bool:
        """
        Check if command is safe to execute.
        
        Args:
            command: Command to validate
            
        Returns:
            True if safe, False otherwise
        """
        command_lower = command.lower()
        
        # Check blacklist
        for blocked in self.BLACKLIST:
            if blocked in command_lower:
                return False
        
        return True

    def _get_parameters_schema(self) -> dict[str, Any]:
        """Get parameter schema for this tool."""
        return {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "Shell command to execute",
                },
                "timeout": {
                    "type": "integer",
                    "description": "Timeout in seconds",
                    "default": 30,
                },
                "capture_output": {
                    "type": "boolean",
                    "description": "Whether to capture stdout/stderr",
                    "default": True,
                },
            },
            "required": ["command"],
        }

