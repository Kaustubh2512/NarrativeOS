# Apify MCP Integration

Zynd agents call NarrativeOS Actors **on-demand** for fresh data instead of waiting for scheduled pipeline runs.

## Quick Start

```python
from data.mcp.client import NarrativeOSDataClient

client = NarrativeOSDataClient()  # reads APIFY_TOKEN from env or .env

# Fetch fresh news
news = client.fetch_news(max_articles=20)

# Fetch SEC filings
filings = client.fetch_sec_filings(tickers=["NVDA", "AMD"])

# Fetch both in parallel
data = client.fetch_both(max_articles=10, max_filings=3)
```

## MCP Server (AI Assistant Use)

The `.mcp.json` at project root exposes Apify Actors as MCP tools for VS Code/Cursor.

To enable: set `APIFY_TOKEN` in your env or in `.env`.

## Architecture

```
Zynd Agent
  │
  ├── NarrativeOSDataClient.fetch_news()     ──►  Apify News Actor (on-demand)
  ├── NarrativeOSDataClient.fetch_sec_filings()  ──►  Apify SEC Actor (on-demand)
  │
  └── Scheduled runs (hourly/daily)           ──►  Apify datasets → pipeline.py
```
