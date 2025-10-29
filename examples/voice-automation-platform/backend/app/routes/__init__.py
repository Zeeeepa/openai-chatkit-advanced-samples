"""API routes for Voice Automation Platform."""

from .voice import router as voice
from .tasks import router as tasks
from .agents import router as agents
from .mcp import router as mcp
from .websocket import router as websocket

__all__ = ["voice", "tasks", "agents", "mcp", "websocket"]

