"""Voice-controlled automation agent."""

import os
from typing import Any

from chatkit.server import ChatKitServer
from chatkit.types import ThreadMetadata
from agents import Agent


class VoiceAgent:
    """Agent that executes automation tasks from voice input."""

    def __init__(self, store, tools: list[Any] | None = None):
        """Initialize the agent with store and tools.
        
        Args:
            store: ChatKit Store implementation for persistence
            tools: List of Agent tools (CLI, Browser, etc.)
        """
        self.store = store
        self.tools = tools or []
        
        # Initialize Agent with OpenAI client
        self.agent = Agent(
            name="VoiceAutomation",
            model=os.getenv("MODEL", "gpt-4o"),
            instructions=self._get_system_prompt(),
            tools=self.tools,
        )
        
        # Initialize ChatKit Server
        self.server = ChatKitServer(
            store=self.store,
            agent=self.agent,
        )

    def _get_system_prompt(self) -> str:
        """Get the agent's system prompt."""
        return """You are a voice-controlled automation assistant.

Your role:
1. Listen to voice commands from users
2. Break down tasks into actionable steps
3. Execute automation using available tools
4. Report progress and results clearly

Available capabilities:
- Execute CLI commands (when allowed)
- Automate browser interactions
- Run tests and validate results
- Search and gather information
- Manage MCP servers

Guidelines:
- Always confirm dangerous operations
- Provide clear status updates
- Handle errors gracefully
- Ask for clarification when needed
- Report results concisely

Remember: You're operating through voice, so keep responses clear and concise."""

    async def process_message(
        self, 
        thread_id: str, 
        message: str, 
        context: dict[str, Any] | None = None
    ) -> str:
        """Process a voice message and return response.
        
        Args:
            thread_id: Thread ID for conversation context
            message: Voice message transcribed to text
            context: Additional context (user info, etc.) - optional
            
        Returns:
            Agent's text response (to be spoken)
        """
        # Run agent with thread_id directly
        # SDK v1.0.0 handles threading internally via store
        response = await self.agent.run(
            messages=[{"role": "user", "content": message}],
            thread_id=thread_id,
            context=context or {},
        )
        
        # Extract text from response
        if hasattr(response, "content"):
            if isinstance(response.content, str):
                return response.content
            elif isinstance(response.content, list):
                # Concatenate text parts
                texts = [
                    part.get("text", "") 
                    for part in response.content 
                    if part.get("type") == "text"
                ]
                return " ".join(texts)
        
        return "I processed your request."

    def get_server(self) -> ChatKitServer:
        """Get the ChatKit server instance.
        
        Returns:
            Configured ChatKit Server
        """
        return self.server
