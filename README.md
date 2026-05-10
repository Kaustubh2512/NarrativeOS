# NarrativeOS

**Decentralized Multi-Agent Narrative Intelligence for Financial Markets**

An autonomous system with 8 specialized AI agents that monitors narratives across news, SEC filings, and social media — scoring sentiment, debating market impact, and generating confidence-weighted trading signals.

```
 Data Ingestion         Narrative Intel         Sentiment            Debate              Signal
 ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
 │  Apify       │ →  │  LangGraph   │ →  │  LLM /       │ →  │  Bull/Bear/  │ →  │  Strategy    │
 │  Actors      │    │  Workflow    │    │  Keyword     │    │  Arbiter     │    │  Consensus   │
 │  (News, SEC, │    │  (4 nodes)   │    │  Sentiment   │    │  (3 rounds)  │    │  Weighting   │
 │  RSS, Twitter)│   │              │    │              │    │              │    │              │
 └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
        │                    │                   │                    │                   │
   Superplane          Zynd AI               OpenRouter           Debate              Bridge
   Bridge (Push)       Registry              gpt-4o-mini          Engine              API
```

---

## Live Demo

| Service | URL |
|---------|-----|
| Dashboard | https://narrative-os-theta.vercel.app |
| Bridge API | https://narrativeos-bridge.onrender.com/docs |
| GitHub | https://github.com/0xYuvi/NarrativeOS |

---

## Quick Start

```bash
# Full interactive walkthrough (runs pipeline, pauses between steps)
./demo.sh

# Quick mode — runs everything at once
./demo.sh --fast

# Use existing bridge data, skip pipeline execution
./demo.sh --skip-pipeline

# Prerequisites: Python 3.12+, .env file with API keys
python3 -m venv .venv && source .venv/bin/activate
pip install -r agents/requirements.txt
```

---

## How Tracks Are Used

### 🕸️ Apify — Internet Sensory Layer

Apify powers **Data Acquisition** — 3 on-demand Actors fetch structured financial intelligence:

| Actor | ID | Source | Output |
|-------|----|--------|--------|
| News RSS | `rxTkx6ACrjUdlCgNO` | Dow Jones, Yahoo Finance, investing.com | Article title, body, URL, timestamp |
| SEC EDGAR | `Q3cP0eqIAlqH2YsrI` | SEC EDGAR filings | Full-text 10-K, 10-Q, 8-K filings |
| Twitter | `0XfiV1wgo6qLV1Xig` | Tweets by cashtag (e.g. `$NVDA`) | Tweet text, author, engagement |

4 additional custom Actors deployed via `apify_client` Python SDK (`data/actors/`):
- **narrativeos-news-scraper** (v0.1.4) — RSS + CheerioCrawler
- **narrativeos-sec-scraper** — EDGAR full-text extraction
- **narrativeos-twitter-scraper** (v0.1.6) — Google News RSS fallback
- **narrativeos-reddit-scraper** (v0.1.19) — 403 blocked (datacenter IPs flagged)

**Integration points:**
- `data/mcp/client.py` — `NarrativeOSDataClient` fetches all 3 actors in parallel via `ThreadPoolExecutor`, falls back to cached datasets on memory limit errors
- `data/pipelines/pipeline.py` — `run_pipeline()` fires actors, enriches events (sentiment scoring, entity extraction), deduplicates, feeds into LangGraph
- `data/pipelines/entity_extractor.py` — extracts ticker mentions from text using 47-company regex, maps to `AssetType`
- `data/actors/` — individual Actor source code deployable to Apify cloud
- `agents/tools/web_search.py` — Google News RSS via httpx + DuckDuckGo fallback for agent research

**Free tier:** 8192MB memory limit, 5 datacenter proxies (BUYPROXIES94952 group). Residential proxy required for Reddit.

---

### ⚡ Zynd AI — Agent Registry & Mesh

Zynd provides **decentralized agent discovery, identity, and inter-agent communication** via the A2A protocol.

The system registers as a Zynd agent named **`narrativeos-cognitive`** with tags `["narrative", "sentiment", "debate", "trading"]`:

| Property | Value |
|----------|-------|
| Agent name | `narrativeos-cognitive` |
| Protocol | A2A (JSON-RPC `message/send`) |
| Handler | `on_message(run_analysis_pipeline)` |
| Port | 5005 (env `ZYND_SERVER_PORT`) |
| SDK | `zyndai` v0.6.0 |
| Tunnel | ngrok (manual, not managed by SDK) |

**Integration points:**
- `agent.py` — `AgentConfig` reads from `agent.config.json` + env vars, registers agent, listens on `/a2a/v1`
- `data/mcp/` — exposes Apify Actors as callable services Zynd agents can discover and invoke
- `agents/debate/` — Bull/Bear/Arbiter agents communicate via structured message passing (Zynd protocol patterns)
- `agents/graph/workflow.py` — LangGraph nodes execute independently as modular services
- `agent.config.json` — registry URL, server port, agent metadata

