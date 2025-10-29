/**
 * API client for Voice Automation Platform backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface Task {
  task_id: string;
  type: string;
  description: string;
  status: string;
  priority: number;
  created_at: string;
  started_at?: string;
  completed_at?: string;
  result?: any;
  error?: string;
}

export interface Agent {
  agent_id: string;
  role: string;
  name: string;
  description: string;
  status: string;
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

export interface VoiceCommandRequest {
  command: string;
  language?: string;
  user_id?: string;
  context?: Record<string, any>;
}

export interface VoiceCommandResponse {
  task_id: string;
  status: string;
  message: string;
  estimated_duration?: number;
}

/**
 * Voice API
 */
export const voiceAPI = {
  async sendCommand(request: VoiceCommandRequest): Promise<VoiceCommandResponse> {
    const response = await fetch(`${API_BASE_URL}/api/voice/command`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(request),
    });
    
    if (!response.ok) {
      throw new Error(`Failed to send command: ${response.statusText}`);
    }
    
    return response.json();
  },

  async getStatus() {
    const response = await fetch(`${API_BASE_URL}/api/voice/status`);
    if (!response.ok) throw new Error("Failed to fetch voice status");
    return response.json();
  },

  async getTask(taskId: string): Promise<Task> {
    const response = await fetch(`${API_BASE_URL}/api/voice/tasks/${taskId}`);
    if (!response.ok) throw new Error("Failed to fetch task");
    return response.json();
  },
};

/**
 * Tasks API
 */
export const tasksAPI = {
  async list(status?: string, page = 1, pageSize = 20) {
    const params = new URLSearchParams();
    if (status) params.set("status", status);
    params.set("page", page.toString());
    params.set("page_size", pageSize.toString());
    
    const response = await fetch(`${API_BASE_URL}/api/tasks?${params}`);
    if (!response.ok) throw new Error("Failed to fetch tasks");
    return response.json();
  },

  async get(taskId: string): Promise<Task> {
    const response = await fetch(`${API_BASE_URL}/api/tasks/${taskId}`);
    if (!response.ok) throw new Error("Failed to fetch task");
    return response.json();
  },

  async create(task: {
    type: string;
    description: string;
    params?: Record<string, any>;
    priority?: number;
    depends_on?: string[];
  }): Promise<Task> {
    const response = await fetch(`${API_BASE_URL}/api/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(task),
    });
    
    if (!response.ok) throw new Error("Failed to create task");
    return response.json();
  },

  async cancel(taskId: string) {
    const response = await fetch(`${API_BASE_URL}/api/tasks/${taskId}`, {
      method: "DELETE",
    });
    
    if (!response.ok) throw new Error("Failed to cancel task");
  },

  async getStats() {
    const response = await fetch(`${API_BASE_URL}/api/tasks/stats`);
    if (!response.ok) throw new Error("Failed to fetch task stats");
    return response.json();
  },
};

/**
 * Agents API
 */
export const agentsAPI = {
  async list() {
    const response = await fetch(`${API_BASE_URL}/api/agents`);
    if (!response.ok) throw new Error("Failed to fetch agents");
    return response.json();
  },

  async get(agentId: string): Promise<Agent> {
    const response = await fetch(`${API_BASE_URL}/api/agents/${agentId}`);
    if (!response.ok) throw new Error("Failed to fetch agent");
    return response.json();
  },

  async spawn(agent: {
    role: string;
    custom_name?: string;
    model?: string;
    temperature?: number;
    max_tokens?: number;
  }): Promise<Agent> {
    const response = await fetch(`${API_BASE_URL}/api/agents`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(agent),
    });
    
    if (!response.ok) throw new Error("Failed to spawn agent");
    return response.json();
  },

  async remove(agentId: string) {
    const response = await fetch(`${API_BASE_URL}/api/agents/${agentId}`, {
      method: "DELETE",
    });
    
    if (!response.ok) throw new Error("Failed to remove agent");
  },

  async getStats() {
    const response = await fetch(`${API_BASE_URL}/api/agents/stats`);
    if (!response.ok) throw new Error("Failed to fetch agent stats");
    return response.json();
  },

  async getStatus(agentId: string) {
    const response = await fetch(`${API_BASE_URL}/api/agents/${agentId}/status`);
    if (!response.ok) throw new Error("Failed to fetch agent status");
    return response.json();
  },
};

/**
 * MCP API
 */
export const mcpAPI = {
  async listTools() {
    const response = await fetch(`${API_BASE_URL}/api/mcp/tools`);
    if (!response.ok) throw new Error("Failed to fetch MCP tools");
    return response.json();
  },

  async getTool(toolId: string): Promise<MCPTool> {
    const response = await fetch(`${API_BASE_URL}/api/mcp/tools/${toolId}`);
    if (!response.ok) throw new Error("Failed to fetch tool");
    return response.json();
  },

  async executeTool(toolId: string, params: Record<string, any>) {
    const response = await fetch(`${API_BASE_URL}/api/mcp/execute`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tool_id: toolId, params }),
    });
    
    if (!response.ok) throw new Error("Failed to execute tool");
    return response.json();
  },

  async listServers() {
    const response = await fetch(`${API_BASE_URL}/api/mcp/servers`);
    if (!response.ok) throw new Error("Failed to fetch MCP servers");
    return response.json();
  },

  async startServer(serverId: string) {
    const response = await fetch(`${API_BASE_URL}/api/mcp/servers/${serverId}/start`, {
      method: "POST",
    });
    
    if (!response.ok) throw new Error("Failed to start server");
    return response.json();
  },

  async stopServer(serverId: string) {
    const response = await fetch(`${API_BASE_URL}/api/mcp/servers/${serverId}/stop`, {
      method: "POST",
    });
    
    if (!response.ok) throw new Error("Failed to stop server");
    return response.json();
  },

  async getServerStatus(serverId: string) {
    const response = await fetch(`${API_BASE_URL}/api/mcp/servers/${serverId}/status`);
    if (!response.ok) throw new Error("Failed to fetch server status");
    return response.json();
  },
};

