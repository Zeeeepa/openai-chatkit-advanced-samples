'use client';

import { Home, BarChart, Bot, Wrench, Settings, Menu, X } from 'lucide-react';
import { useAppStore } from '@/stores/app-store';

export default function Sidebar() {
  const { sidebarOpen, toggleSidebar } = useAppStore();

  return (
    <>
      {/* Mobile toggle */}
      <button
        onClick={toggleSidebar}
        className="lg:hidden fixed top-4 left-4 z-50 p-2 bg-white rounded-lg shadow-lg"
      >
        {sidebarOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
      </button>

      {/* Sidebar */}
      <aside
        className={`${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        } lg:translate-x-0 fixed lg:static inset-y-0 left-0 z-40 w-64 bg-gray-900 text-white transition-transform duration-300`}
      >
        <div className="flex flex-col h-full">
          <div className="p-6">
            <h1 className="text-xl font-bold">🎙️ Voice Platform</h1>
            <p className="text-xs text-gray-400 mt-1">AI Automation</p>
          </div>

          <nav className="flex-1 px-3">
            <a
              href="#"
              className="flex items-center gap-3 px-3 py-2 rounded-lg bg-gray-800 text-white mb-2"
            >
              <Home className="w-5 h-5" />
              Dashboard
            </a>
            <a
              href="#"
              className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-800 text-gray-300 mb-2"
            >
              <BarChart className="w-5 h-5" />
              Analytics
            </a>
            <a
              href="#"
              className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-800 text-gray-300 mb-2"
            >
              <Bot className="w-5 h-5" />
              Agents
            </a>
            <a
              href="#"
              className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-800 text-gray-300 mb-2"
            >
              <Wrench className="w-5 h-5" />
              Tools
            </a>
          </nav>

          <div className="p-3 border-t border-gray-800">
            <a
              href="#"
              className="flex items-center gap-3 px-3 py-2 rounded-lg hover:bg-gray-800 text-gray-300"
            >
              <Settings className="w-5 h-5" />
              Settings
            </a>
          </div>

          <div className="p-4 bg-gray-800 text-xs text-gray-400">
            <p>v1.0.0</p>
            <p className="mt-1">OpenAI ChatKit Demo</p>
          </div>
        </div>
      </aside>

      {/* Overlay for mobile */}
      {sidebarOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black bg-opacity-50 z-30"
          onClick={toggleSidebar}
        />
      )}
    </>
  );
}

