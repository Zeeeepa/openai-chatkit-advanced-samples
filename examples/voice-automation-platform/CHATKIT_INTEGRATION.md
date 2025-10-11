# ChatKit Integration Guide

This document explains how the Voice Automation Platform integrates with OpenAI's official ChatKit framework.

## Overview

The Voice Automation Platform now includes **full ChatKit integration** following OpenAI's official patterns. This provides:

- ✅ Official `<openai-chatkit>` web component
- ✅ Session management with client secrets
- ✅ File attachments support
- ✅ Client-side tools handling
- ✅ Theme configuration
- ✅ Error handling and recovery

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     ChatKit Integration                      │
└─────────────────────────────────────────────────────────────┘

Frontend (Next.js)                 Backend (FastAPI)
┌──────────────────┐              ┌──────────────────┐
│                  │              │                  │
│  ChatKitPanel    │◄────────────►│  /api/chatkit    │
│  Component       │              │  /session        │
│                  │              │                  │
│  - useChatKit()  │              │  - OpenAI SDK    │
│  - getClient     │              │  - Session       │
│    Secret()      │              │    Creation      │
│  - onClientTool  │              │                  │
│                  │              │                  │
└──────────────────┘              └──────────────────┘
         │                                 │
         │                                 │
         ▼                                 ▼
┌──────────────────┐              ┌──────────────────┐
│  ChatKit CDN     │              │  Agent Builder   │
│  Web Component   │              │  Workflow        │
└──────────────────┘              └──────────────────┘
```

## Quick Start

### 1. Get Your Workflow ID

1. Go to [OpenAI Agent Builder](https://platform.openai.com/agent-builder)
2. Create a new workflow or use an existing one
3. Click "Publish" to get your workflow ID
4. Copy the `wf_xxxxx` ID

### 2. Configure Environment Variables

**Backend** (`backend/.env`):
```bash
OPENAI_API_KEY=sk-your-api-key-here
CHATKIT_WORKFLOW_ID=wf_your_workflow_id_here
```

**Frontend** (`frontend/.env.local`):
```bash
NEXT_PUBLIC_CHATKIT_WORKFLOW_ID=wf_your_workflow_id_here
```

### 3. Install Dependencies

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

The following packages are now included:
- `openai>=1.12.0` - OpenAI Python SDK
- `chatkit>=0.1.0` - ChatKit Python SDK
- `agents>=0.1.0` - OpenAI Agents SDK

**Frontend:**
```bash
cd frontend
npm install
```

The following packages are now included:
- `@openai/chatkit-react` - ChatKit React bindings
- `@openai/chatkit` - ChatKit core library

### 4. Start the Servers

**Backend:**
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm run dev
```

### 5. Test the Integration

1. Open http://localhost:3000
2. The ChatKit component will automatically load
3. Try a voice command or type a message
4. The agent will respond using your workflow

## Components

### Backend: ChatKit Session Endpoint

Location: `backend/app/routes/chatkit.py`

**Key Features:**
- Session creation with workflow ID
- Client secret generation
- File upload configuration
- Session refresh support
- Health check endpoint

**Endpoints:**
- `POST /api/chatkit/session` - Create new session
- `POST /api/chatkit/session/refresh` - Refresh session
- `GET /api/chatkit/health` - Health check

**Example Request:**
```typescript
POST /api/chatkit/session
{
  "workflow": { "id": "wf_xxxxx" },
  "chatkit_configuration": {
    "file_upload": {
      "enabled": true,
      "max_size_mb": 10
    }
  }
}
```

**Example Response:**
```json
{
  "client_secret": "cs_xxxxx",
  "session_id": "session_xxxxx",
  "expires_at": 1234567890
}
```

### Frontend: ChatKitPanel Component

Location: `frontend/src/components/ChatKitPanel.tsx`

**Key Features:**
- Official `useChatKit` hook integration
- Automatic session management
- File attachments enabled
- Client-side tools support
- Theme switching
- Error handling with recovery

**Usage Example:**
```typescript
import { ChatKitPanel } from '@/components/ChatKitPanel';

export default function Page() {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  return (
    <ChatKitPanel
      theme={theme}
      onThemeChange={setTheme}
      onResponseEnd={() => console.log('Response complete')}
      className="h-[600px] w-full"
    />
  );
}
```

## Client-Side Tools

Client-side tools allow the AI agent to invoke functions that run in the browser.

### Built-in Tools

**Theme Switching:**
```typescript
// Agent can call this tool to switch themes
{
  "name": "switch_theme",
  "params": {
    "theme": "dark" | "light"
  }
}
```

