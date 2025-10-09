import { useState, useEffect } from 'react'

interface VoiceInterfaceProps {
  threadId: string | null
  isListening: boolean
  onListeningChange: (listening: boolean) => void
}

export function VoiceInterface({ threadId, isListening, onListeningChange }: VoiceInterfaceProps) {
  const [transcript, setTranscript] = useState('')
  const [recognition, setRecognition] = useState<any>(null)
  
  // TODO: Use threadId when backend integration is complete
  console.log('Voice Interface - threadId:', threadId);

  useEffect(() => {
    // Initialize Web Speech API
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
      const recognizer = new SpeechRecognition()
      
      recognizer.continuous = false
      recognizer.interimResults = true
      recognizer.lang = 'en-US'
      
      recognizer.onresult = (event: any) => {
        const result = event.results[event.results.length - 1]
        setTranscript(result[0].transcript)
      }
      
      recognizer.onend = () => {
        onListeningChange(false)
      }
      
      setRecognition(recognizer)
    }
  }, [onListeningChange])

  const startListening = () => {
    if (recognition) {
      recognition.start()
      onListeningChange(true)
      setTranscript('')
    }
  }

  const stopListening = () => {
    if (recognition) {
      recognition.stop()
    }
  }

  return (
    <div className="voice-interface">
      <button
        onClick={isListening ? stopListening : startListening}
        className={`voice-button ${isListening ? 'listening' : ''}`}
      >
        {isListening ? '🎙️ Stop' : '🎤 Start'}
      </button>
      
      {transcript && (
        <div className="transcript">
          <p>{transcript}</p>
        </div>
      )}
      
      {!recognition && (
        <p className="error">Speech recognition not supported in this browser</p>
      )}
    </div>
  )
}
