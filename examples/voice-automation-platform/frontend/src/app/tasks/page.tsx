"use client";

import { TaskDashboard } from "@/components/TaskDashboard";

export default function TasksPage() {
  return (
    <div className="p-8">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Task Management</h1>
        <p className="mt-2 text-gray-600">
          View and manage all automation tasks
        </p>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <TaskDashboard />
      </div>
    </div>
  );
}

