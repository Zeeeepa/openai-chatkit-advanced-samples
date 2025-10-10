# 🧪 Testing Guide

## Test Checklist

### Pre-Flight Checks
- [ ] Python 3.9+ installed
- [ ] Node.js 18+ installed
- [ ] OpenAI API key configured
- [ ] Both servers can start
- [ ] No port conflicts (8000, 3000)

### Backend Tests

#### 1. Server Startup
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

Expected output:
```
🚀 Voice Automation Platform Starting...
✓ Webhook system initialized
✓ Environment: Development
✓ Voice Input: Enabled
✅ Voice Automation Platform Ready!
```

#### 2. Health Check
```bash
curl http://localhost:8000/health
```

Expected:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime": "operational"
}
```

#### 3. API Documentation
Visit: http://localhost:8000/api/docs

Check that all endpoints are listed:
- Voice (3 endpoints)
- Tasks (6 endpoints)
- Agents (6 endpoints)
- MCP (8 endpoints)

#### 4. Voice Command Test
```bash
curl -X POST http://localhost:8000/api/voice/command \
  -H "Content-Type: application/json" \
  -d '{
    "command": "Test command",
    "language": "en-US"
  }'
```

Expected:
```json
{
  "task_id": "...",
  "status": "idle",
  "message": "Processing command: 'Test command'...",
  "estimated_duration": 30
}
```

#### 5. Task Management
```bash
# List tasks
curl http://localhost:8000/api/tasks

# Get stats
curl http://localhost:8000/api/tasks/stats
```

#### 6. Agent Management
```bash
# List agents
curl http://localhost:8000/api/agents

# Get stats
curl http://localhost:8000/api/agents/stats
```

#### 7. MCP Tools
```bash
# List tools
curl http://localhost:8000/api/mcp/tools

# List servers
curl http://localhost:8000/api/mcp/servers
```

### Frontend Tests

#### 1. Development Server
```bash
cd frontend
npm run dev
```

Expected output:
```
ready - started server on 0.0.0.0:3000
```

#### 2. Page Access
Visit each page and verify it loads:
- [ ] http://localhost:3000 (Home - Voice Interface & Task Dashboard)
- [ ] http://localhost:3000/agents (Agent Monitor)
- [ ] http://localhost:3000/tasks (Task Management)
- [ ] http://localhost:3000/settings (MCP Manager)

#### 3. UI Component Tests

**Home Page:**
- [ ] Voice interface visible
- [ ] Command input field works
- [ ] Task dashboard displays
- [ ] No console errors

**Agents Page:**
- [ ] Agent list displays
- [ ] Spawn agent button visible
- [ ] Agent cards show correct info

**Tasks Page:**
- [ ] Task list displays
- [ ] Task stats show correctly
- [ ] Filter controls work

**Settings Page:**
- [ ] MCP tools list displays
- [ ] Server controls visible

#### 4. WebSocket Connection
Open browser console on http://localhost:3000

Expected console messages:
```
[WebSocket] Connected
[WebSocket] Received: connected event
```

#### 5. API Integration
In browser console:
```javascript
// Test API connection
fetch('http://localhost:8000/health')
  .then(r => r.json())
  .then(console.log);
```

### Integration Tests

#### 1. End-to-End Voice Command Flow
1. Open frontend: http://localhost:3000
2. Enter command: "Test automation workflow"
3. Click "Send Command" or press Enter
4. Verify:
   - [ ] Task appears in dashboard
   - [ ] Task status updates
   - [ ] WebSocket events received
   - [ ] Task completes or shows progress

#### 2. Multi-Agent Workflow
Run example workflow:
```bash
cd examples
python workflow_05_multi_agent.py
```

Verify:
- [ ] Main agent spawns
- [ ] Sub-agents created
- [ ] Tools executed
- [ ] Webhooks fired
- [ ] Task completes
- [ ] Result returned

#### 3. WebSocket Real-Time Updates
1. Open frontend in browser
2. Open backend logs in terminal
3. Send a voice command
4. Verify:
   - [ ] Command received in backend logs
   - [ ] Task created event in frontend
   - [ ] Agent spawned event in frontend
   - [ ] Progress updates in frontend
   - [ ] Completion event in frontend

### Performance Tests

#### 1. Concurrent Tasks
```python
import asyncio
import httpx

