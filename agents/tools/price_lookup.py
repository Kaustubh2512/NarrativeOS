from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def lookup_price(ticker: str) -> dict | None:
    try:
        import yfinance as yf
    except ImportError:
        logger.warning("yfinance not installed")
        return None

    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d")
        if hist.empty:
            return None

        last = hist.iloc[-1]
        prev_close = hist.iloc[-2]["Close"] if len(hist) > 1 else last["Close"]
        change_pct = ((last["Close"] - prev_close) / prev_close) * 100

        return {
            "ticker": ticker,
            "price": round(last["Close"], 2),
            "change_pct": round(change_pct, 2),
            "day_high": round(last["High"], 2),
            "day_low": round(last["Low"], 2),
            "volume": int(last["Volume"]),
            "date": str(last.name.date()) if hasattr(last.name, "date") else str(last.name),
        }
    except Exception as e:
        logger.warning("yfinance lookup failed for %s: %s", ticker, e)
    return None
