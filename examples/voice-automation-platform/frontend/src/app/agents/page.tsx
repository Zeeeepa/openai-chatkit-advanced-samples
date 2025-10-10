"use client";

import { AgentMonitor } from "@/components/AgentMonitor";

export default function AgentsPage() {
  return (
    <div className="p-8">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Agent Monitor</h1>
        <p className="mt-2 text-gray-600">
          Manage and monitor active AI agents in the system
        </p>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <AgentMonitor />
      </div>
    </div>
  );
}

