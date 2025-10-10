# 🎤 Voice Automation Platform

> **A production-ready voice-to-voice AI automation platform powered by multi-agent orchestration and MCP tools**

Build sophisticated voice-controlled automation workflows where AI agents coordinate to complete complex tasks—from research and analysis to code execution and validation.

## 🌟 Features

### Voice-First Interface
- 🎙️ **Natural voice commands** using Web Speech API
- 🗣️ **Text-to-speech responses** for hands-free operation
- 🎯 **Intent recognition** to parse user requests

### Multi-Agent Orchestration
- 🤖 **Main Agent Creator** spawns specialized sub-agents on-demand
- 👥 **Coordinated workflows** where agents communicate via webhooks
- ✅ **Quality validation** through dedicated validator agents
- 📊 **Real-time progress tracking** for all running tasks

### MCP Tool Integration
- 🔧 **Extensible tool system** via Model Context Protocol
- 🌐 **Pre-built tools**: CLI executor, browser automation, research agent, test runner
- 📦 **Easy to add custom tools** through MCP servers
- 🎛️ **Dynamic server management** - add/remove tools on the fly

### Visual Dashboards
- 💬 **Chat Interface** - conversational interaction with agents
- 📋 **Task Manager** - monitor active, queued, and completed tasks
- 🖥️ **MCP Dashboard** - view and manage connected tool servers
- 📈 **Analytics** - track agent performance and resource usage

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                Voice Interface Layer                     │
│   Web Speech API  ◄──► React UI ◄──► Text-to-Speech    │
└─────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────┐
│          Agent Orchestration Layer (FastAPI)             │
│                                                           │
│   ┌─────────────────────────────────────────────────┐  │
│   │         Main Agent Creator                       │  │
│   │   • Parse voice commands                         │  │
│   │   • Spawn specialized sub-agents                 │  │
│   │   • Coordinate multi-agent workflows             │  │
│   │   • Aggregate and validate results               │  │
│   └─────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────┐
│              Sub-Agent Pool + MCP Tools                  │
│                                                           │
│   Agents:                    MCP Tools:                  │
│   • Research Agent           • CLI Executor              │
│   • Code Agent               • Browser Automation        │
│   • Data Agent               • Web Search                │
│   • Validator Agent          • File Manager              │
│   • Custom Agents            • Test Runner               │
│                              • Custom Tools              │
└─────────────────────────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────┐
│        Inter-Agent Communication (Webhooks)              │
│   • Task completion events                               │
│   • Progress updates                                     │
│   • Error notifications                                  │
│   • Result aggregation                                   │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- OpenAI API key
- Docker (optional, for MCP servers)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/voice-automation-platform.git
cd voice-automation-platform

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
npm install

# Configure environment
cp .env.example .env
# Edit .env with your OpenAI API key
```

### Run the Platform

```bash
# Terminal 1: Start backend
cd backend
uvicorn app.main:app --reload

# Terminal 2: Start frontend
cd frontend
npm run dev

# Terminal 3: Start MCP servers (optional)
cd backend/mcp_servers
python cli_executor_server.py
```

Open http://localhost:3000 in your browser and start talking!

## 📖 Usage

### Example 1: Research and Summarize
```
You: "Research the latest AI breakthroughs and create a summary"

System:
├─ [Research Agent] Searching for AI breakthroughs...
├─ [Research Agent] Found 15 relevant articles
├─ [Code Agent] Analyzing data patterns...
└─ [Validator Agent] ✓ Quality check passed

Response: [Comprehensive summary with sources]
```

### Example 2: Code Generation and Testing
```
You: "Create a REST API for user management and test it"

System:
├─ [Code Agent] Generating FastAPI endpoints...
├─ [Code Agent] Writing test cases...
├─ [CLI Executor] Running pytest...
└─ [Validator Agent] ✓ All 12 tests passed

Response: [Code + test results + deployment instructions]
```

### Example 3: Web Automation
```
You: "Monitor GitHub trending repos and notify me of new Python projects"

System:
├─ [Browser Agent] Navigating to GitHub trending...
├─ [Browser Agent] Filtering Python repositories...
├─ [Data Agent] Comparing with previous data...
└─ [Validator Agent] ✓ Found 3 new projects

Response: [List of new Python projects with descriptions]
```

## 🎯 Core Concepts

### Agent Types

#### Main Agent Creator
The orchestrator that receives voice commands and coordinates all sub-agents.

```python
from app.agents import MainAgent

agent = MainAgent()
result = await agent.process_command("research latest AI news")
```

#### Specialized Sub-Agents
Each sub-agent has a specific purpose and can use MCP tools:

- **Research Agent**: Web search, article analysis, data gathering
- **Code Agent**: Code generation, refactoring, analysis
- **Data Agent**: Data processing, transformation, validation
- **Validator Agent**: Quality checks, test validation, result verification

### MCP Tools

Tools are integrated via Model Context Protocol servers:

```python
# app/tools/cli_executor.py
class CLIExecutorTool(MCPTool):
    name = "cli_executor"
    description = "Execute shell commands safely"
    
    async def execute(self, command: str) -> str:
        # Implementation
        pass
