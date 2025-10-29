'use client';

import { useState } from 'react';
import { Mic, MicOff, Send } from 'lucide-react';
import { apiClient } from '@/lib/api-client';
import { useAppStore } from '@/stores/app-store';

export default function VoiceInterface() {
  const [command, setCommand] = useState('');
  const [response, setResponse] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const { isListening, setListening, setLastCommand } = useAppStore();

  const handleVoiceInput = () => {
    // In production: integrate with Web Speech API
    setListening(!isListening);

    if (!isListening) {
      // Start listening
      console.log('Starting voice recognition...');
      // Mock: simulate voice input after 2 seconds
      setTimeout(() => {
        const mockCommand = 'Search for documentation on FastAPI';
        setCommand(mockCommand);
        setListening(false);
      }, 2000);
    }
  };

  const handleSubmit = async (e?: React.FormEvent) => {
    e?.preventDefault();

    if (!command.trim()) return;

    setIsProcessing(true);
    setLastCommand(command);

    try {
      const result = await apiClient.processVoiceCommand(command);

      setResponse(result.response_text);
      setCommand('');
    } catch (error) {
      console.error('Failed to process command:', error);
      setResponse('Sorry, I encountered an error processing your command.');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold text-gray-900">Voice Command</h2>
        <button
          onClick={handleVoiceInput}
          className={`p-3 rounded-full transition-all ${
            isListening
              ? 'bg-red-500 hover:bg-red-600 animate-pulse'
              : 'bg-primary-500 hover:bg-primary-600'
          }`}
          title={isListening ? 'Stop listening' : 'Start listening'}
        >
          {isListening ? (
            <MicOff className="w-6 h-6 text-white" />
          ) : (
            <Mic className="w-6 h-6 text-white" />
          )}
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="command" className="block text-sm font-medium text-gray-700 mb-2">
            What would you like me to do?
          </label>
          <div className="flex gap-2">
            <input
              id="command"
              type="text"
              value={command}
              onChange={(e) => setCommand(e.target.value)}
              placeholder="e.g., 'Search for React documentation' or 'Create a new task'"
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              disabled={isProcessing || isListening}
            />
            <button
              type="submit"
              disabled={isProcessing || !command.trim()}
              className="px-6 py-3 bg-primary-500 text-white rounded-lg hover:bg-primary-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>

        {isListening && (
          <div className="flex items-center gap-2 text-red-500 animate-pulse">
            <div className="w-2 h-2 bg-red-500 rounded-full"></div>
            <span className="text-sm font-medium">Listening...</span>
          </div>
        )}

        {isProcessing && (
          <div className="flex items-center gap-2 text-primary-500">
            <div className="w-5 h-5 border-2 border-primary-500 border-t-transparent rounded-full animate-spin"></div>
            <span className="text-sm font-medium">Processing your command...</span>
          </div>
        )}
      </form>

      {response && (
        <div className="mt-6 p-4 bg-primary-50 border border-primary-200 rounded-lg">
          <h3 className="text-sm font-semibold text-primary-900 mb-2">Response:</h3>
          <p className="text-gray-700">{response}</p>
        </div>
      )}

      <div className="mt-6 grid grid-cols-2 gap-3">
        <button
          onClick={() => setCommand('Search for TypeScript best practices')}
          className="px-4 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
        >
          Search documentation
        </button>
        <button
          onClick={() => setCommand('Create a new Python project')}
          className="px-4 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
        >
          Generate code
        </button>
      </div>
    </div>
  );
}

