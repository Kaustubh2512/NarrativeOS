from __future__ import annotations

import logging
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)


def search_news(ticker: str, max_results: int = 5) -> list[str]:
    headlines = _google_news_rss(ticker, max_results)
    if not headlines:
        headlines = _search_fallback(ticker, max_results)
    return headlines


def _google_news_rss(ticker: str, max_results: int) -> list[str]:
    try:
        import httpx
        url = f"https://news.google.com/rss/search?q={ticker}+stock&hl=en-US&gl=US&ceid=US:en"
        resp = httpx.get(url, timeout=15, follow_redirects=True,
                         headers={"User-Agent": "Mozilla/5.0"})
        if resp.status_code != 200:
            return []
        root = ET.fromstring(resp.text)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        items = root.findall(".//item")
        headlines = []
        for item in items[:max_results]:
            title_el = item.find("title")
            if title_el is not None and title_el.text:
                headlines.append(title_el.text)
        return headlines
    except Exception as e:
        logger.warning("Google News RSS failed for %s: %s", ticker, e)
        return []


def _search_fallback(ticker: str, max_results: int) -> list[str]:
    try:
        from ddgs import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(f"{ticker} stock news", max_results=max_results))
            return [r.get("title", "") for r in results if r.get("title")]
    except Exception as e:
        logger.warning("DDGS search fallback failed for %s: %s", ticker, e)
    return []


def fetch_url_text(url: str) -> str | None:
    try:
        import httpx
        resp = httpx.get(url, timeout=15, follow_redirects=True,
                         headers={"User-Agent": "Mozilla/5.0"})
        if resp.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(resp.text, "html.parser")
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()
            text = soup.get_text(separator=" ", strip=True)
            return text[:3000]
    except Exception as e:
        logger.warning("fetch_url failed for %s: %s", url, e)
    return None
