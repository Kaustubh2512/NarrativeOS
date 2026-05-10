"""Superplane bridge client — agent calls this to push pipeline results.

Usage:
    from infra.superplane.client import push_signal
    push_signal(signal.model_dump())
"""

from __future__ import annotations

import logging
import os
from typing import Any

import httpx

logger = logging.getLogger(__name__)

SUPERPLANE_BRIDGE_URL = os.environ.get("SUPERPLANE_BRIDGE_URL", "http://localhost:8765")

_TIMEOUT = httpx.Timeout(5.0)


def push_signal(signal: dict[str, Any]) -> bool:
    try:
        with httpx.Client(timeout=_TIMEOUT) as client:
            resp = client.post(
                f"{SUPERPLANE_BRIDGE_URL}/api/v1/datasets/executed_signals/items",
                json=signal,
            )
            resp.raise_for_status()
            logger.info("Signal pushed to Superplane bridge: %s", signal.get("signal_id", "?"))
            return True
    except Exception as e:
        logger.debug("Superplane bridge unreachable (non-critical): %s", e)
        return False


def push_event(event: dict[str, Any]) -> bool:
    try:
        with httpx.Client(timeout=_TIMEOUT) as client:
            resp = client.post(
                f"{SUPERPLANE_BRIDGE_URL}/api/v1/datasets/ingress/items",
                json=event,
            )
            resp.raise_for_status()
            return True
    except Exception as e:
        logger.debug("Superplane bridge unreachable (non-critical): %s", e)
        return False
