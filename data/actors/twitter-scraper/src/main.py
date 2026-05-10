import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apify import Actor
from src.normalize import normalize_tweet

import httpx
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


TWITTER_SEARCH_URL = "https://twitter.com/search?q={query}&src=typed_query&f=live"
GOOGLE_NEWS_URL = "https://news.google.com/rss/search?q={query}+when:1d&hl=en-US&gl=US&ceid=US:en"


async def search_google_news(
    client: httpx.AsyncClient,
    query: str,
) -> list[dict]:
    tweets: list[dict] = []
    url = GOOGLE_NEWS_URL.format(query=query)

    try:
        resp = await client.get(url, headers={"User-Agent": "NarrativeOS/1.0"})
        resp.raise_for_status()

        import feedparser
        feed = feedparser.parse(resp.text)

        for entry in feed.entries[:10]:
            title = entry.get("title", "")
            source = entry.get("source", "") or entry.get("source_title", "")
            link = entry.get("link", "")

            if any(kw in title.lower() for kw in ["shares", "stock", "market", "bull", "bear"]):
                tweets.append({
                    "title": title[:200],
                    "body": title,
                    "url": link,
                    "author": source or "Google News",
                    "published_at": str(entry.get("published", "")),
                    "likes": 0,
                    "retweets": 0,
                    "replies": 0,
                    "search_query": query,
                })
    except Exception as e:
        Actor.log.warning("Google News search failed for %s: %s", query, e)

    return tweets


async def search_twitter_playwright(
    query: str,
    max_tweets: int,
    proxy_url: str | None = None,
) -> list[dict]:
    tweets: list[dict] = []
    url = TWITTER_SEARCH_URL.format(query=query)

    async with async_playwright() as p:
        proxy_settings = {}
        if proxy_url:
            proxy_settings["server"] = proxy_url

        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"],
        )
        ctx = await browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
            proxy=proxy_settings if proxy_settings else None,
        )
        await ctx.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        """)

        page = await ctx.new_page()

        try:
            await page.goto(url, wait_until="domcontentloaded", timeout=45000)
            await page.wait_for_timeout(8000)

            html = await page.content()
            soup = BeautifulSoup(html, "lxml")

            tweet_els = soup.select("article[data-testid='tweet']") or soup.select("div[data-testid='cellInnerDiv']")

            for tweet_el in tweet_els[:max_tweets]:
                try:
                    text_el = tweet_el.select_one("div[data-testid='tweetText']") or tweet_el.select_one("div[lang]")
                    text = text_el.get_text(strip=True) if text_el else ""

                    name_el = tweet_el.select_one("div[data-testid='User-Names'] a")
                    author = name_el.get_text(strip=True) if name_el else ""

                    link_el = tweet_el.select_one("a[href*='/status/']")
                    tweet_url = ""
                    if link_el and link_el.get("href"):
                        href = link_el["href"]
                        tweet_url = href if href.startswith("http") else f"https://twitter.com{href}"

                    if not text:
                        continue

                    tweets.append({
                        "title": text[:200],
                        "body": text,
                        "url": tweet_url,
                        "author": author,
                        "published_at": "",
                        "likes": 0,
                        "retweets": 0,
                        "replies": 0,
                        "search_query": query,
                    })
                except Exception:
                    continue

        except Exception as e:
            Actor.log.warning("Twitter search failed for %s: %s", query, e)
        finally:
            await browser.close()

    return tweets


async def main() -> None:
    async with Actor:
        Actor.log.info("NarrativeOS Twitter Scraper — starting (Google News + Nitter fallback)")

        proxy_url = None
        try:
            proxy = await Actor.create_proxy_configuration()
            if proxy and proxy.is_enabled:
                proxy_url = await proxy.get_url()
                Actor.log.info("Using Apify proxy")
        except Exception as e:
            Actor.log.info("Proxy not available: %s", e)

        inp = await Actor.get_input() or {}
        tickers: list[str] = inp.get("tickers", ["$NVDA", "$AMD", "$AAPL", "$MSFT"])
        max_tweets: int = inp.get("max_tweets", 20)

        Actor.log.info("Searching %d tickers, max %d tweets each", len(tickers), max_tweets)

        all_tweets: list[dict] = []

        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            for ticker in tickers:
                query = ticker.replace(" ", "")
                Actor.log.info("Searching: %s", query)

                tweet_results = await search_google_news(client, query)
                Actor.log.info("  → %d tweets via Google News for %s", len(tweet_results), query)
                all_tweets.extend(tweet_results)

                if len(tweet_results) < max_tweets:
                    remaining = max_tweets - len(tweet_results)
                    pw_tweets = await search_twitter_playwright(query, remaining, proxy_url)
                    Actor.log.info("  → %d tweets via PW for %s", len(pw_tweets), query)
                    all_tweets.extend(pw_tweets)

        Actor.log.info("Collected %d raw tweets total", len(all_tweets))

        for tweet in all_tweets:
            event = normalize_tweet(tweet)
            await Actor.push_data(event)

        Actor.log.info("Twitter scrape complete — %d events pushed", len(all_tweets))

        Actor.log.info("Collected %d raw tweets total", len(all_tweets))

        for tweet in all_tweets:
            event = normalize_tweet(tweet)
            await Actor.push_data(event)

        Actor.log.info("Twitter scrape complete — %d events pushed", len(all_tweets))


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