async def test_concurrent():
    async with httpx.AsyncClient() as client:
        tasks = []
        for i in range(10):
            task = client.post(
                "http://localhost:8000/api/voice/command",
                json={"command": f"Test task {i}"}
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        print(f"Created {len(results)} tasks")

asyncio.run(test_concurrent())
```

Expected: All 10 tasks created successfully

#### 2. WebSocket Load
Open 5+ browser tabs with frontend and verify:
- [ ] All connect successfully
- [ ] All receive events
- [ ] No connection drops
- [ ] No memory leaks

### Error Handling Tests

#### 1. Invalid API Key
1. Set wrong API key in backend/.env
2. Restart backend
3. Send voice command
4. Verify: Proper error message returned

#### 2. Network Failure
1. Stop backend
2. Try frontend operations
3. Verify: Proper error handling, no crashes

#### 3. Invalid Input
```bash
# Empty command
curl -X POST http://localhost:8000/api/voice/command \
  -H "Content-Type: application/json" \
  -d '{"command": ""}'
```

Expected: 422 validation error

#### 4. Non-existent Resources
```bash
curl http://localhost:8000/api/tasks/nonexistent-id
```

Expected: 404 not found

### Security Tests

#### 1. CORS
```bash
curl -X OPTIONS http://localhost:8000/api/voice/command \
  -H "Origin: http://evil.com" \
  -H "Access-Control-Request-Method: POST"
```

Verify: Only configured origins allowed

#### 2. Rate Limiting
Send 100 rapid requests:
```bash
for i in {1..100}; do
  curl http://localhost:8000/health &
done
```

Verify: Server handles load gracefully

## Automated Test Suite

Run full test suite:

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app

# Frontend tests
cd frontend
npm test
npm run type-check
npm run lint
```

## Common Issues

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

### Import Errors
```bash
# Reinstall dependencies
cd backend
pip install -r requirements.txt --force-reinstall
```

### WebSocket Connection Failed
- Verify backend is running
- Check WebSocket URL in frontend/.env.local
- Test direct WebSocket connection:
```bash
wscat -c ws://localhost:8000/ws
```

## Test Results Template

```
Date: _______________
Tester: _____________

Backend Tests:
- Server Startup: [ ] Pass [ ] Fail
- Health Check: [ ] Pass [ ] Fail
- API Docs: [ ] Pass [ ] Fail
- Voice Command: [ ] Pass [ ] Fail
- Task Management: [ ] Pass [ ] Fail
- Agent Management: [ ] Pass [ ] Fail
- MCP Tools: [ ] Pass [ ] Fail

Frontend Tests:
- Dev Server: [ ] Pass [ ] Fail
- Page Access: [ ] Pass [ ] Fail
- UI Components: [ ] Pass [ ] Fail
- WebSocket: [ ] Pass [ ] Fail
- API Integration: [ ] Pass [ ] Fail

Integration Tests:
- E2E Voice Flow: [ ] Pass [ ] Fail
- Multi-Agent: [ ] Pass [ ] Fail
- Real-time Updates: [ ] Pass [ ] Fail

Performance Tests:
- Concurrent Tasks: [ ] Pass [ ] Fail
- WebSocket Load: [ ] Pass [ ] Fail

Notes:
_______________________________
_______________________________
```

## Success Criteria

All tests should pass for production deployment:
- ✅ All endpoints return 200/201 status
- ✅ WebSocket connections stable
- ✅ No console errors
- ✅ UI renders correctly
- ✅ Real-time updates work
- ✅ Example workflows complete
- ✅ Error handling works
- ✅ Security measures active

