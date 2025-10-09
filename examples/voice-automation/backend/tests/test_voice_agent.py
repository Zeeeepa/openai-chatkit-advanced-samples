"""Tests for VoiceAgent."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timezone

from app.voice_agent import VoiceAgent
from app.memory_store import MemoryStore


@pytest.fixture
def mock_store():
    """Create a mock store."""
    return MemoryStore()


@pytest.fixture
def mock_tools():
    """Create mock tools."""
    return []


def test_voice_agent_initialization(mock_store, mock_tools):
    """Test VoiceAgent initialization."""
    with patch("app.voice_agent.Agent"):
        with patch("app.voice_agent.ChatKitServer"):
            agent = VoiceAgent(store=mock_store, tools=mock_tools)
            
            assert agent.store == mock_store
            assert agent.tools == mock_tools


def test_system_prompt_generation(mock_store):
    """Test system prompt is properly generated."""
    with patch("app.voice_agent.Agent"):
        with patch("app.voice_agent.ChatKitServer"):
            agent = VoiceAgent(store=mock_store)
            prompt = agent._get_system_prompt()
            
            assert "voice-controlled" in prompt.lower()
            assert "automation" in prompt.lower()
            assert "tools" in prompt.lower()


@pytest.mark.asyncio
async def test_process_message_string_response(mock_store):
    """Test processing message with string response."""
    with patch("app.voice_agent.Agent") as MockAgent:
        with patch("app.voice_agent.ChatKitServer"):
            # Mock agent response
            mock_agent_instance = MagicMock()
            mock_response = MagicMock()
            mock_response.content = "Task completed successfully"
            mock_agent_instance.run = AsyncMock(return_value=mock_response)
            MockAgent.return_value = mock_agent_instance
            
            agent = VoiceAgent(store=mock_store)
            
            response = await agent.process_message(
                thread_id="test_thread",
                message="Run tests",
                context={}
            )
            
            assert response == "Task completed successfully"
            mock_agent_instance.run.assert_called_once()


@pytest.mark.asyncio
async def test_process_message_list_response(mock_store):
    """Test processing message with list response."""
    with patch("app.voice_agent.Agent") as MockAgent:
        with patch("app.voice_agent.ChatKitServer"):
            # Mock agent response with list content
            mock_agent_instance = MagicMock()
            mock_response = MagicMock()
            mock_response.content = [
                {"type": "text", "text": "First part"},
                {"type": "text", "text": "Second part"}
            ]
            mock_agent_instance.run = AsyncMock(return_value=mock_response)
            MockAgent.return_value = mock_agent_instance
            
            agent = VoiceAgent(store=mock_store)
            
            response = await agent.process_message(
                thread_id="test_thread",
                message="Complex task",
                context={}
            )
            
            assert "First part" in response
            assert "Second part" in response


@pytest.mark.asyncio
async def test_process_message_fallback(mock_store):
    """Test fallback response when content format is unexpected."""
    with patch("app.voice_agent.Agent") as MockAgent:
        with patch("app.voice_agent.ChatKitServer"):
            # Mock agent response without content
            mock_agent_instance = MagicMock()
            mock_response = MagicMock(spec=[])  # No 'content' attribute
            mock_agent_instance.run = AsyncMock(return_value=mock_response)
            MockAgent.return_value = mock_agent_instance
            
            agent = VoiceAgent(store=mock_store)
            
            response = await agent.process_message(
                thread_id="test_thread",
                message="Test",
                context={}
            )
            
            assert response == "I processed your request."


def test_get_server(mock_store):
    """Test getting the ChatKit server instance."""
    with patch("app.voice_agent.Agent"):
        with patch("app.voice_agent.ChatKitServer") as MockServer:
            mock_server_instance = MagicMock()
            MockServer.return_value = mock_server_instance
            
            agent = VoiceAgent(store=mock_store)
            server = agent.get_server()
            
            assert server == mock_server_instance

