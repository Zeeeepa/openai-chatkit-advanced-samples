"""Webhook manager for event-driven agent communication."""

import asyncio
from collections import defaultdict
from typing import Any, Callable, Coroutine

from pydantic import BaseModel


class WebhookEvent(BaseModel):
    """Webhook event model."""

    event_type: str
    source: str
    data: dict[str, Any]
    timestamp: float


WebhookHandler = Callable[[WebhookEvent], Coroutine[Any, Any, None]]


class WebhookManager:
    """
    Manages webhook subscriptions and event emission.
    
    Enables loose coupling between agents through event-driven architecture.
    Agents can subscribe to events and emit events without direct dependencies.
    """

    def __init__(self):
        """Initialize webhook manager."""
        self._handlers: dict[str, list[WebhookHandler]] = defaultdict(list)
        self._event_queue: asyncio.Queue[WebhookEvent] = asyncio.Queue()
        self._worker_task: asyncio.Task | None = None
        self._running = False

    def subscribe(self, event_type: str, handler: WebhookHandler):
        """
        Subscribe to an event type.
        
        Args:
            event_type: Type of event to subscribe to (e.g., "agent_completed")
            handler: Async function to call when event occurs
        """
        self._handlers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: WebhookHandler):
        """
        Unsubscribe from an event type.
        
        Args:
            event_type: Type of event to unsubscribe from
            handler: Handler function to remove
        """
        if event_type in self._handlers:
            try:
                self._handlers[event_type].remove(handler)
            except ValueError:
                pass

    async def emit(self, event_type: str, source: str, data: dict[str, Any]):
        """
        Emit an event to all subscribers.
        
        Args:
            event_type: Type of event (e.g., "task_completed")
            source: Source of the event (e.g., "agent_123")
            data: Event data payload
        """
        event = WebhookEvent(
            event_type=event_type,
            source=source,
            data=data,
            timestamp=asyncio.get_event_loop().time(),
        )
        
        await self._event_queue.put(event)

    async def _process_events(self):
        """Background worker to process events from queue."""
        while self._running:
            try:
                # Get event with timeout to allow checking _running flag
                event = await asyncio.wait_for(
                    self._event_queue.get(),
                    timeout=1.0,
                )
                
                # Get handlers for this event type
                handlers = self._handlers.get(event.event_type, [])
                
                # Execute all handlers concurrently
                if handlers:
                    await asyncio.gather(
                        *[handler(event) for handler in handlers],
                        return_exceptions=True,
                    )
                
            except asyncio.TimeoutError:
                # No event within timeout, continue
                continue
            except Exception as e:
                print(f"Error processing webhook event: {e}")

    async def start(self):
        """Start the webhook event processor."""
        if self._running:
            return
        
        self._running = True
        self._worker_task = asyncio.create_task(self._process_events())

    async def stop(self):
        """Stop the webhook event processor."""
        if not self._running:
            return
        
        self._running = False
        
        if self._worker_task:
            await self._worker_task
            self._worker_task = None

    def get_subscriptions(self) -> dict[str, int]:
        """
        Get subscription statistics.
        
        Returns:
            Dict mapping event types to number of subscribers
        """
        return {
            event_type: len(handlers)
            for event_type, handlers in self._handlers.items()
        }


# Global webhook manager instance
_webhook_manager: WebhookManager | None = None


def get_webhook_manager() -> WebhookManager:
    """Get or create the global webhook manager."""
    global _webhook_manager
    if _webhook_manager is None:
        _webhook_manager = WebhookManager()
    return _webhook_manager

