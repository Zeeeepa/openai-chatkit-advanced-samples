"""
Voice Automation Platform - FastAPI Backend
"""

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import settings
from .routes import voice, tasks, agents, mcp, websocket
from .webhooks import get_webhook_manager, register_default_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for the FastAPI application.
    
    Handles startup and shutdown events:
    - Start webhook event processor
    - Initialize connections
    - Cleanup on shutdown
    """
    print("=" * 80)
    print("🚀 Voice Automation Platform Starting...")
    print("=" * 80)
    
    # Startup: Initialize webhook manager
    webhook_manager = get_webhook_manager()
    register_default_handlers(webhook_manager)
    await webhook_manager.start()
    print("✓ Webhook system initialized")
    
    # Startup: Log configuration
    print(f"✓ Environment: {'Development' if settings.debug else 'Production'}")
    print(f"✓ Voice Input: {'Enabled' if settings.enable_voice_input else 'Disabled'}")
    print(f"✓ Webhooks: {'Enabled' if settings.enable_webhooks else 'Disabled'}")
    print(f"✓ API URL: http://{settings.host}:{settings.port}")
    print(f"✓ WebSocket URL: ws://{settings.host}:{settings.port}/ws")
    
    print("=" * 80)
    print("✅ Voice Automation Platform Ready!")
    print("=" * 80)
    
    yield
    
    # Shutdown: Cleanup
    print("\n" + "=" * 80)
    print("🛑 Voice Automation Platform Shutting Down...")
    print("=" * 80)
    
    await webhook_manager.stop()
    print("✓ Webhook system stopped")
    
    print("=" * 80)
    print("👋 Shutdown Complete")
    print("=" * 80)


# Create FastAPI application
app = FastAPI(
    title="Voice Automation Platform API",
    description="Multi-agent voice-controlled automation system",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Voice Automation Platform API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "docs": "/api/docs",
            "redoc": "/api/redoc",
            "openapi": "/api/openapi.json",
            "voice": "/api/voice",
            "tasks": "/api/tasks",
            "agents": "/api/agents",
            "mcp": "/api/mcp",
            "websocket": "/ws",
        },
    }


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "uptime": "operational",
    }


# API routes
app.include_router(voice.router, prefix="/api/voice", tags=["Voice"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(agents.router, prefix="/api/agents", tags=["Agents"])
app.include_router(mcp.router, prefix="/api/mcp", tags=["MCP"])
app.include_router(websocket.router, prefix="/ws", tags=["WebSocket"])


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors."""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not Found",
            "message": f"The requested resource was not found: {request.url.path}",
        },
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later.",
        },
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower(),
    )

