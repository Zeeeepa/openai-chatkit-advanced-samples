interface ChatKitPanelProps {
  threadId: string | null
  onThreadIdChange: (id: string) => void
}

export function ChatKitPanel({ threadId, onThreadIdChange }: ChatKitPanelProps) {
  // Placeholder - ChatKit React integration in Step 22
  // TODO: Use onThreadIdChange when ChatKit integration is complete
  console.log('ChatKit Panel - onThreadIdChange:', onThreadIdChange);
  
  return (
    <div className="chatkit-panel">
      <h2>Chat History</h2>
      <p className="placeholder">
        ChatKit Panel integration coming in Step 22
      </p>
      {threadId && (
        <div className="thread-info">
          <p>Thread ID: {threadId}</p>
        </div>
      )}
    </div>
  )
}
