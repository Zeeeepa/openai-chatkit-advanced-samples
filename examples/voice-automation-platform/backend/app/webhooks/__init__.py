"""Webhook system for agent communication."""

from .manager import WebhookManager, get_webhook_manager
from .handlers import register_default_handlers
from .security import validate_webhook_signature

__all__ = [
    "WebhookManager",
    "get_webhook_manager",
    "register_default_handlers",
    "validate_webhook_signature",
]

