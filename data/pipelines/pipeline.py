import json
import logging
import os
import sys
from datetime import datetime, timezone
from typing import Any

from apify_client import ApifyClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from pipelines.entity_extractor import extract_tickers, extract_entities
from stream.event_bus import EventBus

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

APIFY_TOKEN = os.environ.get("APIFY_API_TOKEN", "")
NEWS_RUN_ID = "QgROEyqZvSsukXh8e"
SEC_RUN_ID = "ldaLOgnrdLZXo1eam"
WEBHOOK_URL = os.environ.get("NARRATIVEOS_EVENT_STREAM_URL", "")


def enrich_event(event: dict[str, Any]) -> dict[str, Any]:
    text = f"{event.get('title', '')} {event.get('body', '')}"
    existing_tickers = event.get("ticker_mentions", []) or []
    if not existing_tickers:
        event["ticker_mentions"] = extract_tickers(text)
        event["entities"] = extract_entities(text)
    return event


def run_pipeline() -> list[dict[str, Any]]:
    client = ApifyClient(APIFY_TOKEN)
    bus = EventBus(webhook_url=WEBHOOK_URL)

    news_items = client.dataset(
        client.run(NEWS_RUN_ID).get()["defaultDatasetId"]
    ).list_items().items
    sec_items = client.dataset(
        client.run(SEC_RUN_ID).get()["defaultDatasetId"]
    ).list_items().items

    all_events = news_items + sec_items
    logger.info("Total raw events: %d (news=%d, sec=%d)", len(all_events), len(news_items), len(sec_items))

    enriched = [enrich_event(e) for e in all_events]
    seen: set[str] = set()
    deduped: list[dict[str, Any]] = []
    for e in enriched:
        eid = e.get("id", "")
        if eid not in seen:
            seen.add(eid)
            deduped.append(e)

    logger.info("After dedup: %d events", len(deduped))

    for event in deduped:
        bus.emit(event)

    flushed = bus.flush()
    bus.close()
    return flushed


def main() -> None:
    events = run_pipeline()
    print(f"\n{'='*60}")
    print(f"Pipeline complete: {len(events)} events emitted")
    print(f"{'='*60}")

    with_tickers = [e for e in events if e.get("ticker_mentions")]
    for e in with_tickers[:5]:
        tickers = ", ".join(e.get("ticker_mentions", []))
        print(f"  {e['id']} | {tickers} | {e['title'][:70]}")
    if len(with_tickers) > 5:
        print(f"  ... and {len(with_tickers) - 5} more with tickers")


if __name__ == "__main__":
    main()
