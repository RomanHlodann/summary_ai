from __future__ import annotations

import asyncio
import functools
import logging
import os
from typing import Any, Callable, TypeVar

from openai import APIConnectionError, APIStatusError, RateLimitError


logger = logging.getLogger(__name__)
F = TypeVar("F", bound=Callable[..., Any])

_RETRYABLE = (RateLimitError, APIConnectionError)
_DEFAULT_ATTEMPTS = 3
_DEFAULT_BASE_DELAY = 1.0


def with_retry(attempts: int = _DEFAULT_ATTEMPTS, base_delay: float = _DEFAULT_BASE_DELAY) -> Callable[[F], F]:
    def decorator(fn: F) -> F:
        @functools.wraps(fn)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, attempts + 1):
                try:
                    return await fn(*args, **kwargs)
                except _RETRYABLE as exc:
                    if attempt == attempts:
                        logger.error("All %d attempts failed: %s", attempts, exc)
                        raise
                    delay = base_delay * (2 ** (attempt - 1))
                    logger.warning("Attempt %d failed (%s), retrying in %.1fs", attempt, exc, delay)
                    await asyncio.sleep(delay)
                except APIStatusError:
                    raise
        return wrapper
    return decorator
