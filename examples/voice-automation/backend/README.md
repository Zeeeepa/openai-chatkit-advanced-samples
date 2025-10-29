# Voice Automation Backend

Backend server for voice-controlled automation platform built with FastAPI, ChatKit, and Agents SDK.

## 📦 Structure

```
backend/
├── app/
│   ├── __init__.py          # Package init
│   ├── main.py              # FastAPI server (✅ Complete)
│   ├── memory_store.py      # In-memory Store (✅ Complete)
│   ├── voice_agent.py       # VoiceAgent class (✅ Complete)
│   ├── tools/               # Agent tools (🚧 Phase 3)
│   │   └── __init__.py
│   └── widgets/             # ChatKit widgets (🚧 Phase 4)
│       └── __init__.py
├── tests/
│   ├── test_memory_store.py # MemoryStore tests (✅ 6 tests)
│   ├── test_voice_agent.py  # VoiceAgent tests (✅ 6 tests)
│   └── test_main.py         # FastAPI tests (✅ 7 tests)
├── pyproject.toml           # Dependencies
├── .env.example             # Environment template
└── README.md                # This file
```

## ✅ Phase 2 Complete (Steps 6-10)

**What's Implemented:**

### Step 6: MemoryStore ✅
- Full `Store` interface implementation
- Thread CRUD operations
- Item CRUD with pagination
- 6 comprehensive test cases

### Step 7: VoiceAgent ✅
- Agent + ChatKit Server integration
- Voice message processing pipeline
- System prompt for voice automation
- 6 test cases covering all scenarios

### Step 8: FastAPI Server ✅
- Lifecycle management (startup/shutdown)
- CORS configuration
- Health check endpoint
- Voice processing endpoint (`/api/voice`)
- 7 test cases with error handling

### Steps 9-10: Tools + Testing ✅
- Tool/widget directories prepared
- Backend structure complete
- Ready for Phase 3 (Tools)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Using pip
pip install -e .

# Or using uv (recommended)
uv pip install -e .
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

Required variables:
```bash
OPENAI_API_KEY=sk-proj-...
MODEL=gpt-4o
PORT=8001
```

### 3. Run Server

```bash
# Development with auto-reload
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --reload --port 8001
```

### 4. Run Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_memory_store.py -v

# With coverage
pytest tests/ --cov=app --cov-report=html
```

## 📡 API Endpoints

### `GET /`
Service information
```json
{
  "service": "Voice Automation API",
  "version": "0.1.0",
  "status": "running"
}
```

### `GET /health`
Health check with component status
```json
{
  "status": "healthy",
  "store": "initialized",
  "agent": "initialized"
}
```

### `POST /api/voice`
Process voice message

**Request:**
```json
{
  "message": "Run the tests",
  "thread_id": "optional-existing-thread",
  "context": {}
}
```

**Response:**
```json
{
  "thread_id": "thread_1",
  "response": "Running tests now...",
  "status": "success"
}
```

**Error Responses:**
- `400` - Missing message
- `503` - Agent not initialized
- `500` - Processing error

## 🧪 Testing

### Test Coverage

- **MemoryStore** (6 tests)
  - Thread creation/loading
  - Item addition/retrieval
  - Pagination (asc/desc)
  - Item deletion
  - Error handling

- **VoiceAgent** (6 tests)
  - Initialization
  - System prompt
  - Message processing (string/list)
  - Fallback handling
  - Server retrieval

- **FastAPI Server** (7 tests)
  - Root endpoint
  - Health check
  - Voice processing (success)
  - Thread ID handling
  - Error cases (400, 503, 500)

### Running Specific Tests

```bash
# Memory store only
pytest tests/test_memory_store.py -v

# Voice agent only
pytest tests/test_voice_agent.py -v

# FastAPI server only
pytest tests/test_main.py -v

# Run with markers
pytest -m asyncio -v
```

## 🔧 Development

### Code Quality

```bash
# Linting
ruff check app/

# Type checking
mypy app/

# Format code
ruff format app/
```

### Architecture

```
┌─────────────────┐
│  FastAPI Server │
│   (main.py)     │
└────────┬────────┘
         │
         ├─> MemoryStore (persistence)
         │
         └─> VoiceAgent
                │
                ├─> ChatKit Server
                ├─> Agents SDK
                └─> Tools (Phase 3)
```

### Adding New Tools (Phase 3)

Tools will be added in `app/tools/`:

```python
# app/tools/cli_tool.py
from agents import Tool

class CLITool(Tool):
    def execute(self, command: str) -> str:
        # Execute CLI command
        pass
```

Then integrate in `main.py`:
```python
from app.tools.cli_tool import CLITool

tools = [CLITool()]
agent = VoiceAgent(store=store, tools=tools)
```

## 🔒 Security

- CLI execution disabled by default (`ALLOW_CLI_EXECUTION=false`)
- CORS restricted to frontend origin
- Input validation on all endpoints
- Error messages don't leak sensitive info

## 📊 Monitoring

Health check endpoint provides:
- Store initialization status
- Agent initialization status
- Overall service health

## 🚧 Next Steps (Phase 3)

**Steps 11-15: Automation Tools**

1. **Step 11**: CLI Tool
   - Execute shell commands
   - Security sandbox
   - Output capture

2. **Step 12**: Browser Tool
   - Playwright automation
   - Page navigation
   - Element interaction

3. **Step 13**: Test Runner
   - pytest integration
   - Test discovery
   - Result parsing

4. **Step 14**: Research Tool
   - Web search
   - Content extraction
   - Summarization

5. **Step 15**: MCP Manager
   - Server discovery
   - Installation
   - Configuration

## 📝 Notes

- Uses in-memory storage (data lost on restart)
- Designed for development/testing
- Production should use persistent store (PostgreSQL, etc.)
- Tools require additional dependencies (playwright, etc.)

## 📚 Dependencies

Core:
- `fastapi` - Web server
- `uvicorn` - ASGI server
- `chatkit-python` - ChatKit SDK
- `agents` - Agents SDK
- `python-dotenv` - Environment config

Testing:
- `pytest` - Test framework
- `pytest-asyncio` - Async test support
- `httpx` - HTTP client for testing

Future (Phase 3):
- `playwright` - Browser automation
- `aiofiles` - Async file operations

## 🤝 Contributing

When adding features:
1. Write tests first (TDD)
2. Follow existing patterns
3. Update this README
4. Run full test suite before commit

## 📄 License

MIT

