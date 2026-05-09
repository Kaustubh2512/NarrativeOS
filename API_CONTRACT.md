# API Contract — NarrativeOS Event Schemas

This file defines the shared data contracts between the 3 team members. All pipelines must conform to these schemas.

---

## NarrativeEvent (Member 1 → Member 2)

Produced by Apify Actors. Consumed by Zynd agents via webhook or dataset polling.

```json
{
  "id": "evt_20260509_reddit_001",
  "source": "reddit",
  "source_actor": "narrativeos-reddit-scraper",
  "title": "NVDA earnings beat expectations by 15%",
  "body": "Full text of the post or article...",
  "url": "https://reddit.com/r/wallstreetbets/...",
  "author": "username",
  "published_at": "2026-05-09T14:30:00Z",
  "collected_at": "2026-05-09T14:31:15Z",
  "ticker_mentions": ["NVDA", "AMD"],
  "entities": [
    {"name": "NVIDIA", "type": "company", "ticker": "NVDA"},
    {"name": "AMD", "type": "company", "ticker": "AMD"}
  ],
  "sentiment_score": null,
  "metadata": {
    "upvotes": 1520,
    "comments": 340,
    "subreddit": "wallstreetbets",
    "post_type": "DD"
  }
}
```

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique event ID (`{source}_{timestamp}_{seq}`) |
| `source` | string | yes | One of: `reddit`, `news`, `sec_filing`, `twitter`, `rss` |
| `source_actor` | string | yes | Apify Actor name that produced this event |
| `title` | string | yes | Headline or post title |
| `body` | string | yes | Full text content |
| `url` | string | yes | Permalink to original content |
| `author` | string | no | Author/source attribution |
| `published_at` | string (ISO8601) | yes | Original publication timestamp |
| `collected_at` | string (ISO8601) | yes | When Apify collected it |
| `ticker_mentions` | string[] | yes | Extracted ticker symbols (uppercase) |
| `entities` | object[] | no | Named entities with type mapping |
| `sentiment_score` | float | no | Pre-scored sentiment (-1 to 1), null if not pre-processed |
| `metadata` | object | no | Source-specific metadata |

### Delivery

- **Option A (recommended):** Apify webhook → Member 3's Superplane ingress canvas → routes to Member 2's agent endpoint
- **Option B (direct):** Member 2 polls Apify dataset via `apify_client` API

---

## AnalysisSignal (Member 2 → Member 3)

Produced by Zynd agent mesh (Portfolio Manager). Consumed by Superplane execution canvas.

```json
{
  "signal_id": "sig_20260509_nvda_001",
  "ticker": "NVDA",
  "direction": "BUY",
  "confidence": 0.78,
  "narrative_summary": "Strong semiconductor demand driven by AI inference workloads at hyperscalers",
  "sentiment_polarity": 0.65,
  "emotional_intensity": 0.4,
  "debate_summary": {
    "bull_case": "Data center revenue continuing to grow 200% YoY, new Blackwell architecture entering mass production",
    "bear_case": "Valuation at 35x forward earnings, potential export restriction escalation",
    "arbiter_ruling": "Bull case stronger — growth fundamentals outweigh valuation concerns at this stage",
    "debate_rounds": 3
  },
  "risk_score": 0.35,
  "risk_factors": ["Valuation multiple compression", "Geopolitical export risk"],
  "reasoning_trace": [
    "News Analyst: NVDA announced 3 new hyperscaler partnerships",
    "Sentiment Analyst: Bullish momentum score 72/100 across tracked sources",
    "Technical Analyst: RSI at 62, MACD bullish crossover",
    "Bull Researcher: Growth trajectory supports continued upside",
    "Bear Researcher: Forward PE above 5-year average"
  ],
  "supporting_events": [
    "evt_20260509_reddit_001",
    "evt_20260509_news_003",
    "evt_20260509_sec_002"
  ],
  "generated_at": "2026-05-09T15:00:00Z",
  "agent_version": "narrativeos-v0.1.0"
}
```

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `signal_id` | string | yes | Unique signal ID |
| `ticker` | string | yes | Target ticker symbol |
| `direction` | string | yes | `BUY`, `SELL`, `HOLD`, or `WATCHLIST` |
| `confidence` | float | yes | 0.0 (low) to 1.0 (high) |
| `narrative_summary` | string | yes | One-paragraph narrative explanation |
| `sentiment_polarity` | float | yes | -1.0 (bearish) to 1.0 (bullish) |
| `emotional_intensity` | float | yes | 0.0 (calm) to 1.0 (panic/euphoria) |
| `debate_summary` | object | yes | Bull/Bear positions + Arbiter ruling |
| `risk_score` | float | yes | 0.0 (low risk) to 1.0 (high risk) |
| `risk_factors` | string[] | no | Specific risk flags |
| `reasoning_trace` | string[] | yes | Step-by-step reasoning chain |
| `supporting_events` | string[] | yes | NarrativeEvent IDs that influenced this signal |
| `generated_at` | string (ISO8601) | yes | Signal generation timestamp |
| `agent_version` | string | yes | Version of the agent mesh that produced it |

---

## Webhook Endpoints (Contract Between Members)

### Member 1 → Member 3 (Apify → Superplane)

```
POST /api/v1/webhooks/apify-event
Content-Type: application/json
Body: NarrativeEvent
```

### Member 3 → Member 2 (Superplane → Zynd)

```
POST <zynd-agent-url>/webhook/analyze
Content-Type: application/json
Body: { "events": NarrativeEvent[], "trigger": "scheduled|webhook|manual" }
```

### Member 2 → Member 3 (Zynd → Superplane)

```
POST /api/v1/webhooks/signal
Content-Type: application/json
Body: AnalysisSignal
```

---

## Versioning

This contract is version `v1`. Any changes to the schema must be:
1. Proposed as a PR updating this file
2. Reviewed by all 3 members
3. Tagged with a new version number (e.g. `v2`)
4. Backward-compatible within the same major version (add optional fields, don't remove required ones)
