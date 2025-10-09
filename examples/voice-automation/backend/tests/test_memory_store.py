"""Tests for MemoryStore."""

import pytest
from datetime import datetime, timezone

from app.memory_store import MemoryStore
from chatkit.types import ThreadMetadata, UserMessageItem, TextContent


@pytest.mark.asyncio
async def test_create_and_load_thread():
    """Test thread creation and loading."""
    store = MemoryStore()
    thread = ThreadMetadata(
        id=store.generate_thread_id({}),
        title="Test Thread",
        created_at=datetime.now(timezone.utc),
    )

    created = await store.create_thread(thread, {})
    loaded = await store.load_thread(thread.id, {})

    assert created.id == thread.id
    assert loaded.title == "Test Thread"


@pytest.mark.asyncio
async def test_add_and_load_items():
    """Test adding and loading thread items."""
    store = MemoryStore()
    thread = ThreadMetadata(
        id=store.generate_thread_id({}), created_at=datetime.now(timezone.utc)
    )
    await store.create_thread(thread, {})

    item = UserMessageItem(
        id=store.generate_item_id("message", thread, {}),
        thread_id=thread.id,
        content=[TextContent(type="text", text="Hello")],
        created_at=datetime.now(timezone.utc),
    )

    await store.add_thread_item(thread.id, item, {})

    items = await store.load_thread_items(thread.id, None, 10, "asc", {})

    assert len(items.data) == 1
    assert items.data[0].id == item.id
    assert not items.has_more


@pytest.mark.asyncio
async def test_pagination():
    """Test item pagination."""
    store = MemoryStore()
    thread = ThreadMetadata(
        id=store.generate_thread_id({}), created_at=datetime.now(timezone.utc)
    )
    await store.create_thread(thread, {})

    # Add 5 items
    items = []
    for i in range(5):
        item = UserMessageItem(
            id=store.generate_item_id("message", thread, {}),
            thread_id=thread.id,
            content=[TextContent(type="text", text=f"Message {i}")],
            created_at=datetime.now(timezone.utc),
        )
        await store.add_thread_item(thread.id, item, {})
        items.append(item)

    # Load first page (2 items)
    page1 = await store.load_thread_items(thread.id, None, 2, "asc", {})
    assert len(page1.data) == 2
    assert page1.has_more
    assert page1.data[0].id == items[0].id

    # Load second page
    page2 = await store.load_thread_items(thread.id, page1.after, 2, "asc", {})
    assert len(page2.data) == 2
    assert page2.has_more

    # Load final page
    page3 = await store.load_thread_items(thread.id, page2.after, 2, "asc", {})
    assert len(page3.data) == 1
    assert not page3.has_more


@pytest.mark.asyncio
async def test_delete_item():
    """Test item deletion."""
    store = MemoryStore()
    thread = ThreadMetadata(
        id=store.generate_thread_id({}), created_at=datetime.now(timezone.utc)
    )
    await store.create_thread(thread, {})

    item = UserMessageItem(
        id=store.generate_item_id("message", thread, {}),
        thread_id=thread.id,
        content=[TextContent(type="text", text="Hello")],
        created_at=datetime.now(timezone.utc),
    )
    await store.add_thread_item(thread.id, item, {})

    # Delete item
    await store.delete_thread_item(thread.id, item.id, {})

    # Verify deletion
    items = await store.load_thread_items(thread.id, None, 10, "asc", {})
    assert len(items.data) == 0


@pytest.mark.asyncio
async def test_thread_not_found():
    """Test error handling for missing thread."""
    store = MemoryStore()

    with pytest.raises(ValueError, match="Thread .* not found"):
        await store.load_thread("nonexistent", {})

