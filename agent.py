"""narrativeos-cognitive — Zynd-registered NarrativeOS agent mesh wrapper.

Runs the full multi-agent pipeline (Narrative → Sentiment → Debate → Signal)
as a discoverable Zynd entity.

When invoked with `{"fetch": true}` — or when no events are provided —
the agent pulls fresh data from Apify actors via the MCP client.
"""

from __future__ import annotations

import json
import logging
import os
import sys
from typing import Any

from dotenv import load_dotenv
from zyndai_agent import AgentConfig, ZyndAIAgent, resolve_registry_url
from zyndai_agent.a2a.server import HandlerInput, TaskHandle

load_dotenv()

logger = logging.getLogger(__name__)

_config: dict = {}
if os.path.exists("agent.config.json"):
    with open("agent.config.json") as _f:
        _config = json.load(_f)


def _fetch_data() -> list[dict[str, Any]]:
    """Pull fresh data from Apify actors via MCP client."""
    try:
        from data.mcp.client import NarrativeOSDataClient
        from data.pipelines.normalize import normalize_article, normalize_sec_filing, normalize_tweet

        client = NarrativeOSDataClient()
        logger.info("Fetching fresh data from Apify actors via MCP client...")
        result = client.fetch_all(max_articles=10, max_filings=5, max_tweets=5)

        events: list[dict[str, Any]] = []
        for article in result.get("news", []):
            events.append(normalize_article(article))
        for filing in result.get("sec", []):
            events.append(normalize_sec_filing(filing))
        for tweet in result.get("twitter", []):
            events.append(normalize_tweet(tweet))

        news_count = len(result.get("news", []))
        sec_count = len(result.get("sec", []))
        twitter_count = len(result.get("twitter", []))
        logger.info("MCP fetch complete: %d events (%d news, %d sec, %d twitter)", len(events), news_count, sec_count, twitter_count)
        return events

    except Exception as e:
        logger.warning("MCP fetch failed (Apify token may not be set): %s", e)
        return []


def run_analysis_pipeline(inbound: HandlerInput, task: TaskHandle) -> dict:
    try:
        from agents.graph.workflow import run_analysis
        from agents.models import NarrativeEvent

        events_data = inbound.message.content
        if isinstance(events_data, str) and events_data.strip():
            import json as _json
            events_data = _json.loads(events_data)

        should_fetch = False
        if isinstance(events_data, dict):
            should_fetch = events_data.pop("fetch", False)
        if not should_fetch and inbound.payload.get("fetch"):
            should_fetch = True

        raw_events: list[dict[str, Any]] = []
        if should_fetch:
            raw_events = _fetch_data()
        elif isinstance(events_data, list):
            raw_events = events_data
        elif isinstance(events_data, dict):
            raw_events = events_data.get("events", [events_data])
        else:
            raw_events = []

        if not raw_events:
            noop = {"signal_id": "", "ticker": "UNKNOWN", "direction": "HOLD", "confidence": 0.0,
                    "error": "No events to analyze"}
            return noop

        events = [NarrativeEvent(**e) for e in raw_events]

        tickers = set()
        for e in events:
            tickers.update(e.ticker_mentions)
        primary = next(iter(tickers)) if tickers else None

        signal = run_analysis(events, primary)
        signal_dict = signal.model_dump()

        try:
            from infra.superplane.client import push_signal, push_event
            push_signal(signal_dict)
            for e in raw_events[:5]:
                push_event(e)
        except Exception:
            pass

        return signal_dict

    except Exception as e:
        return task.fail(str(e))


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    agent_config = AgentConfig(
        name=_config.get("name", "narrativeos-cognitive"),
        description=_config.get("description", "NarrativeOS multi-agent reasoning mesh"),
        version=_config.get("version", "0.1.0"),
        category=_config.get("category", "finance"),
        tags=_config.get("tags", ["narrative", "sentiment", "debate", "trading"]),
        server_host=_config.get("server_host", "0.0.0.0"),
        server_port=int(os.environ.get("ZYND_SERVER_PORT") or _config.get("server_port") or 5000),
        auth_mode=_config.get("auth_mode", "permissive"),
        registry_url=resolve_registry_url(from_config_file=_config.get("registry_url")),
        keypair_path=os.environ.get("ZYND_AGENT_KEYPAIR_PATH", _config.get("keypair_path")),
        entity_url=os.environ.get("ZYND_ENTITY_URL", _config.get("entity_url")),
        price=_config.get("price"),
        entity_pricing=_config.get("entity_pricing"),
        entity_index=_config.get("entity_index", 0),
        skills=_config.get("skills"),
        fqan=_config.get("fqan"),
    )

    zynd_agent = ZyndAIAgent(config=agent_config)
    zynd_agent.on_message(run_analysis_pipeline)
    zynd_agent.start()

    print("\nNarrativeOS Cognitive Mesh is running on Zynd")
    print(f"FQAN:    {agent_config.registry_url}/0xYuvi/narrativeos-cognitive")
    print(f"A2A URL: {zynd_agent.a2a_url}")
    print(f"Card:    {zynd_agent.card_url}")

    if sys.stdin.isatty():
        print("\nType 'exit' to quit\n")
        while True:
            try:
                cmd = input()
            except EOFError:
                break
            if cmd.lower() == "exit":
                break
        zynd_agent.stop()
    else:
        import signal
        signal.pause()
