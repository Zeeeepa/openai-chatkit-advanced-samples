"""Tests for FastAPI server."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock

from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_root_endpoint(client):
    """Test root endpoint returns service info."""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["service"] == "Voice Automation API"
    assert data["version"] == "0.1.0"
    assert data["status"] == "running"


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert "status" in data
    assert "store" in data
    assert "agent" in data


@pytest.mark.asyncio
async def test_process_voice_success():
    """Test successful voice message processing."""
    with patch("app.main.agent") as mock_agent:
        with patch("app.main.store") as mock_store:
            # Mock store
            mock_store.generate_thread_id = MagicMock(return_value="test_thread_1")
            
            # Mock agent
            mock_agent.process_message = AsyncMock(
                return_value="Tests completed successfully"
            )
            
            client = TestClient(app)
            
            response = client.post(
                "/api/voice",
                json={
                    "message": "Run the tests",
                    "context": {}
                }
            )
            
            assert response.status_code == 200
            
            data = response.json()
            assert data["status"] == "success"
            assert data["response"] == "Tests completed successfully"
            assert "thread_id" in data


@pytest.mark.asyncio
async def test_process_voice_with_thread_id():
    """Test voice processing with existing thread_id."""
    with patch("app.main.agent") as mock_agent:
        with patch("app.main.store"):
            # Mock agent
            mock_agent.process_message = AsyncMock(
                return_value="Continuing conversation"
            )
            
            client = TestClient(app)
            
            response = client.post(
                "/api/voice",
                json={
                    "thread_id": "existing_thread",
                    "message": "Follow up question",
                    "context": {}
                }
            )
            
            assert response.status_code == 200
            
            data = response.json()
            assert data["thread_id"] == "existing_thread"
            assert data["response"] == "Continuing conversation"


def test_process_voice_missing_message(client):
    """Test error when message is missing."""
    with patch("app.main.agent") as mock_agent:
        mock_agent.__bool__ = MagicMock(return_value=True)  # Agent is initialized
        
        response = client.post(
            "/api/voice",
            json={}
        )
        
        assert response.status_code == 400
        
        data = response.json()
        assert "error" in data
        assert "required" in data["error"].lower()


def test_process_voice_agent_not_initialized(client):
    """Test error when agent is not initialized."""
    with patch("app.main.agent", None):
        response = client.post(
            "/api/voice",
            json={"message": "Test"}
        )
        
        assert response.status_code == 503
        
        data = response.json()
        assert "error" in data
        assert "not initialized" in data["error"].lower()


@pytest.mark.asyncio
async def test_process_voice_error_handling():
    """Test error handling during message processing."""
    with patch("app.main.agent") as mock_agent:
        # Mock agent to raise exception
        mock_agent.process_message = AsyncMock(
            side_effect=Exception("Processing failed")
        )
        
        client = TestClient(app)
        
        response = client.post(
            "/api/voice",
            json={
                "message": "Test",
                "context": {}
            }
        )
        
        assert response.status_code == 500
        
        data = response.json()
        assert "error" in data

