# 🎙️ Voice Automation Platform

Complete voice-to-voice automation platform built with ChatKit, enabling natural language control of system tasks, browser automation, testing, and research through an intuitive voice interface.

## ✨ Features

### 🗣️ Voice Interface
- **Web Speech API Integration** - Real-time voice-to-text
- **Text-to-Speech Responses** - Natural voice feedback
- **Continuous Listening Mode** - Hands-free operation
- **Command Recognition** - Intelligent intent parsing

### 🤖 Automation Capabilities
- **CLI Executor** - Run terminal commands with real-time output
- **Browser Automation** - Control browsers, capture screenshots
- **Test Runner** - Execute pytest suites with result visualization
- **Research Agent** - Autonomous web research with citations

### 📊 Task Management
- **Concurrent Tasks** - Run multiple automation tasks simultaneously
- **Progress Tracking** - Real-time progress widgets
- **Task History** - View all completed tasks
- **Cancel/Retry** - Full task lifecycle control

### 🔧 MCP Integration
- **MCP Dashboard** - Visual server management interface
- **Dynamic Installation** - Install MCP servers on-demand
- **Server Control** - Start/stop/configure servers
- **Tool Discovery** - Browse available MCP tools

## 🏗️ Architecture

```
Voice Input (Web Speech API)
    ↓
ChatKit Panel (React/Next.js)
    ├─ Voice Recording UI
    ├─ TTS Playback
    └─ Widget Rendering
    ↓
ChatKit Server (Python)
    ├─ VoiceAutomationAgent
    │   ├─ Intent Parser
    │   └─ Tool Orchestrator
    ├─ CLI Tool
    ├─ Browser Tool
    ├─ Test Runner Tool
    ├─ Research Agent Tool
    └─ MCP Manager
    ↓
Widgets & Actions
    ├─ Progress Widgets
    ├─ Task Manager Widget
    ├─ MCP Dashboard Widget
    └─ Results Visualization
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API Key
- Modern browser (Chrome/Edge for best voice support)

### Installation

1. **Clone and install dependencies:**
```bash
cd examples/voice-automation

# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

2. **Configure environment:**
```bash
# Backend .env
cp backend/.env.example backend/.env
# Add your OPENAI_API_KEY

# Frontend .env.local
cp frontend/.env.local.example frontend/.env.local
# Configure NEXT_PUBLIC_API_URL
```

3. **Run the application:**
```bash
# Terminal 1: Backend
cd backend
python -m app.main

# Terminal 2: Frontend
cd frontend
npm run dev
```

4. **Open browser:**
```
http://localhost:3000
```

## 🎯 Usage Examples

### Voice Commands

**CLI Execution:**
```
"Run ls -la in the terminal"
"Execute npm install"
"Show me the directory structure"
```

**Browser Automation:**
```
"Open github.com and take a screenshot"
"Navigate to example.com and click the login button"
"Fill out the form on the current page"
```

**Testing:**
```
"Run all tests in the tests directory"
"Execute pytest with coverage"
"Run unit tests for the authentication module"
```

**Research:**
```
"Research the latest ChatKit features"
"Find documentation about OpenAI Agents SDK"
"Search for Python async best practices"
```

**Task Management:**
```
"Show me all running tasks"
"Cancel task #3"
"Create a new task to analyze the codebase"
```

**MCP Management:**
```
"Show MCP servers"
"Install the browser automation MCP"
"Start the filesystem server"
```

## 📁 Project Structure

```
voice-automation/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI server
│   │   ├── agent.py             # VoiceAutomationAgent
│   │   ├── store.py             # In-memory Store
│   │   └── tools/
│   │       ├── __init__.py
│   │       ├── cli.py           # CLI executor
│   │       ├── browser.py       # Browser automation
│   │       ├── test_runner.py   # Pytest runner
│   │       ├── research.py      # Research agent
│   │       └── mcp_manager.py   # MCP integration
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── app/
│   │   ├── page.tsx             # Main page
│   │   └── api/
│   │       └── create-session/
│   │           └── route.ts     # Session endpoint
│   ├── components/
│   │   ├── ChatKitPanel.tsx     # ChatKit integration
│   │   └── VoiceInterface.tsx   # Voice UI
│   ├── package.json
│   └── .env.local.example
└── README.md
```

## 🔧 Configuration

### Backend Configuration (backend/.env)

```env
OPENAI_API_KEY=sk-...
MODEL=gpt-4o
LOG_LEVEL=INFO
ALLOW_DANGEROUS_CODE=false  # Set true to enable CLI execution
```

### Frontend Configuration (frontend/.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CHATKIT_WORKFLOW_ID=wf_...
```

## 🎨 Custom Widgets

This example demonstrates custom ChatKit widgets:

### Task Manager Widget
- View all concurrent tasks
- Monitor task progress
- Cancel/retry tasks
- Task history viewer

### MCP Dashboard Widget
- List installed MCP servers
- Server status indicators
- Quick start/stop controls
- Install from registry

### Progress Widget
- Real-time progress bars
- Step-by-step execution
- Error handling
- Completion notifications

## 🛡️ Security Considerations

**CLI Execution:**
- Disabled by default
- Requires explicit opt-in via environment variable
- Command validation and sanitization
- Restricted to safe commands in production

**Browser Automation:**
- Sandboxed browser contexts
- No access to sensitive sites by default
- Screenshot sanitization

**MCP Servers:**
- Install from trusted registry only
- Server permissions are configurable
- Isolated execution contexts

## 🧪 Testing

```bash
# Run backend tests
cd backend
pytest tests/ -v

# Run frontend tests
cd frontend
npm test

# End-to-end tests
npm run test:e2e
```

## 📚 Learn More

- [ChatKit Python Documentation](https://openai.github.io/chatkit-python/)
- [ChatKit React Documentation](https://github.com/openai/chatkit-react)
- [OpenAI Agents SDK](https://github.com/openai/agents-sdk)
- [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)

## 🤝 Contributing

This is an example project in the ChatKit Advanced Samples repository. Feel free to:
- Report issues
- Suggest improvements
- Submit pull requests
- Share your voice automation workflows!

## 📝 License

MIT License - See [LICENSE](../../LICENSE) for details.

## 🙏 Acknowledgments

Built with:
- [ChatKit](https://github.com/openai/chatkit) - Chat interface SDK
- [OpenAI Agents SDK](https://github.com/openai/agents-sdk) - Agent framework
- [Playwright](https://playwright.dev/) - Browser automation
- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [Next.js](https://nextjs.org/) - Frontend framework

---

**Ready to automate with voice?** Start the servers and say "Hello!" 🎤