**Communication flow:** External message → `on_message` → `_fetch_data()` (Apify) → `run_analysis()` (LangGraph) → `push_signal()` (Superplane bridge) → response.

---

### ⚙️ Superplane — Workflow Orchestration

Superplane orchestrates **long-running event-driven agent workflows** with execution tracing and state management:

| Pipeline Stage | Canvas File | Entry Point | Exit Point |
|---------------|-------------|-------------|------------|
| Ingress | `01-ingress.yaml` | Data ingestion via Apify | Structured NarrativeEvent |
| Analysis | `02-analysis.yaml` | LangGraph agent graph | AnalysisSignal |
| Execution | `03-execution.yaml` | Signal validation | Bridge push |

**Integration points:**
- `infra/superplane/bridge.py` — FastAPI server (port 8765) with 9 endpoints: status, signals CRUD, events CRUD, canvas listing
- `infra/superplane/client.py` — `push_signal()` / `push_event()` with 5s timeout, used by pipeline and Zynd agent
- `infra/superplane/data/` — flat JSON persistence (`executed_signals.json`, `ingress_events.json`)
- `infra/superplane/canvases/` — 3 Superplane workflow YAML definitions
- `infra/superplane/Dockerfile` — containerized for Render.com deployment
- `render.yaml` — Render Blueprint: `rootDir: infra/superplane`, `plan: free`

**Deployed endpoints:**
- `GET /health` — health check
- `GET /api/v1/status` — pipeline metrics (24h windows)
- `GET /api/v1/datasets/executed_signals/items` — latest signals
- `POST /api/v1/datasets/executed_signals/items` — push signal
- `GET /api/v1/datasets/ingress/items` — latest events
- `POST /api/v1/datasets/ingress/items` — push event

Dashboard accesses these through Vercel serverless function proxies (`/api/status`, `/api/signals`, `/api/events`).

---

## Architecture — 8 Agent Pipeline

The system graph identifies these core abstractions (god nodes by edge count):

| Rank | Node | Edges | Role |
|------|------|-------|------|
| 1 | `main()` | 19 | Pipeline entry point |
| 2 | `SignalAggregator` | 14 | Generates final signal from debate output |
| 3 | `NarrativeIntelligenceAgent` | 13 | Clusters topics, computes momentum |
| 4 | `NarrativeOSDataClient` | 12 | Apify fetch orchestration |
| 5 | `SentimentVector` | 11 | Polarity / intensity / instability |
| 6 | `DebateEngine` | 11 | 3-agent adversarial reasoning |
| 7–9 | `BullAgent`, `BearAgent`, `ArbiterAgent` | 10 each | Debate participants |

### Pipeline Steps

**Step 1: Narrative Intelligence**
- Clusters events by ticker
- LLM-enriches cluster themes via OpenRouter
- Computes momentum score (event velocity)
- `agents/narrative_intelligence.py`

**Step 2: Sentiment Reasoning**
- LLM sentiment analysis with structured JSON output
- Falls back to keyword scoring when LLM unavailable
- Produces `SentimentVector`: polarity, intensity, instability
- `agents/sentiment.py`

**Step 3: Debate System**
- Bull Agent argues optimistic case from event data
- Bear Agent argues pessimistic case
- Arbiter rules BUY/SELL/HOLD with confidence
- LLM-powered with detailed rationale per round
- `agents/debate/engine.py`

**Step 4: Signal Generation**
- Aggregates debate output into `AnalysisSignal`
- Computes risk score from sentiment volatility
- Generates reasoning trace for explainability
- `agents/graph/workflow.py`

### Agent Tools

| Tool | Backend | Purpose |
|------|---------|---------|
| `web_search` | Google News RSS + DuckDuckGo | Real-time news lookup per ticker |
| `price_lookup` | yfinance | 5-day price history, day high/low, volume |
| `sec_lookup` | Local cached EDGAR | Recent SEC filing summaries per ticker |

Tools are disabled during backtesting (`use_tools=False`) to avoid contamination with live data.

---

## Entity Extraction & Asset Coverage

**47 mapped tickers** across 4 asset types in `agents/models.py`:

| Asset Type | Count | Examples |
|------------|-------|---------|
| Equities | 21 | NVDA, AAPL, MSFT, GOOGL, AMZN, META, TSLA, JPM, PLTR, AVGO, NFLX, DIS, BA, COIN, HOOD, MSTR |
| Crypto | 9 | BTC, ETH, SOL, XRP, DOGE, ADA, DOT, LINK, AVAX |
| Commodities | 15 | GOLD, SILVER, OIL, WTI, BRENT, NG, COPPER, CORN, WHEAT, SOY |
| ETFs | 2 | SPY, QQQ |

`data/pipelines/entity_extractor.py` mirrors the map for extraction from raw text. Tickers are identified by regex pattern matching in article headlines and bodies.

---

## Backtesting

**16 historical events** across equities (10) and crypto/commodities (6):

