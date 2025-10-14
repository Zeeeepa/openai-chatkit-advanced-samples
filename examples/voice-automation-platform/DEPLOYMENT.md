# Voice Automation Platform - Deployment Guide

Complete deployment guide for the Voice Automation Platform with ChatKit integration and GLM-4.5V vision capabilities.

---

## 🚀 Quick Start (Recommended)

The easiest way to deploy is using our automated setup script:

```bash
# Check your environment
python3 setup.py --check

# Deploy in development mode
python3 setup.py --mode=dev

# Deploy with Z.ai vision demo
python3 setup.py --mode=demo
```

**That's it!** The script will:
- ✅ Validate your environment
- ✅ Install all dependencies
- ✅ Configure environment files
- ✅ Start both backend and frontend
- ✅ Provide health checks

---

## 📋 Prerequisites

### Required
- **Python 3.8+** (for backend)
- **Node.js 18+** (for frontend)
- **npm 8+** (for package management)

### API Keys Needed
1. **OpenAI API Key** - Get from [OpenAI Platform](https://platform.openai.com/api-keys)
2. **ChatKit Workflow ID** - Create workflow in [Agent Builder](https://platform.openai.com/agent-builder)
3. **Z.ai API Token** (optional) - For vision capabilities

### Check Your Environment
```bash
python3 setup.py --check
```

Expected output:
```
✅ Python 3.8+ - Compatible
✅ Node.js v18+ - Available
✅ npm 8+ - Available
```

---

## 🎯 Deployment Modes

### 1. Development Mode (Default)
Best for local development with hot-reloading:

```bash
python3 setup.py --mode=dev
```

**Features:**
- Backend auto-reload on code changes
- Frontend hot-module replacement
- Debug logging enabled
- CORS enabled for localhost

### 2. Demo Mode (With Vision)
Includes Z.ai GLM-4.5V vision integration:

```bash
python3 setup.py --mode=demo
```

**Extra Features:**
- Pre-configured Z.ai credentials
- Vision testing enabled
- All dev mode features

### 3. Production Mode
Optimized for production deployment:

```bash
python3 setup.py --mode=prod
```

**Features:**
- Optimized builds
- Production error handling
- Security hardening
- Performance optimizations

---

## ⚙️ Configuration

### Backend Configuration

#### 1. Edit `backend/.env`

```bash
# Required: OpenAI API Key
OPENAI_API_KEY=sk-your-openai-api-key-here

# Required: OpenAI Model Configuration
OPENAI_MODEL=gpt-4
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=2000

# Required: ChatKit Workflow ID
CHATKIT_WORKFLOW_ID=wf_your_workflow_id_here
CHATKIT_API_BASE=https://api.openai.com/v1

# Optional: Z.ai Vision Configuration (for demo mode)
ANTHROPIC_MODEL=glm-4.5V
ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic
ANTHROPIC_AUTH_TOKEN=your_zai_token_here
```

#### 2. Get Your Workflow ID

1. Visit [OpenAI Agent Builder](https://platform.openai.com/agent-builder)
2. Create a new workflow:
   - Name: "Voice Automation Agent"
   - Add tools: CLI Executor, Web Search, File Manager
   - Configure agent behavior
3. Click **Publish**
4. Copy the Workflow ID (starts with `wf_`)

### Frontend Configuration

#### 1. Edit `frontend/.env.local`

```bash
# Required: ChatKit Workflow ID (same as backend)
NEXT_PUBLIC_CHATKIT_WORKFLOW_ID=wf_your_workflow_id_here

# Optional: Backend API URL (if not localhost)
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Z.ai Vision Setup (Optional)

To enable vision capabilities with GLM-4.5V:

#### 1. Get Z.ai API Token

Current demo token (provided):
```bash
ANTHROPIC_AUTH_TOKEN=665b963943b647dc9501dff942afb877.A47LrMc7sgGjyfBJ
```

Or request your own from [Z.ai](https://z.ai)

#### 2. Configure Backend

Add to `backend/.env`:
```bash
ANTHROPIC_MODEL=glm-4.5V
ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic
ANTHROPIC_AUTH_TOKEN=your_token_here
```

#### 3. Test Vision Integration

```bash
python3 tests/test_vision_integration.py
```

Expected: 5/5 tests pass ✅

---

## 📦 Manual Installation (Alternative)

If you prefer manual setup instead of using `setup.py`:

### Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env with your API keys

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend runs on: http://localhost:8000  
API Docs: http://localhost:8000/docs

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local
# Edit .env.local with your workflow ID

# Start development server
npm run dev
```

Frontend runs on: http://localhost:3000

---

## 🔍 Verification & Testing

### 1. Check Backend Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-14T12:00:00Z"
}
```

### 2. Access API Documentation

Open: http://localhost:8000/docs

You should see interactive Swagger UI with all endpoints:
- POST `/api/chatkit/session` - Create ChatKit session
- POST `/api/chatkit/session/refresh` - Refresh session
- GET `/api/chatkit/health` - Health check
- And 20+ more endpoints...

### 3. Access Frontend

Open: http://localhost:3000

You should see:
- ✅ Voice input interface
- ✅ Task dashboard
- ✅ Agent monitor
- ✅ MCP tools panel

### 4. Test ChatKit Integration

1. Open browser console (F12)
2. Navigate to http://localhost:3000
3. Check for ChatKit script loading
4. Look for session creation logs

### 5. Run Vision Tests (if enabled)

```bash
cd examples/voice-automation-platform
python3 tests/test_vision_integration.py
```

Expected output:
```
🚀 STARTING VISION INTEGRATION TESTS
============================================================

✅ PASS - UI Component Recognition
✅ PASS - Error State Detection
✅ PASS - Code Screenshot Analysis
✅ PASS - Architecture Diagram Analysis
✅ PASS - Visual Regression Detection

Overall: 5/5 tests passed
🎉 ALL TESTS PASSED!
```

---

## 🐛 Troubleshooting

### Backend Issues

#### "Module not found" errors
```bash
cd backend
pip install -r requirements.txt --upgrade
```

#### "OPENAI_API_KEY not set"
Edit `backend/.env` and add your API key:
```bash
OPENAI_API_KEY=sk-your-key-here
```

#### Port 8000 already in use
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different port
uvicorn app.main:app --reload --port 8001
```

### Frontend Issues

#### "Cannot find module" errors
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

#### "NEXT_PUBLIC_CHATKIT_WORKFLOW_ID is required"
Edit `frontend/.env.local` and add your workflow ID:
```bash
NEXT_PUBLIC_CHATKIT_WORKFLOW_ID=wf_your_id_here
```

#### Port 3000 already in use
```bash
# Use different port
npm run dev -- -p 3001
```

### ChatKit Integration Issues

#### "Session creation failed"
1. Verify workflow ID is correct in both `.env` files
2. Check OpenAI API key is valid
3. Ensure workflow is published in Agent Builder
4. Check browser console for detailed errors

#### "Script loading failed"
1. Check internet connection (CDN access)
2. Verify ChatKit script URL is correct in `layout.tsx`
3. Check browser console for CSP errors

### Vision Integration Issues

#### "Vision tests failing"
1. Verify Z.ai token is set in `.env`:
   ```bash
   ANTHROPIC_AUTH_TOKEN=your_token_here
   ```
2. Check API endpoint is accessible:
   ```bash
   curl https://api.z.ai/api/anthropic/v1/messages -H "Authorization: Bearer your_token"
   ```
3. Install test dependencies:
   ```bash
   pip install pillow requests
   ```

---

## 🔒 Security Best Practices

### API Keys
- ✅ Never commit `.env` files to git
- ✅ Use environment variables in production
- ✅ Rotate API keys regularly
- ✅ Use separate keys for dev/prod

### Backend Security
- ✅ Enable CORS only for trusted origins
- ✅ Use HTTPS in production
- ✅ Implement rate limiting
- ✅ Validate all inputs
- ✅ Use authentication middleware

### Frontend Security
- ✅ Don't expose backend API keys
- ✅ Use `NEXT_PUBLIC_` prefix only for public vars
- ✅ Implement CSP headers
- ✅ Sanitize user inputs
- ✅ Use secure WebSocket connections (WSS)

---

## 🚀 Production Deployment

### Using Docker (Recommended)

Coming soon! We're working on Docker compose configuration.

### Manual Production Setup

#### Backend

```bash
# Install production dependencies
pip install -r requirements.txt --no-dev

# Set production environment
export ENVIRONMENT=production

# Use production ASGI server
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### Frontend

```bash
# Build production bundle
npm run build

# Start production server
npm start
```

### Environment Variables for Production

```bash
# Backend
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
ALLOWED_ORIGINS=https://yourdomain.com

# Frontend
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NODE_ENV=production
```

---

## 📊 Monitoring & Logs

### Backend Logs

```bash
# View live logs
tail -f backend/logs/app.log

# Check error logs
grep ERROR backend/logs/app.log
```

### Frontend Logs

```bash
# Development server logs
npm run dev

# Production server logs
pm2 logs frontend
```

### Application Health

Backend: http://localhost:8000/health  
Frontend: http://localhost:3000/api/health

---

## 🆘 Getting Help

### Documentation
- [ChatKit Integration Guide](./CHATKIT_INTEGRATION.md)
- [Architecture Overview](./README.md)
- [API Documentation](http://localhost:8000/docs)

### Community
- Create an issue on GitHub
- Check existing issues for solutions
- Contact the development team

### Debug Mode

Enable verbose logging:

```bash
# Backend
export DEBUG=true
export LOG_LEVEL=DEBUG

# Frontend
export NEXT_PUBLIC_DEBUG=true
```

---

## ✅ Post-Deployment Checklist

After successful deployment:

- [ ] Backend health check returns 200
- [ ] Frontend loads without errors
- [ ] ChatKit script loads successfully
- [ ] Session creation works
- [ ] API documentation accessible
- [ ] Environment variables configured
- [ ] Vision tests pass (if enabled)
- [ ] CORS configured correctly
- [ ] Logs are being written
- [ ] Monitoring is active

---

## 🎉 You're All Set!

Your Voice Automation Platform is now running!

**Access Points:**
- 🌐 Frontend: http://localhost:3000
- 📚 API Docs: http://localhost:8000/docs
- 🏥 Health Check: http://localhost:8000/health

**Next Steps:**
1. Configure your agents in the Agent Builder
2. Add MCP tools for automation
3. Test voice commands
4. Create automation workflows
5. Monitor task execution

Happy automating! 🚀

