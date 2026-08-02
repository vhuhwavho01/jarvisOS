"""
core/events.py

Lightweight thread-safe EventBus singleton used for inter-module communication.
Provides subscribe/unsubscribe/publish. Handlers are executed synchronously.
"""

from __future__ import annotations

import logging
import threading
from typing import Any, Callable, Dict, List

logger = logging.getLogger("EventBus")
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(name)s - %(message)s"))
    logger.addHandler(ch)
logger.setLevel(logging.INFO)

EventHandler = Callable[[str, Any], None]


class EventBus:
    """Simple thread-safe publish/subscribe bus."""

    def __init__(self):
        self._subs: Dict[str, List[EventHandler]] = {}
        self._lock = threading.RLock()

    def subscribe(self, topic: str, handler: EventHandler) -> None:
        with self._lock:
            self._subs.setdefault(topic, []).append(handler)
            logger.debug("Subscribed %s to %s", handler, topic)

    def unsubscribe(self, topic: str, handler: EventHandler) -> None:
        with self._lock:
            handlers = self._subs.get(topic)
            if not handlers:
                return
            try:
                handlers.remove(handler)
                logger.debug("Unsubscribed %s from %s", handler, topic)
            except ValueError:
                logger.debug("Handler %s not found for topic %s", handler, topic)

    def publish(self, topic: str, payload: Any = None) -> None:
        handlers: List[EventHandler] = []
        with self._lock:
            handlers = list(self._subs.get(topic, []))
        logger.debug("Publishing topic=%s to %d handlers", topic, len(handlers))
        for h in handlers:
            try:
                h(topic, payload)
            except Exception:
                logger.exception("Event handler error for topic=%s", topic)


# Module-level singleton for easy imports
bus = EventBus()
