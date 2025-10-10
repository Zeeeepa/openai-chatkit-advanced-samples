'use client';

import { Wrench, Play } from 'lucide-react';
import { useAppStore } from '@/stores/app-store';

export default function MCPManager() {
  const { tools, selectTool } = useAppStore();

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">MCP Tools</h2>

      {tools.length === 0 ? (
        <div className="text-center py-12">
          <Wrench className="w-12 h-12 text-gray-400 mx-auto mb-3" />
          <p className="text-gray-500">No tools available</p>
        </div>
      ) : (
        <div className="space-y-3">
          {tools.map((tool) => (
            <button
              key={tool.name}
              onClick={() => selectTool(tool)}
              className="w-full border border-gray-200 rounded-lg p-4 hover:shadow-md transition-all text-left hover:border-primary-300"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <Wrench className="w-4 h-4 text-primary-500" />
                    <h3 className="font-semibold text-gray-900">{tool.name}</h3>
                  </div>
                  <p className="text-sm text-gray-600">{tool.description}</p>
                </div>
                <Play className="w-5 h-5 text-gray-400" />
              </div>
            </button>
          ))}
        </div>
      )}

      <div className="mt-6 pt-4 border-t border-gray-200">
        <div className="text-center">
          <div className="text-2xl font-bold text-gray-900">{tools.length}</div>
          <div className="text-xs text-gray-500">Available Tools</div>
        </div>
      </div>
    </div>
  );
}

