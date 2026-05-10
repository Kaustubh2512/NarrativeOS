"""Shared LLM client — supports OpenAI, OpenRouter, and any OpenAI-compatible endpoint."""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Try loading .env from project root
_env_path = Path(__file__).resolve().parent.parent / ".env"
if _env_path.exists():
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip())

_LLM_CLIENT = None
_LLM_MODEL = None


def get_client():
    global _LLM_CLIENT, _LLM_MODEL
    if _LLM_CLIENT is not None:
        return _LLM_CLIENT, _LLM_MODEL

    try:
        from openai import OpenAI
    except ImportError:
        logger.warning("openai package not installed")
        return None, None

    api_key = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY") or ""
    base_url = os.environ.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

    if not api_key:
        logger.warning("No LLM API key found (set OPENROUTER_API_KEY or OPENAI_API_KEY)")
        return None, None

    _LLM_CLIENT = OpenAI(api_key=api_key, base_url=base_url, timeout=30)
    _LLM_MODEL = os.environ.get("LLM_MODEL", "openai/gpt-4o-mini")
    logger.info("LLM client initialized with model=%s base_url=%s", _LLM_MODEL, base_url)
    return _LLM_CLIENT, _LLM_MODEL


def call_llm(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.5,
    max_tokens: int = 500,
    json_mode: bool = False,
    retries: int = 1,
) -> str | None:
    client, model = get_client()
    if client is None:
        return None

    kwargs: dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
        "timeout": 30,
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    last_error = None
    for attempt in range(retries + 1):
        try:
            response = client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
        except Exception as e:
            last_error = e
            if attempt < retries:
                logger.warning("LLM retry %d/%d after: %s", attempt + 1, retries, e)
    logger.error("LLM call failed after %d attempts: %s", retries + 1, last_error)
    return None
