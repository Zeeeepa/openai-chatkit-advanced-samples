"use client";

import { VoiceInterface } from "@/components/VoiceInterface";
import { TaskDashboard } from "@/components/TaskDashboard";

export default function Home() {
  return (
    <div className="p-8 space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            Voice Automation Platform
          </h1>
          <p className="mt-2 text-gray-600">
            Control your multi-agent system with voice commands
          </p>
        </div>
      </div>

      {/* Voice Interface Section */}
      <section className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">Voice Control</h2>
        <VoiceInterface />
      </section>

      {/* Task Dashboard Section */}
      <section className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">Active Tasks</h2>
        <TaskDashboard />
      </section>
    </div>
  );
}

