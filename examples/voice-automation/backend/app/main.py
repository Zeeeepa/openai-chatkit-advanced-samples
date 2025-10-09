"""FastAPI server for Voice Automation."""

import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.memory_store import MemoryStore
from app.voice_agent import VoiceAgent

# Load environment variables
load_dotenv()


# Global state
store = None
agent = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for FastAPI app."""
    global store, agent
    
    # Startup
    print("🚀 Starting Voice Automation Server...")
    
    # Initialize store
    store = MemoryStore()
    print("✅ MemoryStore initialized")
    
    # Initialize agent (tools will be added in Step 9)
    agent = VoiceAgent(store=store, tools=[])
    print("✅ VoiceAgent initialized")
    
    print("🎉 Server ready!")
    
    yield
    
    # Shutdown
    print("👋 Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Voice Automation API",
    description="Voice-controlled automation platform",
    version="0.1.0",
    lifespan=lifespan,
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "Voice Automation API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "store": "initialized" if store else "not initialized",
        "agent": "initialized" if agent else "not initialized"
    }


@app.post("/api/voice")
async def process_voice(data: dict):
    """Process a voice message.
    
    Expected payload:
    {
        "thread_id": "optional-thread-id",
        "message": "transcribed voice text",
        "context": {}
    }
    """
    if not agent:
        return JSONResponse(
            status_code=503,
            content={"error": "Agent not initialized"}
        )
    
    try:
        message = data.get("message", "")
        context = data.get("context", {})
        
        # Validate message first
        if not message:
            return JSONResponse(
                status_code=400,
                content={"error": "Message is required"}
            )
        
        # Generate thread_id after validation
        thread_id = data.get("thread_id", store.generate_thread_id({}))
        
        # Process message
        response = await agent.process_message(
            thread_id=thread_id,
            message=message,
            context=context
        )
        
        return {
            "thread_id": thread_id,
            "response": response,
            "status": "success"
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8001))
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True,
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )
