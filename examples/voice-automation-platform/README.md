# 🎙️ Voice Automation Platform

A production-ready, voice-controlled multi-agent automation system powered by OpenAI ChatKit and FastAPI.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Examples](#examples)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

## 🌟 Overview

Voice Automation Platform enables you to control a sophisticated multi-agent AI system using natural voice commands. The system coordinates specialized agents that work together to accomplish complex tasks like research, code generation, testing, and more.

### Key Capabilities

- 🎤 **Voice Control**: Natural language commands to trigger automation
- 🤖 **Multi-Agent System**: 4 specialized agents working collaboratively
- 🔧 **MCP Tools**: Extensible tool system (CLI, Web Search, File Manager)
- 🔄 **Real-time Updates**: WebSocket-based live progress tracking
- 📡 **Event-Driven**: Webhook system for agent communication
- 🎨 **Modern UI**: Responsive Next.js dashboard

## ✨ Features

### Backend (FastAPI)
- ✅ **Multi-Agent Orchestration**: Main agent coordinates specialized sub-agents
- ✅ **4 Specialized Agents**:
  - **Orchestrator**: Plans and coordinates complex workflows
  - **Research**: Gathers information and analyzes data
  - **Code**: Generates, reviews, and tests code
  - **Validator**: Ensures quality and correctness
- ✅ **3 MCP Tools**:
  - **CLI Executor**: Run system commands safely
  - **Web Search**: Search and scrape web content
  - **File Manager**: Read, write, and manage files
- ✅ **REST API**: 20+ endpoints for complete system control
- ✅ **WebSocket**: Real-time task and agent status updates
- ✅ **Webhook System**: Event-driven inter-agent communication
- ✅ **Memory Store**: Persistent conversation and result storage

### Frontend (Next.js 14)
- ✅ **Voice Interface**: Speech-to-text command input
- ✅ **Task Dashboard**: Real-time task monitoring and statistics
- ✅ **Agent Monitor**: Live agent status and management
- ✅ **MCP Manager**: Browse and execute tools
- ✅ **Responsive Design**: Mobile-friendly interface
- ✅ **WebSocket Integration**: Live updates without refresh

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Voice Interface (UI)                     │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Voice Input  │  │ Task Monitor │  │ Agent Status │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└───────────────────────────────┬─────────────────────────────┘
                                │
                        WebSocket / REST API
                                │
┌───────────────────────────────┴─────────────────────────────┐
│                     FastAPI Backend                          │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              Main Agent (Orchestrator)                  │ │
│  │                                                          │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐            │ │
│  │  │ Research │  │   Code   │  │Validator │            │ │
│  │  │  Agent   │  │  Agent   │  │  Agent   │            │ │
│  │  └─────┬────┘  └─────┬────┘  └─────┬────┘            │ │
│  └────────┼─────────────┼─────────────┼──────────────────┘ │
│           │             │             │                      │
│  ┌────────┴─────────────┴─────────────┴──────────────────┐ │
│  │                    MCP Tools                            │ │
│  │                                                          │ │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐       │ │
│  │  │    CLI     │  │    Web     │  │    File    │       │ │
│  │  │  Executor  │  │   Search   │  │  Manager   │       │ │
│  │  └────────────┘  └────────────┘  └────────────┘       │ │
│  └──────────────────────────────────────────────────────────┘ │
│                                                               │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │                  Webhook System                          │ │
│  │  (Event-driven agent communication)                      │ │
│  └──────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Voice Command** → User speaks command to frontend
2. **API Request** → Frontend sends command to `/api/voice/command`
3. **Task Creation** → Backend creates task and assigns to main agent
4. **Agent Orchestration** → Main agent spawns specialized sub-agents
5. **Tool Execution** → Agents use MCP tools to accomplish subtasks
6. **Webhook Events** → Agents emit events as they complete work
7. **WebSocket Updates** → Frontend receives real-time progress updates
8. **Result Delivery** → Completed task result returned to user

## 🚀 Quick Start

### Prerequisites

- Python 3.9+ 
- Node.js 18+
- OpenAI API key

### One-Command Setup

**Unix/Linux/macOS:**
```bash
./setup.sh
```

**Windows (PowerShell):**
```powershell
.\setup.ps1
```

### Start Development Servers

**Unix/Linux/macOS:**
```bash
./dev-start.sh
```

**Windows (PowerShell):**
```powershell
.\dev-start.ps1
```

Then open:
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/api/docs

## 📦 Installation

### Manual Installation

#### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Unix/Linux/macOS
# OR
.\venv\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Edit .env.local if needed
```

## ⚙️ Configuration

### Backend Configuration (`.env`)

```env
# Required
OPENAI_API_KEY=sk-your-key-here

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True

# Features
ENABLE_VOICE_INPUT=True
ENABLE_WEBHOOKS=True

# See backend/.env.example for all options
```

### Frontend Configuration (`.env.local`)

```env
# API URLs
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws

# Features
NEXT_PUBLIC_VOICE_ENABLED=true
NEXT_PUBLIC_DEFAULT_LANGUAGE=en-US

# See frontend/.env.example for all options
```

## 🎯 Usage

### Voice Commands

Simply speak or type commands like:

- "Research the latest trends in AI agents and create a report"
- "Review the code in the utils directory"
- "Scrape the latest AI news from TechCrunch and summarize"
- "Process all JSON files in the data directory"
- "Create a REST API for a todo application with tests"

### Programmatic API

```python
import httpx

# Send voice command
response = httpx.post(
    "http://localhost:8000/api/voice/command",
    json={
        "command": "Research AI trends and create a summary",
        "language": "en-US"
    }
)

task_id = response.json()["task_id"]

# Check task status
status = httpx.get(f"http://localhost:8000/api/tasks/{task_id}")
print(status.json())
```

### WebSocket Connection

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log('Event:', message.event, message.data);
};

// Subscribe to specific events
ws.send(JSON.stringify({
  type: 'subscribe',
  events: ['task_updated', 'agent_spawned']
}));
```

## 📚 API Documentation

### Endpoints

#### Voice Control
- `POST /api/voice/command` - Send voice command
- `GET /api/voice/status` - Voice service status
- `GET /api/voice/tasks/{id}` - Get voice task status

#### Task Management
- `GET /api/tasks` - List all tasks
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{id}` - Get task details
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Cancel task
- `GET /api/tasks/stats` - Task statistics

#### Agent Management
- `GET /api/agents` - List all agents
- `POST /api/agents` - Spawn new agent
- `GET /api/agents/{id}` - Get agent details
- `GET /api/agents/{id}/status` - Agent status
- `DELETE /api/agents/{id}` - Remove agent
- `GET /api/agents/stats` - Agent statistics

#### MCP Tools
- `GET /api/mcp/tools` - List all tools
- `GET /api/mcp/tools/{id}` - Tool details
- `POST /api/mcp/execute` - Execute tool
- `GET /api/mcp/servers` - List MCP servers
- `POST /api/mcp/servers/{id}/start` - Start server
- `POST /api/mcp/servers/{id}/stop` - Stop server

#### WebSocket
- `WS /ws` - WebSocket connection for real-time updates

### Interactive API Docs

Visit http://localhost:8000/api/docs for interactive Swagger UI documentation.

## 💡 Examples

We provide 5 complete workflow examples:

1. **Research Report** (`workflow_01_research_report.py`)
   - Demonstrates research and report generation
   
2. **Code Review** (`workflow_02_code_review.py`)
   - Automated code quality analysis
   
3. **Web Scraping** (`workflow_03_web_scraping.py`)
   - Web data extraction and analysis
   
4. **File Processing** (`workflow_04_file_processing.py`)
   - Batch file operations
   
5. **Multi-Agent Project** (`workflow_05_multi_agent.py`)
   - Complex multi-agent collaboration

Run any example:
```bash
cd examples
python workflow_01_research_report.py
```

## 🛠️ Development

### Running Tests

```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend tests
cd frontend
npm test
```

### Code Quality

```bash
# Backend linting
cd backend
ruff check .
black .
mypy .

# Frontend linting
cd frontend
npm run lint
npm run format
```

### Project Structure

```
voice-automation-platform/
├── backend/
│   ├── app/
│   │   ├── agents/          # AI agents
│   │   ├── tools/           # MCP tools
│   │   ├── routes/          # API endpoints
│   │   ├── webhooks/        # Webhook system
│   │   ├── config.py        # Configuration
│   │   └── main.py          # FastAPI app
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── app/             # Next.js pages
│   │   ├── components/      # React components
│   │   ├── lib/             # Utilities
│   │   └── hooks/           # React hooks
│   ├── package.json
│   └── .env.example
├── examples/                # Workflow examples
├── setup.sh                 # Unix setup script
├── setup.ps1                # Windows setup script
├── dev-start.sh             # Unix dev launcher
├── dev-start.ps1            # Windows dev launcher
└── README.md
```

## 🐛 Troubleshooting

### Common Issues

**Backend won't start:**
```bash
# Check Python version
python3 --version  # Should be 3.9+

# Verify virtual environment
source backend/venv/bin/activate
which python  # Should point to venv

# Check dependencies
pip install -r backend/requirements.txt
```

**Frontend won't start:**
```bash
# Check Node version
node --version  # Should be 18+

# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**OpenAI API errors:**
```bash
# Verify API key in backend/.env
grep OPENAI_API_KEY backend/.env

# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**WebSocket connection fails:**
- Ensure backend is running on port 8000
- Check `NEXT_PUBLIC_WS_URL` in frontend/.env.local
- Verify no firewall blocking WebSocket connections

### Debug Mode

Enable debug logging:

```env
# backend/.env
DEBUG=True
LOG_LEVEL=DEBUG

# frontend/.env.local
NEXT_PUBLIC_ENABLE_DEBUG=true
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- OpenAI ChatKit for the agent framework
- FastAPI for the backend framework
- Next.js for the frontend framework
- The open source community

## 📞 Support

For issues and questions:
- Open a GitHub issue
- Check the troubleshooting guide
- Review API documentation at `/api/docs`

---

**Built with ❤️ using OpenAI ChatKit, FastAPI, and Next.js**

