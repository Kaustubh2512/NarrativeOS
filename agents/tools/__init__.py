from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field

from agents.tools.price_lookup import lookup_price
from agents.tools.web_search import search_news
from agents.tools.sec_lookup import lookup_sec_filings

logger = logging.getLogger(__name__)


@dataclass
class ResearchData:
    ticker: str
    price: dict | None = None
    news: list[str] = field(default_factory=list)
    sec_filings: list[str] = field(default_factory=list)
    web_summary: str | None = None


def research_ticker(ticker: str) -> ResearchData:
    data = ResearchData(ticker=ticker)
    try:
        data.price = lookup_price(ticker)
    except Exception as e:
        logger.warning("price lookup failed for %s: %s", ticker, e)
    try:
        data.news = search_news(ticker)
    except Exception as e:
        logger.warning("news search failed for %s: %s", ticker, e)
    try:
        data.sec_filings = lookup_sec_filings(ticker)
    except Exception as e:
        logger.warning("sec lookup failed for %s: %s", ticker, e)
    return data


def research_ticker_text(ticker: str) -> str:
    data = research_ticker(ticker)
    parts = [f"=== RESEARCH DATA FOR {ticker} ==="]
    if data.price:
        p = data.price
        parts.append(
            f"PRICE: ${p.get('price', 'N/A')} "
            f"(change: {p.get('change_pct', 'N/A')}%, "
            f"high: ${p.get('day_high', 'N/A')}, "
            f"low: ${p.get('day_low', 'N/A')})"
        )
    if data.news:
        parts.append("RECENT NEWS:")
        for h in data.news[:5]:
            parts.append(f"  - {h}")
    if data.sec_filings:
        parts.append("RECENT SEC FILINGS:")
        for f in data.sec_filings[:3]:
            parts.append(f"  - {f}")
    return "\n".join(parts)
