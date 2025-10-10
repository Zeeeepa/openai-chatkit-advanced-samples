"""In-memory store implementation for Voice Automation Platform."""

import asyncio
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any

from chatkit.store import Store
from chatkit.types import Page, ThreadItem, ThreadMetadata


class MemoryStore(Store[dict[str, Any]]):
    """
    In-memory implementation of the ChatKit Store interface.
    
    This store keeps all data in memory and is suitable for development
    and testing. For production, consider using a persistent store like
    PostgreSQL or Redis.
    """

    def __init__(self):
        """Initialize the memory store."""
        self._threads: dict[str, ThreadMetadata] = {}
        self._items: dict[str, list[ThreadItem]] = defaultdict(list)
        self._attachments: dict[tuple[str, str], bytes] = {}
        self._lock = asyncio.Lock()

    def generate_thread_id(self, context: dict[str, Any]) -> str:
        """Generate a unique thread ID."""
        return f"thread_{uuid.uuid4().hex[:12]}"

    def generate_item_id(
        self,
        type: str,
        thread: ThreadMetadata,
        context: dict[str, Any],
    ) -> str:
        """Generate a unique item ID."""
        return f"{type}_{uuid.uuid4().hex[:12]}"

    async def add_thread_item(
        self,
        thread_id: str,
        item: ThreadItem,
        context: dict[str, Any],
    ) -> None:
        """Add an item to a thread."""
        async with self._lock:
            self._items[thread_id].append(item)

    async def load_thread_items(
        self,
        thread_id: str,
        limit: int | None,
        order: str,
        after: str | None,
        context: dict[str, Any],
    ) -> Page[ThreadItem]:
        """Load items from a thread."""
        async with self._lock:
            items = self._items.get(thread_id, [])

            # Apply after filter
            if after:
                try:
                    after_idx = next(
                        i for i, item in enumerate(items) if item.id == after
                    )
                    items = items[after_idx + 1 :]
                except StopIteration:
                    items = []

            # Apply ordering
            if order == "desc":
                items = list(reversed(items))

            # Apply limit
            has_more = False
            if limit is not None and len(items) > limit:
                has_more = True
                items = items[:limit]

            # Get the cursor for next page
            next_cursor = items[-1].id if items and has_more else None

            return Page(
                data=items,
                has_more=has_more,
                after=next_cursor,
            )

    async def create_thread(
        self,
        thread: ThreadMetadata,
        context: dict[str, Any],
    ) -> None:
        """Create a new thread."""
        async with self._lock:
            self._threads[thread.id] = thread

    async def load_thread(
        self,
        thread_id: str,
        context: dict[str, Any],
    ) -> ThreadMetadata | None:
        """Load a thread by ID."""
        async with self._lock:
            return self._threads.get(thread_id)

    async def update_thread(
        self,
        thread_id: str,
        title: str,
        context: dict[str, Any],
    ) -> None:
        """Update thread metadata."""
        async with self._lock:
            if thread_id in self._threads:
                thread = self._threads[thread_id]
                thread.title = title
                thread.updated_at = datetime.now(timezone.utc)

    async def delete_thread(
        self,
        thread_id: str,
        context: dict[str, Any],
    ) -> None:
        """Delete a thread and all its items."""
        async with self._lock:
            self._threads.pop(thread_id, None)
            self._items.pop(thread_id, None)
            
            # Delete attachments
            keys_to_delete = [
                key for key in self._attachments.keys() if key[0] == thread_id
            ]
            for key in keys_to_delete:
                del self._attachments[key]

    async def load_threads(
        self,
        after: str | None,
        limit: int | None,
        order: str,
        context: dict[str, Any],
    ) -> Page[ThreadMetadata]:
        """Load all threads."""
        async with self._lock:
            threads = list(self._threads.values())

            # Sort by updated_at
            threads.sort(
                key=lambda t: t.updated_at,
                reverse=(order == "desc"),
            )

            # Apply after filter
            if after:
                try:
                    after_idx = next(
                        i for i, thread in enumerate(threads) if thread.id == after
                    )
                    threads = threads[after_idx + 1 :]
                except StopIteration:
                    threads = []

            # Apply limit
            has_more = False
            if limit is not None and len(threads) > limit:
                has_more = True
                threads = threads[:limit]

            # Get cursor for next page
            next_cursor = threads[-1].id if threads and has_more else None

            return Page(
                data=threads,
                has_more=has_more,
                after=next_cursor,
            )

    async def save_attachment(
        self,
        thread_id: str,
        attachment_id: str,
        data: bytes,
        context: dict[str, Any],
    ) -> None:
        """Save attachment data."""
        async with self._lock:
            self._attachments[(thread_id, attachment_id)] = data

    async def load_attachment(
        self,
        thread_id: str,
        attachment_id: str,
        context: dict[str, Any],
    ) -> bytes:
        """Load attachment data."""
        async with self._lock:
            data = self._attachments.get((thread_id, attachment_id))
            if data is None:
                raise KeyError(
                    f"Attachment {attachment_id} not found in thread {thread_id}"
                )
            return data

    async def delete_attachment(
        self,
        thread_id: str,
        attachment_id: str,
        context: dict[str, Any],
    ) -> None:
        """Delete an attachment."""
        async with self._lock:
            self._attachments.pop((thread_id, attachment_id), None)

    # Additional utility methods for the platform

    async def get_thread_count(self) -> int:
        """Get total number of threads."""
        async with self._lock:
            return len(self._threads)

    async def get_item_count(self, thread_id: str) -> int:
        """Get number of items in a thread."""
        async with self._lock:
            return len(self._items.get(thread_id, []))

    async def clear_all(self) -> None:
        """Clear all stored data. Use with caution!"""
        async with self._lock:
            self._threads.clear()
            self._items.clear()
            self._attachments.clear()

