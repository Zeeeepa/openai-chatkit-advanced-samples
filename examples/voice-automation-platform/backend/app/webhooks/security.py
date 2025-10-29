"""Webhook security utilities."""

import hashlib
import hmac
from typing import Any

from fastapi import HTTPException, Header

from ..config import settings


def compute_signature(payload: str, secret: str) -> str:
    """
    Compute HMAC signature for webhook payload.
    
    Args:
        payload: The payload string to sign
        secret: Secret key for HMAC
        
    Returns:
        Hexadecimal signature string
    """
    signature = hmac.new(
        key=secret.encode("utf-8"),
        msg=payload.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).hexdigest()
    
    return signature


def validate_webhook_signature(
    payload: str,
    signature: str,
    secret: str | None = None,
) -> bool:
    """
    Validate webhook signature.
    
    Args:
        payload: The payload string
        signature: The signature to validate
        secret: Secret key (uses config if not provided)
        
    Returns:
        True if signature is valid
    """
    if secret is None:
        secret = settings.webhook_secret
    
    expected_signature = compute_signature(payload, secret)
    
    # Use constant-time comparison to prevent timing attacks
    return hmac.compare_digest(signature, expected_signature)


async def verify_webhook_header(
    x_webhook_signature: str = Header(None),
    payload_str: str = "",
) -> bool:
    """
    FastAPI dependency to verify webhook signature from headers.
    
    Usage:
        @app.post("/webhooks")
        async def webhook(verified: bool = Depends(verify_webhook_header)):
            if not verified:
                raise HTTPException(status_code=401)
    """
    if not settings.enable_webhooks:
        return True
    
    if not x_webhook_signature:
        raise HTTPException(
            status_code=401,
            detail="Missing webhook signature header",
        )
    
    if not validate_webhook_signature(payload_str, x_webhook_signature):
        raise HTTPException(
            status_code=401,
            detail="Invalid webhook signature",
        )
    
    return True


class RateLimiter:
    """
    Simple in-memory rate limiter for webhooks.
    
    In production, use Redis-backed rate limiting.
    """

    def __init__(self, max_requests: int = 100, time_window: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            max_requests: Maximum requests allowed
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self._requests: dict[str, list[float]] = {}

    def is_allowed(self, identifier: str, current_time: float) -> bool:
        """
        Check if request is allowed for identifier.
        
        Args:
            identifier: Unique identifier (e.g., IP or webhook source)
            current_time: Current timestamp
            
        Returns:
            True if request is allowed
        """
        # Get request history for identifier
        if identifier not in self._requests:
            self._requests[identifier] = []
        
        request_times = self._requests[identifier]
        
        # Remove old requests outside time window
        cutoff_time = current_time - self.time_window
        request_times[:] = [t for t in request_times if t > cutoff_time]
        
        # Check if limit exceeded
        if len(request_times) >= self.max_requests:
            return False
        
        # Add current request
        request_times.append(current_time)
        return True

    def cleanup(self, current_time: float):
        """
        Cleanup old entries.
        
        Should be called periodically to prevent memory growth.
        """
        cutoff_time = current_time - self.time_window
        
        # Remove identifiers with no recent requests
        empty_identifiers = [
            identifier
            for identifier, times in self._requests.items()
            if not times or max(times) < cutoff_time
        ]
        
        for identifier in empty_identifiers:
            del self._requests[identifier]


# Global rate limiter instance
_rate_limiter: RateLimiter | None = None


def get_rate_limiter() -> RateLimiter:
    """Get or create the global rate limiter."""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter(
            max_requests=100,  # 100 requests
            time_window=60,    # per minute
        )
    return _rate_limiter