### Custom Tools

Add custom client tools by passing an `onClientTool` handler:

```typescript
<ChatKitPanel
  onClientTool={async (invocation) => {
    if (invocation.name === "custom_action") {
      // Handle your custom action
      return { success: true, data: "result" };
    }
    return { success: false };
  }}
/>
```

## File Attachments

File attachments are enabled by default. Users can:
- Upload files up to 10MB
- Attach multiple files per message
- Preview attachments before sending

**Configuration:**
```typescript
// In backend/app/routes/chatkit.py
chatkit_configuration: {
  file_upload: {
    enabled: true,
    max_size_mb: 10,
    allowed_types: ["image/*", "application/pdf"]
  }
}
```

## Theme Configuration

Customize the ChatKit appearance:

```typescript
const chatkit = useChatKit({
  theme: {
    colorScheme: 'light',
    palette: {
      primary: '#3b82f6',
      secondary: '#64748b',
    },
    typography: {
      fontFamily: 'Inter, sans-serif',
    },
  },
  // ... other options
});
```

See [ChatKit Playground](https://chatkit.studio/playground) for theme options.

## Error Handling

The integration includes comprehensive error handling:

### Script Loading Errors
```
⚠️ ChatKit web component is unavailable. Verify script URL.
```
**Solution:** Check your internet connection or CDN access.

### Session Creation Errors
```
⚠️ Set NEXT_PUBLIC_CHATKIT_WORKFLOW_ID in your .env.local file.
```
**Solution:** Add your workflow ID to the environment file.

### API Errors
```
⚠️ Failed to create session: [error message]
```
**Solution:** Check backend logs and API key configuration.

## Development Mode

When `NODE_ENV=development`, the integration includes:
- Detailed console logging
- Request/response debugging
- Error stack traces
- Development-only warnings

**Example Logs:**
```
[ChatKitPanel] getClientSecret invoked
  currentSecretPresent: false
  workflowId: wf_xxxxx
  endpoint: /api/chatkit/session

[ChatKitPanel] createSession response
  status: 200
  ok: true
  bodyPreview: {...}
```

## Production Checklist

Before deploying to production:

- [ ] Set `NODE_ENV=production`
- [ ] Use real workflow ID (not `wf_replace...`)
- [ ] Configure proper CORS origins
- [ ] Enable HTTPS for API endpoints
- [ ] Set up proper error monitoring
- [ ] Test file upload limits
- [ ] Verify session refresh works
- [ ] Test theme switching
- [ ] Check mobile responsiveness

## Troubleshooting

### ChatKit Component Not Loading

**Symptom:** Blank screen or loading spinner forever

**Check:**
1. Script URL is accessible: https://cdn.platform.openai.com/deployments/chatkit/chatkit.js
2. Browser console for errors
3. Network tab for failed requests

### Session Creation Fails

**Symptom:** "Failed to create session" error

**Check:**
1. `OPENAI_API_KEY` is valid
2. `CHATKIT_WORKFLOW_ID` starts with `wf_`
3. Backend is running and accessible
4. CORS is configured correctly

### File Upload Not Working

**Symptom:** Cannot attach files

**Check:**
1. `file_upload.enabled` is `true`
2. File size is under `max_size_mb`
3. File type is allowed
4. Backend has `python-multipart` installed

## API Documentation

Full API documentation is available at:
- http://localhost:8000/api/docs (Swagger UI)
- http://localhost:8000/api/redoc (ReDoc)

## Resources

- [ChatKit Documentation](https://openai.github.io/chatkit-js/)
- [ChatKit Python SDK](https://openai.github.io/chatkit-python/)
- [Agent Builder](https://platform.openai.com/agent-builder)
- [ChatKit Playground](https://chatkit.studio/playground)
- [OpenAI API Keys](https://platform.openai.com/api-keys)

## Support

For issues or questions:
1. Check the logs: `backend/logs/voice_automation.log`
2. Review browser console for frontend errors
3. Verify environment variables are set
4. Check API documentation at `/api/docs`
5. Review this guide's troubleshooting section

## Migration from Custom Implementation

If you were using the custom multi-agent system:

1. **Workflow Creation:** Map your agents to Agent Builder workflows
2. **Environment:** Add `CHATKIT_WORKFLOW_ID` to both backend and frontend
3. **Dependencies:** Run `pip install -r requirements.txt` and `npm install`
4. **Component:** Replace custom UI with `<ChatKitPanel />`
5. **Testing:** Verify all features work with the new integration

The custom implementation is still available in git history if needed.

