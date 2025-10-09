"""In-memory Store implementation for development."""

from collections import defaultdict
from datetime import datetime
from typing import Any, Literal

from chatkit.store import Store
from chatkit.types import Page, ThreadItem, ThreadMetadata


class MemoryStore(Store[dict[str, Any]]):
    """In-memory implementation of Store for development and testing."""

    def __init__(self):
        self._threads: dict[str, ThreadMetadata] = {}
        self._items: dict[str, list[ThreadItem]] = defaultdict(list)
        self._counter = 0

    def generate_thread_id(self, context: dict[str, Any]) -> str:
        """Generate a unique thread ID."""
        self._counter += 1
        return f"thread_{self._counter}"

    def generate_item_id(
        self, item_type: str, thread: ThreadMetadata, context: dict[str, Any]
    ) -> str:
        """Generate a unique item ID."""
        self._counter += 1
        return f"{item_type}_{self._counter}"

    async def create_thread(
        self, thread: ThreadMetadata, context: dict[str, Any]
    ) -> ThreadMetadata:
        """Create a new thread."""
        self._threads[thread.id] = thread
        self._items[thread.id] = []
        return thread

    async def load_thread(
        self, thread_id: str, context: dict[str, Any]
    ) -> ThreadMetadata:
        """Load a thread by ID."""
        if thread_id not in self._threads:
            raise ValueError(f"Thread {thread_id} not found")
        return self._threads[thread_id]

    async def save_thread(
        self, thread: ThreadMetadata, context: dict[str, Any]
    ) -> None:
        """Save thread metadata."""
        self._threads[thread.id] = thread

    async def add_thread_item(
        self, thread_id: str, item: ThreadItem, context: dict[str, Any]
    ) -> None:
        """Add an item to a thread."""
        if thread_id not in self._items:
            raise ValueError(f"Thread {thread_id} not found")
        self._items[thread_id].append(item)

    async def load_thread_items(
        self,
        thread_id: str,
        after: str | None,
        limit: int,
        order: Literal["asc", "desc"],
        context: dict[str, Any],
    ) -> Page[ThreadItem]:
        """Load thread items with pagination."""
        items = self._items.get(thread_id, [])

        if order == "desc":
            items = list(reversed(items))

        # Find start index
        start_idx = 0
        if after:
            for i, item in enumerate(items):
                if item.id == after:
                    start_idx = i + 1
                    break

        # Get page
        page_items = items[start_idx : start_idx + limit]
        has_more = len(items) > start_idx + limit

        return Page(
            data=page_items,
            has_more=has_more,
            after=page_items[-1].id if page_items and has_more else None,
        )

    async def load_item(
        self, thread_id: str, item_id: str, context: dict[str, Any]
    ) -> ThreadItem:
        """Load a specific item."""
        items = self._items.get(thread_id, [])
        for item in items:
            if item.id == item_id:
                return item
        raise ValueError(f"Item {item_id} not found")

    async def save_item(
        self, thread_id: str, item: ThreadItem, context: dict[str, Any]
    ) -> None:
        """Save/update an item."""
        items = self._items.get(thread_id, [])
        for i, existing in enumerate(items):
            if existing.id == item.id:
                items[i] = item
                return
        raise ValueError(f"Item {item.id} not found")

    async def delete_thread_item(
        self, thread_id: str, item_id: str, context: dict[str, Any]
    ) -> None:
        """Delete an item from a thread."""
        items = self._items.get(thread_id, [])
        self._items[thread_id] = [i for i in items if i.id != item_id]

