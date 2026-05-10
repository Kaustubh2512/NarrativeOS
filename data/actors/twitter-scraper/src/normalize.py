import hashlib
import re
from datetime import datetime, timezone
from typing import Any


KNOWN_COMPANIES: dict[str, str] = {
    "NVDA": "NVIDIA", "AMD": "Advanced Micro Devices", "AAPL": "Apple",
    "MSFT": "Microsoft", "GOOGL": "Alphabet (Google)", "GOOG": "Alphabet (Google)",
    "AMZN": "Amazon", "META": "Meta Platforms", "TSLA": "Tesla",
    "JPM": "JPMorgan Chase", "GS": "Goldman Sachs", "SPY": "SPDR S&P 500 ETF",
    "QQQ": "Invesco QQQ Trust", "PLTR": "Palantir Technologies", "AVGO": "Broadcom",
    "TSM": "Taiwan Semiconductor", "ARM": "ARM Holdings", "NFLX": "Netflix",
    "DIS": "Walt Disney", "BA": "Boeing", "COIN": "Coinbase",
    "HOOD": "Robinhood Markets", "MSTR": "MicroStrategy",
}

TICKER_PATTERN = re.compile(r'\b[A-Z]{1,5}\b')
CASHTAG_PATTERN = re.compile(r'\$([A-Z]{1,5})')


def extract_tickers(text: str) -> list[str]:
    if not text:
        return []
    words = set(TICKER_PATTERN.findall(text))
    cashtags = set(CASHTAG_PATTERN.findall(text))
    combined = words | cashtags
    known = {t for t in combined if t in KNOWN_COMPANIES}
    return sorted(known)


def extract_entities(text: str) -> list[dict]:
    return [
        {"name": KNOWN_COMPANIES.get(t, t), "type": "company", "ticker": t}
        for t in dict.fromkeys(extract_tickers(text))
    ]


def build_event_id(source: str, url: str) -> str:
    h = hashlib.sha256(f"{source}:{url}".encode()).hexdigest()[:12]
    return f"evt_{source}_{h}"


def normalize_tweet(tweet: dict[str, Any]) -> dict[str, Any]:
    text = f"{tweet.get('title', '')} {tweet.get('body', '')}"
    return {
        "id": build_event_id("twitter", tweet.get("url", "")),
        "source": "twitter",
        "source_actor": "narrativeos-twitter-scraper",
        "title": tweet.get("title", ""),
        "body": tweet.get("body", ""),
        "url": tweet.get("url", ""),
        "author": tweet.get("author", ""),
        "published_at": _to_iso(tweet.get("published_at")),
        "collected_at": _now_iso(),
        "ticker_mentions": extract_tickers(text),
        "entities": extract_entities(text),
        "sentiment_score": None,
        "metadata": {
            "likes": tweet.get("likes", 0),
            "retweets": tweet.get("retweets", 0),
            "replies": tweet.get("replies", 0),
            "search_query": tweet.get("search_query", ""),
        },
    }


def _to_iso(val: Any) -> str:
    if val is None:
        return _now_iso()
    if isinstance(val, (int, float)):
        return datetime.fromtimestamp(val, tz=timezone.utc).isoformat()
    return str(val)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def clean_tweet_text(raw: str) -> str:
    if not raw:
        return ""
    clean = re.sub(r'<[^>]+>', ' ', raw)
    clean = re.sub(r'\s+', ' ', clean).strip()
    return clean
