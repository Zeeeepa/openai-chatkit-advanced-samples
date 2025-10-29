'use client';

import { Bot, Play, Trash2, Activity } from 'lucide-react';
import { useAppStore } from '@/stores/app-store';
import { apiClient } from '@/lib/api-client';

export default function AgentMonitor() {
  const { agents, addAgent, removeAgent } = useAppStore();

  const handleSpawnAgent = async (role: string) => {
    try {
      const agent = await apiClient.spawnAgent(role);
      addAgent(agent);
    } catch (error) {
      console.error('Failed to spawn agent:', error);
    }
  };

  const handleRemoveAgent = async (agentId: string) => {
    try {
      await apiClient.removeAgent(agentId);
      removeAgent(agentId);
    } catch (error) {
      console.error('Failed to remove agent:', error);
    }
  };

  const getRoleColor = (role: string) => {
    switch (role) {
      case 'orchestrator':
        return 'bg-purple-100 text-purple-700 border-purple-300';
      case 'research':
        return 'bg-blue-100 text-blue-700 border-blue-300';
      case 'code':
        return 'bg-green-100 text-green-700 border-green-300';
      case 'validator':
        return 'bg-orange-100 text-orange-700 border-orange-300';
      default:
        return 'bg-gray-100 text-gray-700 border-gray-300';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-2xl font-bold text-gray-900">Agent Monitor</h2>
        <Activity className="w-6 h-6 text-primary-500 animate-pulse" />
      </div>

      <div className="mb-6 flex gap-2">
        <button
          onClick={() => handleSpawnAgent('orchestrator')}
          className="flex-1 px-3 py-2 text-sm bg-purple-100 hover:bg-purple-200 text-purple-700 rounded transition-colors"
        >
          <Play className="w-4 h-4 inline mr-1" />
          Orchestrator
        </button>
        <button
          onClick={() => handleSpawnAgent('research')}
          className="flex-1 px-3 py-2 text-sm bg-blue-100 hover:bg-blue-200 text-blue-700 rounded transition-colors"
        >
          <Play className="w-4 h-4 inline mr-1" />
          Research
        </button>
        <button
          onClick={() => handleSpawnAgent('code')}
          className="flex-1 px-3 py-2 text-sm bg-green-100 hover:bg-green-200 text-green-700 rounded transition-colors"
        >
          <Play className="w-4 h-4 inline mr-1" />
          Code
        </button>
      </div>

      {agents.length === 0 ? (
        <div className="text-center py-12">
          <Bot className="w-12 h-12 text-gray-400 mx-auto mb-3" />
          <p className="text-gray-500">No agents running</p>
          <p className="text-sm text-gray-400 mt-1">
            Spawn an agent to start automation
          </p>
        </div>
      ) : (
        <div className="space-y-3 max-h-80 overflow-y-auto">
          {agents.map((agent) => (
            <div
              key={agent.id}
              className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <Bot className="w-5 h-5 text-primary-500" />
                    <span
                      className={`px-2 py-1 text-xs font-medium rounded border ${getRoleColor(
                        agent.role
                      )}`}
                    >
                      {agent.role}
                    </span>
                    <span className="text-xs text-gray-500">{agent.status}</span>
                  </div>
                  <h3 className="font-semibold text-gray-900">{agent.name}</h3>
                  <div className="flex gap-4 mt-2 text-sm text-gray-600">
                    <div>
                      <span className="text-success-600">✓ {agent.completed_tasks}</span>
                    </div>
                    <div>
                      <span className="text-error-600">✗ {agent.failed_tasks}</span>
                    </div>
                  </div>
                  <p className="text-xs text-gray-400 mt-2">ID: {agent.id}</p>
                </div>
                <button
                  onClick={() => handleRemoveAgent(agent.id)}
                  className="ml-4 p-2 text-gray-400 hover:text-error-500 hover:bg-error-50 rounded transition-colors"
                  title="Remove agent"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="mt-6 pt-4 border-t border-gray-200">
        <div className="grid grid-cols-2 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold text-gray-900">{agents.length}</div>
            <div className="text-xs text-gray-500">Active Agents</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-primary-500">
              {agents.reduce((sum, a) => sum + a.completed_tasks, 0)}
            </div>
            <div className="text-xs text-gray-500">Total Tasks</div>
          </div>
        </div>
      </div>
    </div>
  );
}

