'use client';

import { CheckCircle, Clock, XCircle, Trash2 } from 'lucide-react';
import { useAppStore } from '@/stores/app-store';
import { apiClient } from '@/lib/api-client';

export default function TaskDashboard() {
  const { tasks, removeTask } = useAppStore();

  const handleDelete = async (taskId: string) => {
    try {
      await apiClient.deleteTask(taskId);
      removeTask(taskId);
    } catch (error) {
      console.error('Failed to delete task:', error);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-success-500" />;
      case 'failed':
        return <XCircle className="w-5 h-5 text-error-500" />;
      default:
        return <Clock className="w-5 h-5 text-warning-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-success-50 text-success-700 border-success-200';
      case 'failed':
        return 'bg-error-50 text-error-700 border-error-200';
      default:
        return 'bg-warning-50 text-warning-700 border-warning-200';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">Task Dashboard</h2>

      {tasks.length === 0 ? (
        <div className="text-center py-12">
          <Clock className="w-12 h-12 text-gray-400 mx-auto mb-3" />
          <p className="text-gray-500">No tasks yet</p>
          <p className="text-sm text-gray-400 mt-1">
            Create a task with a voice command to get started
          </p>
        </div>
      ) : (
        <div className="space-y-3 max-h-96 overflow-y-auto">
          {tasks.map((task) => (
            <div
              key={task.id}
              className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    {getStatusIcon(task.status)}
                    <span
                      className={`px-2 py-1 text-xs font-medium rounded border ${getStatusColor(
                        task.status
                      )}`}
                    >
                      {task.status}
                    </span>
                  </div>
                  <h3 className="font-semibold text-gray-900">{task.type}</h3>
                  <p className="text-sm text-gray-600 mt-1">{task.description}</p>
                  <p className="text-xs text-gray-400 mt-2">ID: {task.id}</p>
                </div>
                <button
                  onClick={() => handleDelete(task.id)}
                  className="ml-4 p-2 text-gray-400 hover:text-error-500 hover:bg-error-50 rounded transition-colors"
                  title="Delete task"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="mt-6 pt-4 border-t border-gray-200">
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold text-gray-900">{tasks.length}</div>
            <div className="text-xs text-gray-500">Total</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-success-500">
              {tasks.filter((t) => t.status === 'completed').length}
            </div>
            <div className="text-xs text-gray-500">Completed</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-error-500">
              {tasks.filter((t) => t.status === 'failed').length}
            </div>
            <div className="text-xs text-gray-500">Failed</div>
          </div>
        </div>
      </div>
    </div>
  );
}

