"""CLI command execution tool (Step 11)."""

import os
import subprocess
from typing import Any


class CLITool:
    """Tool for executing CLI commands safely."""

    def __init__(self):
        self.allowed = os.getenv("ALLOW_CLI_EXECUTION", "false").lower() == "true"

    def execute(self, command: str) -> dict[str, Any]:
        """Execute a CLI command.
        
        Args:
            command: Shell command to execute
            
        Returns:
            Dict with stdout, stderr, return_code
        """
        if not self.allowed:
            return {
                "error": "CLI execution disabled",
                "hint": "Set ALLOW_CLI_EXECUTION=true to enable"
            }
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
                "success": result.returncode == 0
            }
        
        except subprocess.TimeoutExpired:
            return {"error": "Command timed out (30s limit)"}
        except Exception as e:
            return {"error": str(e)}

