"""Apify On-Demand Client — Zynd agents call Actors for fresh data.

Usage:
    from data.mcp.client import NarrativeOSDataClient

    client = NarrativeOSDataClient()
    events = client.fetch_news(max_articles=10)
    filings = client.fetch_sec_filings(tickers=["NVDA", "AMD"])
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from apify_client import ApifyClient

APIFY_TOKEN = os.environ.get("APIFY_TOKEN", "")
if not APIFY_TOKEN:
    dotenv = Path(__file__).parents[2] / ".env"
    if dotenv.exists():
        for line in dotenv.read_text().splitlines():
            if line.startswith("APIFY_TOKEN="):
                APIFY_TOKEN = line.split("=", 1)[1].strip()

NEWS_ACTOR_ID = "rxTkx6ACrjUdlCgNO"
SEC_ACTOR_ID = "Q3cP0eqIAlqH2YsrI"
TWITTER_ACTOR_ID = "0XfiV1wgo6qLV1Xig"


class NarrativeOSDataClient:
    """On-demand data client for Zynd agents.

    Agents call fetch_news(), fetch_sec_filings(), or fetch_twitter()
    to get fresh data instead of waiting for scheduled pipeline runs.
    """

    def __init__(self, token: str | None = None):
        self._client = ApifyClient(token or APIFY_TOKEN)

    def fetch_news(
        self,
        max_articles: int = 20,
        rss_sources: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        rss_sources = rss_sources or [
            "https://feeds.content.dowjones.io/public/rss/markets",
            "https://finance.yahoo.com/news/rssindex",
        ]
        result = self._client.actor(NEWS_ACTOR_ID).call(
            run_input={
                "rss_sources": rss_sources,
                "web_sources": [
                    "https://www.investing.com/news/stock-market-news",
                ],
                "max_articles": max_articles,
            },
        )
        dataset_id = result.get("defaultDatasetId")
        if not dataset_id:
            return []
        return list(self._client.dataset(dataset_id).iterate_items())

    def fetch_sec_filings(
        self,
        tickers: list[str] | None = None,
        form_types: list[str] | None = None,
        max_filings: int = 5,
    ) -> list[dict[str, Any]]:
        tickers = tickers or [
            "NVDA", "AMD", "AAPL", "MSFT", "GOOGL",
            "AMZN", "META", "TSLA", "JPM", "GS",
        ]
        form_types = form_types or ["10-K", "10-Q", "8-K"]
        result = self._client.actor(SEC_ACTOR_ID).call(
            run_input={
                "tickers": tickers,
                "form_types": form_types,
                "max_filings": max_filings,
            },
        )
        dataset_id = result.get("defaultDatasetId")
        if not dataset_id:
            return []
        return list(self._client.dataset(dataset_id).iterate_items())

    def fetch_twitter(
        self,
        tickers: list[str] | None = None,
        max_tweets: int = 10,
    ) -> list[dict[str, Any]]:
        tickers = tickers or [
            "NVDA", "AMD", "AAPL", "MSFT", "GOOGL",
            "AMZN", "META", "TSLA",
        ]
        result = self._client.actor(TWITTER_ACTOR_ID).call(
            run_input={
                "tickers": [f"${t}" for t in tickers],
                "max_tweets": max_tweets,
            },
        )
        dataset_id = result.get("defaultDatasetId")
        if not dataset_id:
            return []
        return list(self._client.dataset(dataset_id).iterate_items())

    def fetch_all(
        self,
        max_articles: int = 10,
        max_filings: int = 3,
        max_tweets: int = 5,
    ) -> dict[str, list[dict[str, Any]]]:
        import concurrent.futures

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
            news_future = pool.submit(self.fetch_news, max_articles)
            sec_future = pool.submit(self.fetch_sec_filings, max_filings=max_filings)
            twitter_future = pool.submit(self.fetch_twitter, max_tweets=max_tweets)
            return {
                "news": news_future.result(),
                "sec": sec_future.result(),
                "twitter": twitter_future.result(),
                "collected_at": datetime.now(timezone.utc).isoformat(),
            }
