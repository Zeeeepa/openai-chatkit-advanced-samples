import { useState } from 'react'
import { ChatKitPanel } from './components/ChatKitPanel'
import { VoiceInterface } from './components/VoiceInterface'
import './App.css'

function App() {
  const [threadId, setThreadId] = useState<string | null>(null)
  const [isListening, setIsListening] = useState(false)

  return (
    <div className="app">
      <header className="app-header">
        <h1>🎙️ Voice Automation</h1>
        <p>Speak to control your workflow</p>
      </header>

      <main className="app-main">
        <div className="voice-container">
          <VoiceInterface 
            threadId={threadId}
            isListening={isListening}
            onListeningChange={setIsListening}
          />
        </div>

        <div className="chat-container">
          <ChatKitPanel 
            threadId={threadId}
            onThreadIdChange={setThreadId}
          />
        </div>
      </main>
    </div>
  )
}

export default App

