# Member 1: The Sensory Lead (Apify)

You own the **perception layer** of NarrativeOS. Every insight the system produces begins with data you collect.

## Domain

```
/data/
├── actors/          # Apify Actor definitions
├── pipelines/       # Data normalization + enrichment scripts
├── stream/          # Real-time event feed consumed by agents
└── schemas/         # Input/output schemas for each Actor
```

## Core Tool: Apify — Full Feature Map

| Feature | How You Use It |
|---------|----------------|
| **Actors** (Playwright/Cheerio crawlers) | Scrape Reddit (r/wallstreetbets, r/investing), news feeds, SEC EDGAR filings, social media sentiment |
| **Proxy management** (residential / datacenter / Google SERP) | Avoid rate-limiting and geo-blocking during continuous scraping |
| **Scheduling** (cron expressions) | Run data collection on fixed intervals (hourly news check, daily SEC crawl, continuous Reddit stream) |
| **Storage** (datasets, key-value stores, request queues) | Structured output stored in Apify datasets — each source gets its own dataset collection |
| **Standby mode** (persistent HTTP server) | Run an Actor as a live API endpoint — agents query it on-demand for fresh data instead of waiting for a scheduled run |
| **Metamorph** (Actor chaining) | Chain Actors: Reddit scraper → sentiment preprocessor → normalized dataset in one pipeline |
| **Apify MCP server** | Expose every Actor as a tool via MCP — Zynd agents can call `apify_mcp_run_actor("reddit-scraper", {query: "NVDA"})` directly from their reasoning loop |
| **Webhooks** | Trigger agent re-analysis automatically when a data collection run completes |
| **Integrations** (LangChain, CrewAI, n8n, Make) | Pipe scraped data directly into agent context or no-code workflows |
| **Monitoring** | Set up alerts for data quality drops, scraper failures, or schedule misses |
| **API + SDK** (Python/JS) | Control everything programmatically — `apify_client` for dataset reads, Actor runs, task management |

## Sprint 1 Tasks

1. Set up Apify account, generate API token, install Apify CLI
2. Build **Reddit Actor**: scrape r/wallstreetbets, r/investing, r/stocks → structured dataset with title, body, score, comments, timestamp, ticker mentions
3. Build **News Actor**: scrape financial news RSS feeds and top sites (Reuters, Bloomberg, Yahoo Finance) → normalized article objects
4. Build **SEC Filing Actor**: pull latest 10-K, 10-Q, 8-K filings for tracked tickers from EDGAR
5. Set up **schedules**: Reddit continuous, news hourly, SEC daily
6. Write **normalization pipeline**: deduplication, entity extraction (ticker → company mapping), timestamp normalization, source tagging
7. Define and publish **NarrativeEvent schema** in `API_CONTRACT.md`
8. Set up **Apify → webhook** that fires on each completed Actor run
9. Test data output quality — run sample queries against datasets

## Deliverables

- 3 working Apify Actors (Reddit, News, SEC) deployed and scheduled
- Python normalization scripts in `/data/pipelines/`
- A real-time or near-real-time JSON event stream consumed by Member 2's agents
- Monitoring alerts on all Actors

## API Contract (Output)

Every Actor produces events conforming to the shared `NarrativeEvent` schema defined in `API_CONTRACT.md`. At minimum each event includes: `id`, `source`, `title`, `body`, `url`, `published_at`, `collected_at`, `ticker_mentions`, `entities`, `metadata`.

## Dependencies

- Needs Member 2 to expose a webhook endpoint that receives NarrativeEvents, or to poll Apify datasets
- Needs Member 3 to route Apify webhook calls through Superplane canvases

## GitHub Copilot Usage

- Use **Copilot Chat** with `@workspace` to understand how NarrativeEvent is consumed by agents
- Use **Copilot** to generate Playwright selectors and Cheerio parse logic
- Use **Copilot** for boilerplate Actor input schemas (`.actor/input_schema.json`)
- Use **Copilot Agents** for repo-wide refactors if the data schema changes
