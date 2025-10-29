/**
 * TypeScript types matching backend models
 */

export type AgentStatus =
  | "idle"
  | "thinking"
  | "executing"
  | "waiting"
  | "completed"
  | "failed"
  | "cancelled";

export type AgentRole =
  | "orchestrator"
  | "research"
  | "code"
  | "data"
  | "validator"
  | "browser"
  | "custom";

export interface Task {
  task_id: string;
  type: string;
  description: string;
  status: AgentStatus;
  priority: number;
  created_at: string;
  started_at?: string;
  completed_at?: string;
  result?: any;
  error?: string;
}

export interface Agent {
  agent_id: string;
  role: AgentRole;
  name: string;
  description: string;
  status: AgentStatus;
  model: string;
  current_task?: string;
  completed_tasks: number;
  failed_tasks: number;
  created_at: string;
  tools: string[];
}

export interface MCPTool {
  tool_id: string;
  name: string;
  description: string;
  parameters: Record<string, any>;
  examples: string[];
}

export interface MCPServer {
  server_id: string;
  name: string;
  description: string;
  version: string;
  status: string;
  capabilities: string[];
}

export interface TaskStats {
  total: number;
  idle: number;
  executing: number;
  completed: number;
  failed: number;
  cancelled: number;
}

export interface AgentStats {
  total: number;
  active: number;
  idle: number;
  executing: number;
  by_role: Record<string, number>;
}

export interface VoiceStatus {
  enabled: boolean;
  provider: string;
  languages: string[];
  active_tasks: number;
}

