import re
from typing import NamedTuple

KNOWN_COMPANIES: dict[str, str] = {
    "NVDA": "NVIDIA",
    "AMD": "Advanced Micro Devices",
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "GOOGL": "Alphabet (Google)",
    "GOOG": "Alphabet (Google)",
    "AMZN": "Amazon",
    "META": "Meta Platforms",
    "TSLA": "Tesla",
    "JPM": "JPMorgan Chase",
    "GS": "Goldman Sachs",
    "SPY": "SPDR S&P 500 ETF",
    "QQQ": "Invesco QQQ Trust",
    "PLTR": "Palantir Technologies",
    "AVGO": "Broadcom",
    "TSM": "Taiwan Semiconductor",
    "ARM": "ARM Holdings",
    "NFLX": "Netflix",
    "DIS": "Walt Disney",
    "BA": "Boeing",
    "COIN": "Coinbase",
    "HOOD": "Robinhood Markets",
    "MSTR": "MicroStrategy",
    "BTC": "Bitcoin",
    "ETH": "Ethereum",
    "SOL": "Solana",
    "XRP": "XRP",
    "DOGE": "Dogecoin",
    "ADA": "Cardano",
    "DOT": "Polkadot",
    "LINK": "Chainlink",
    "AVAX": "Avalanche",
    "GOLD": "Gold",
    "XAU": "Gold (XAU)",
    "SILVER": "Silver",
    "XAG": "Silver (XAG)",
    "OIL": "Crude Oil (WTI)",
    "WTI": "West Texas Intermediate",
    "BRENT": "Brent Crude",
    "NG": "Natural Gas",
    "HG": "Copper",
    "COPPER": "Copper Futures",
    "PL": "Platinum",
    "PA": "Palladium",
    "CORN": "Corn Futures",
    "WHEAT": "Wheat Futures",
    "SOY": "Soybean Futures",
}

try:
    from agents.models import ASSET_TYPE_MAP, AssetType
    HAS_MODELS = True
except ImportError:
    HAS_MODELS = False

TICKER_PATTERN = re.compile(r'\b[A-Z]{1,5}\b')


class ExtractedEntity(NamedTuple):
    name: str
    entity_type: str
    ticker: str


def asset_type(ticker: str) -> str:
    if HAS_MODELS:
        at = ASSET_TYPE_MAP.get(ticker, AssetType.UNKNOWN)
        return at.value
    return "unknown"


def extract_tickers(text: str) -> list[str]:
    if not text:
        return []
    words = TICKER_PATTERN.findall(text)
    seen: set[str] = set()
    result: list[str] = []
    for w in words:
        if w in KNOWN_COMPANIES and w not in seen:
            seen.add(w)
            result.append(w)
    return result


def extract_entities(text: str) -> list[dict]:
    tickers = extract_tickers(text)
    entities: list[dict] = []
    seen_tickers: set[str] = set()
    for t in tickers:
        if t not in seen_tickers:
            seen_tickers.add(t)
            entities.append({
                "name": KNOWN_COMPANIES.get(t, t),
                "type": "company",
                "ticker": t,
                "asset_type": asset_type(t),
            })
    return entities