| Result | Count | Breakdown |
|--------|-------|-----------|
| Correct | 10 | NVDA BUY ✓, TSLA SELL ✓, BTC BUY ✓, OIL HOLD ✓, META BUY ✓, GOLD BUY ✓, ETH BUY ✓, AAPL HOLD ✓, AMD BUY ✓, JPM HOLD ✓ |
| Incorrect | 6 | PLTR HOLD (should be BUY), BA HOLD (should be SELL), COIN BUY (should be SELL), SOL HOLD (should be SELL), CORN HOLD (should be BUY), OIL HOLD (should be BUY — geopolitical supply disruption) |

**Accuracy:** 62.5% overall, 83.3% on crypto/commodities.

Events in `agents/backtest/events.py`, runner in `agents/backtest/runner.py`.

---

## Project Structure

```
├── agents/
│   ├── graph/workflow.py       LangGraph pipeline (4 nodes)
│   ├── debate/engine.py        Bull/Bear/Arbiter debate
│   ├── narrative_intelligence.py  Topic clustering + momentum
│   ├── sentiment.py            LLM + keyword sentiment analysis
│   ├── models.py               47 tickers, AssetType enum, event models
│   ├── llm.py                  OpenRouter client (gpt-4o-mini)
│   ├── tools/                  web_search, price_lookup, sec_lookup
│   └── backtest/               16 historical events + runner
│
├── data/
│   ├── actors/                 Apify Actor source code (4 actors)
│   ├── pipelines/
│   │   ├── pipeline.py         E2E ingestion + enrichment + LangGraph
│   │   └── entity_extractor.py Ticker regex + entity extraction
│   └── mcp/
│       └── client.py           NarrativeOSDataClient (Apify fetch)
│
├── infra/
│   ├── superplane/
│   │   ├── bridge.py           FastAPI server (port 8765, 9 endpoints)
│   │   ├── client.py           Push signal/event to bridge
│   │   ├── Dockerfile          Container for Render.com
│   │   ├── canvases/           3 Superplane workflow YAMLs
│   │   └── requirements.txt    fastapi, uvicorn, httpx
│   └── dashboard/
│       ├── src/pages/          Next.js pages (index, api/*)
│       ├── src/components/     AgentFlow, Threads, MagicBento, etc.
│       └── next.config.js
│
├── agent.py                    Zynd agent wrapper (port 5005)
├── agent.config.json           Zynd registry config
├── render.yaml                 Render Blueprint deployment
├── demo.sh                     Interactive walkthrough script
└── .github/workflows/ci.yml    Lint, test, validate, deploy
```

---

## Backend Stack

| Layer | Technology |
|-------|-----------|
| Data Ingestion | Apify SDK v3, Crawlee, 3 on-demand + 4 custom Actors |
| Agent Framework | LangGraph, Python 3.12 |
| LLM | OpenRouter → gpt-4o-mini (configurable via `LLM_MODEL`) |
| Agent Registry | Zynd AI SDK v0.6.0, A2A protocol |
| Workflow Engine | Superplane bridge (FastAPI) |
| Data Persistence | Flat JSON files (ephemeral on Render free tier) |
| Price Data | yfinance |
| Web Search | Google News RSS, DuckDuckGo Search |

## Frontend Stack

| Layer | Technology |
|-------|-----------|
| Framework | Next.js (Pages Router) |
| Styling | TailwindCSS, glassmorphism dark theme |
| Animation | Framer Motion, GSAP, OGL |
| Graph Visualization | React Flow v11 (8 custom glassmorphism nodes) |
| Canvas | Threads (particle network background) |
| Bento Grid | MagicBento (animated asset coverage tiles) |
| Marquee | LogoLoop (15 tech badges) |
| Icons | Lucide React |
| Fonts | Orbitron (headings), Exo 2 (body) |

Color scheme: gold `#F59E0B`, purple `#8B5CF6`, bg `#0F172A`, text `#F8FAFC.

---

## Deployment

| Service | Platform | URL | Type |
|---------|----------|-----|------|
| Superplane Bridge | Render.com | https://narrativeos-bridge.onrender.com | Docker (free tier) |
| Dashboard | Vercel | https://narrative-os-theta.vercel.app | Next.js (free tier) |
| CI/CD | GitHub Actions | `.github/workflows/ci.yml` | Lint + test + validate + conditional deploy |

**Proxy flow:** Dashboard API routes (`/api/status`, `/api/signals`, `/api/events`) proxy to Render bridge via Vercel serverless functions with 15s timeout. `NEXT_PUBLIC_BRIDGE_URL` env var on Vercel points to Render.

**Render free tier warning:** Container spins down after 15 min idle. Filesystem is ephemeral — data persisted in `data/` JSON files is lost on restart. Bridge supports cold-start pings.

---

## Demo Script

```bash
./demo.sh                        # Interactive walkthrough
./demo.sh --fast                 # Non-interactive
./demo.sh --skip-pipeline        # Skip pipeline, use existing bridge
```

The demo: verifies prerequisites (Python, `.env`, bridge reachable), tours the architecture and codebase, runs the E2E pipeline (82 events → LangGraph → signal), checks bridge status, and links to the live dashboard.

Built for the **Agentic Hackathon** — Agent Mesh Track.