```

### Workflows

Define multi-step automation workflows:

```python
# Example workflow definition
workflow = Workflow(
    name="research_and_write",
    steps=[
        Step(agent="research", action="search", params={"query": "..."}),
        Step(agent="research", action="analyze", depends_on=[0]),
        Step(agent="code", action="generate_report", depends_on=[1]),
        Step(agent="validator", action="review", depends_on=[2]),
    ]
)
```

## 🔧 Configuration

### Environment Variables

```bash
# .env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4
WEBHOOK_BASE_URL=http://localhost:8000
MCP_SERVER_DIR=./mcp_servers
ENABLE_VOICE_INPUT=true
ENABLE_VOICE_OUTPUT=true
LOG_LEVEL=INFO
```

### Agent Configuration

```yaml
# config/agents.yaml
agents:
  research:
    model: gpt-4
    temperature: 0.7
    max_tokens: 2000
    tools: [web_search, web_scraper]
  
  code:
    model: gpt-4
    temperature: 0.2
    max_tokens: 4000
    tools: [cli_executor, file_manager]
  
  validator:
    model: gpt-4
    temperature: 0.1
    max_tokens: 1000
    tools: [test_runner]
```

## 📚 API Reference

### REST Endpoints

```
POST   /api/v1/voice          - Process voice command
GET    /api/v1/tasks          - List all tasks
GET    /api/v1/tasks/{id}     - Get task details
DELETE /api/v1/tasks/{id}     - Cancel task
GET    /api/v1/agents         - List active agents
POST   /api/v1/agents/spawn   - Manually spawn agent
GET    /api/v1/mcp/servers    - List MCP servers
POST   /api/v1/mcp/servers    - Add MCP server
DELETE /api/v1/mcp/servers/{id} - Remove MCP server
```

### WebSocket Events

```javascript
// Connect to real-time updates
const ws = new WebSocket('ws://localhost:8000/ws');

// Event types
ws.on('task.created', (data) => { /* New task started */ });
ws.on('task.progress', (data) => { /* Progress update */ });
ws.on('task.completed', (data) => { /* Task finished */ });
ws.on('agent.spawned', (data) => { /* Sub-agent created */ });
ws.on('agent.message', (data) => { /* Inter-agent communication */ });
```

## 🧪 Testing

```bash
# Run backend tests
cd backend
pytest tests/ -v --cov=app

# Run frontend tests
cd frontend
npm test

# Run E2E tests
npm run test:e2e
```

## 🎨 Customization

### Adding a Custom Agent

```python
# app/agents/custom_agent.py
from app.agents.base import BaseAgent

class CustomAgent(BaseAgent):
    name = "custom"
    description = "Your custom agent"
    
    async def process(self, task: Task) -> Result:
        # Your implementation
        pass
```

### Adding a Custom MCP Tool

```python
# app/tools/custom_tool.py
from app.tools.base import MCPTool

class CustomTool(MCPTool):
    name = "custom_tool"
    description = "Your custom tool"
    
    async def execute(self, **params) -> dict:
        # Your implementation
        pass
```

### Creating a Custom Workflow

```python
# workflows/custom_workflow.py
from app.workflows import Workflow, Step

workflow = Workflow(
    name="custom_workflow",
    description="Your custom workflow",
    steps=[
        Step(agent="research", action="gather_data"),
        Step(agent="custom", action="process_data"),
        Step(agent="validator", action="validate"),
    ]
)
```

## 📖 Documentation

- [Architecture Guide](docs/ARCHITECTURE.md)
- [Agent Development](docs/AGENTS.md)
- [MCP Tool Integration](docs/MCP_TOOLS.md)
- [API Reference](docs/API.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## 🗺️ Roadmap

### Version 1.0 (Current)
- ✅ Basic voice input/output
- ✅ Multi-agent orchestration
- ✅ 4 core MCP tools
- ✅ Task management dashboard

### Version 1.1 (Q2 2025)
- ⏳ Advanced voice commands (interruptions, context)
- ⏳ Agent learning and optimization
- ⏳ Workflow templates marketplace
- ⏳ Performance analytics

### Version 2.0 (Q3 2025)
- 📋 Multi-user support
- 📋 Cloud deployment templates
- 📋 Mobile app (iOS/Android)
- 📋 Enterprise features (SSO, audit logs)

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Fork and clone the repo
git clone https://github.com/yourusername/voice-automation-platform.git
cd voice-automation-platform

# Create a feature branch
git checkout -b feature/amazing-feature

# Make your changes and commit
git commit -m "Add amazing feature"

# Push and create PR
git push origin feature/amazing-feature
```

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [ChatKit SDK](https://github.com/openai/chatkit-python)
- Powered by [OpenAI GPT-4](https://openai.com)
- MCP Protocol by [Anthropic](https://www.anthropic.com)
- Inspired by [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) and [LangChain](https://github.com/langchain-ai/langchain)

## 💬 Support

- 📧 Email: support@voiceautomation.dev
- 💬 Discord: [Join our community](https://discord.gg/voice-automation)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/voice-automation-platform/issues)
- 📚 Docs: [Documentation Site](https://docs.voiceautomation.dev)

---

**Built with ❤️ by the Voice Automation Platform team**

