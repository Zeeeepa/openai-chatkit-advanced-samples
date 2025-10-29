"use client";

import { MCPManager } from "@/components/MCPManager";

export default function SettingsPage() {
  return (
    <div className="p-8">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
        <p className="mt-2 text-gray-600">
          Configure MCP servers and tools
        </p>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">MCP Server Configuration</h2>
        <MCPManager />
      </div>
    </div>
  );
}

