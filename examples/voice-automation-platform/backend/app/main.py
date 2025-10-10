"""FastAPI application for voice automation platform."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routes import agents, mcp, tasks, voice, websocket


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print(f"🚀 Starting {settings.APP_NAME}")
    print(f"📡 Server: {settings.HOST}:{settings.PORT}")
    print(f"🔑 OpenAI Model: {settings.OPENAI_MODEL}")
    
    yield
    
    # Shutdown
    print("👋 Shutting down gracefully")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Voice-controlled multi-agent automation platform",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(voice.router, prefix="/api/voice", tags=["voice"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(mcp.router, prefix="/api/mcp", tags=["mcp"])
app.include_router(websocket.router, prefix="/ws", tags=["websocket"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.VERSION,
    }

