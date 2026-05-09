from apify import Actor
from data.pipelines.normalize import normalize_reddit_post
from data.stream.event_bus import EventBus


async def main() -> None:
    async with Actor:
        Actor.log.info("NarrativeOS Reddit Scraper — starting")

        inp = await Actor.get_input() or {}
        subreddits: list[str] = inp.get("subreddits", ["wallstreetbets", "investing", "stocks"])
        max_posts: int = inp.get("max_posts", 25)
        sort: str = inp.get("sort", "new")
        mode: str = inp.get("mode", "playwright")

        event_bus = EventBus()

        if mode == "api" and _has_praw_credentials():
            posts = await _scrape_via_praw(subreddits, max_posts, sort)
        else:
            posts = await _scrape_via_playwright(subreddits, max_posts, sort, inp.get("time_filter", "day"))

        Actor.log.info("Collected %d raw posts from %s", len(posts), subreddits)

        for post in posts:
            event = normalize_reddit_post(post)
            await Actor.push_data(event)
            event_bus.emit(event)

        event_bus.flush()
        Actor.log.info("Reddit scrape complete — %d events pushed", len(posts))


def _has_praw_credentials() -> bool:
    import os
    return bool(os.environ.get("NARRATIVEOS_REDDIT_CLIENT_ID"))


async def _scrape_via_praw(subreddits: list[str], max_posts: int, sort: str) -> list[dict]:
    import praw
    import os

    reddit = praw.Reddit(
        client_id=os.environ["NARRATIVEOS_REDDIT_CLIENT_ID"],
        client_secret=os.environ.get("NARRATIVEOS_REDDIT_CLIENT_SECRET", ""),
        user_agent=os.environ.get("NARRATIVEOS_REDDIT_USER_AGENT", "NarrativeOS/1.0"),
    )

    posts: list[dict] = []
    for sub_name in subreddits:
        sub = reddit.subreddit(sub_name)
        method = getattr(sub, sort, sub.hot)
        for submission in method(limit=max_posts):
            posts.append({
                "id": submission.id,
                "title": submission.title,
                "selftext": submission.selftext[:5000],
                "url": submission.url,
                "permalink": f"https://reddit.com{submission.permalink}",
                "author": str(submission.author) if submission.author else "[deleted]",
                "created_utc": submission.created_utc,
                "ups": submission.ups,
                "score": submission.score,
                "num_comments": submission.num_comments,
                "subreddit": sub_name,
                "link_flair_text": submission.link_flair_text or "",
            })
    return posts


async def _scrape_via_playwright(
    subreddits: list[str], max_posts: int, sort: str, time_filter: str,
) -> list[dict]:
    from playwright.async_api import async_playwright

    posts: list[dict] = []
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page()

        for sub_name in subreddits:
            url = f"https://old.reddit.com/r/{sub_name}/{sort}/"
            if sort == "top":
                url += f"?t={time_filter}"
            Actor.log.info("Scraping %s", url)

            try:
                await page.goto(url, timeout=30000, wait_until="domcontentloaded")
                await page.wait_for_selector("#siteTable", timeout=10000)
            except Exception as e:
                Actor.log.warning("Failed to load %s: %s", url, e)
                continue

            rows = await page.query_selector_all("#siteTable > .thing")
            for row in rows[:max_posts]:
                try:
                    title_el = await row.query_selector("a.title")
                    title = await title_el.inner_text() if title_el else ""
                    href = await title_el.get_attribute("href") if title_el else ""

                    body_el = await row.query_selector(".usertext-body")
                    body = await body_el.inner_text() if body_el else ""

                    author_el = await row.query_selector(".author")
                    author = await author_el.inner_text() if author_el else "[deleted]"

                    time_el = await row.query_selector("time")
                    time_attr = await time_el.get_attribute("datetime") if time_el else ""

                    score_el = await row.query_selector(".score.unvoted")
                    score_text = await score_el.get_attribute("title") if score_el else "0"
                    score_text = score_text or "0"

                    comment_el = await row.query_selector("a.comments")
                    comment_text = await comment_el.inner_text() if comment_el else "0 comments"

                    flair_el = await row.query_selector(".linkflairlabel")
                    flair = await flair_el.inner_text() if flair_el else ""

                    posts.append({
                        "title": title.strip(),
                        "selftext": body.strip()[:5000],
                        "url": href if href.startswith("http") else f"https://reddit.com{href}",
                        "permalink": href,
                        "author": author,
                        "created_utc": time_attr,
                        "score": int(score_text.replace(",", "")),
                        "num_comments": int(comment_text.split()[0]) if comment_text.split() else 0,
                        "subreddit": sub_name,
                        "link_flair_text": flair,
                    })
                except Exception as e:
                    Actor.log.debug("Row parse error: %s", e)
                    continue

        await browser.close()

    return posts


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
