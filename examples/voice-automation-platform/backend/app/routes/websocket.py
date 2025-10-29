"""WebSocket endpoints for real-time updates."""

import asyncio
import json
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

router = APIRouter()

# Active WebSocket connections
_active_connections: list[WebSocket] = []


class WebSocketMessage(BaseModel):
    """WebSocket message format."""

    event: str
    data: dict[str, Any]
    timestamp: float


class ConnectionManager:
    """Manage WebSocket connections and broadcasts."""

    def __init__(self):
        """Initialize connection manager."""
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: dict[str, Any], websocket: WebSocket):
        """Send a message to a specific connection."""
        try:
            await websocket.send_json(message)
        except Exception:
            # Connection closed, remove it
            self.disconnect(websocket)

    async def broadcast(self, message: dict[str, Any]):
        """Broadcast a message to all connections."""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                # Mark for removal
                disconnected.append(connection)
        
        # Remove disconnected clients
        for conn in disconnected:
            self.disconnect(conn)

    async def broadcast_event(self, event: str, data: dict[str, Any]):
        """Broadcast an event with data to all connections."""
        message = {
            "event": event,
            "data": data,
            "timestamp": asyncio.get_event_loop().time(),
        }
        await self.broadcast(message)


# Global connection manager
manager = ConnectionManager()


@router.websocket("")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time updates.
    
    Clients connect here to receive real-time notifications about:
    - Task status changes
    - Agent spawning/completion
    - Tool execution events
    - System status updates
    
    Message format:
    {
        "event": "task_updated",
        "data": {...},
        "timestamp": 1234567890.123
    }
    """
    await manager.connect(websocket)
    
    try:
        # Send welcome message
        await websocket.send_json({
            "event": "connected",
            "data": {
                "message": "Connected to Voice Automation Platform",
                "version": "1.0.0",
            },
            "timestamp": asyncio.get_event_loop().time(),
        })
        
        # Keep connection alive and handle incoming messages
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                
                # Handle client messages
                if message.get("type") == "ping":
                    # Respond to ping
                    await websocket.send_json({
                        "event": "pong",
                        "data": {},
                        "timestamp": asyncio.get_event_loop().time(),
                    })
                
                elif message.get("type") == "subscribe":
                    # Client wants to subscribe to specific events
                    events = message.get("events", [])
                    await websocket.send_json({
                        "event": "subscribed",
                        "data": {"events": events},
                        "timestamp": asyncio.get_event_loop().time(),
                    })
                
                else:
                    # Echo unknown message types
                    await websocket.send_json({
                        "event": "unknown",
                        "data": {"received": message},
                        "timestamp": asyncio.get_event_loop().time(),
                    })
                    
            except json.JSONDecodeError:
                # Invalid JSON
                await websocket.send_json({
                    "event": "error",
                    "data": {"error": "Invalid JSON"},
                    "timestamp": asyncio.get_event_loop().time(),
                })
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        manager.disconnect(websocket)
        print(f"WebSocket error: {e}")


# Helper functions for broadcasting events (used by other routes)

async def broadcast_task_created(task_id: str, task_type: str, description: str):
    """Broadcast task creation event."""
    await manager.broadcast_event(
        "task_created",
        {
            "task_id": task_id,
            "type": task_type,
            "description": description,
        },
    )


async def broadcast_task_updated(task_id: str, status: str, result: Any = None):
    """Broadcast task update event."""
    await manager.broadcast_event(
        "task_updated",
        {
            "task_id": task_id,
            "status": status,
            "result": result,
        },
    )


async def broadcast_agent_spawned(agent_id: str, role: str, name: str):
    """Broadcast agent spawn event."""
    await manager.broadcast_event(
        "agent_spawned",
        {
            "agent_id": agent_id,
            "role": role,
            "name": name,
        },
    )


async def broadcast_agent_completed(agent_id: str, task_id: str, success: bool):
    """Broadcast agent completion event."""
    await manager.broadcast_event(
        "agent_completed",
        {
            "agent_id": agent_id,
            "task_id": task_id,
            "success": success,
        },
    )


async def broadcast_tool_executed(tool_id: str, success: bool, execution_time_ms: float):
    """Broadcast tool execution event."""
    await manager.broadcast_event(
        "tool_executed",
        {
            "tool_id": tool_id,
            "success": success,
            "execution_time_ms": execution_time_ms,
        },
    )


# Export manager and broadcast functions
__all__ = [
    "router",
    "manager",
    "broadcast_task_created",
    "broadcast_task_updated",
    "broadcast_agent_spawned",
    "broadcast_agent_completed",
    "broadcast_tool_executed",
]

