# NarrativeOS

**Decentralized Multi-Agent Narrative Intelligence for Financial Markets**

An autonomous system with 8 specialized AI agents that monitors narratives across news, SEC filings, and social media — scoring sentiment, debating market impact, and generating confidence-weighted trading signals.

```
Data Ingestion  →  Narrative Intel  →  Sentiment  →  Debate  →  Signal
 (Apify)           (LangGraph)         (LLM)        (Bull/Bear)  (Strategy)
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
# Full interactive walkthrough (starts pipeline, pauses between steps)
./demo.sh

# Quick run without pauses
./demo.sh --fast

# Skip pipeline execution, use existing bridge data
./demo.sh --skip-pipeline
```

---

## Architecture

**8 agents** in a directed reasoning pipeline:

| # | Agent | Responsibility | Technology |
|---|-------|---------------|------------|
| 1 | Data Acquisition | Ingest News, SEC, RSS | Apify Actors |
| 2 | Narrative Intelligence | Topic clustering, momentum | LangGraph |
| 3 | Sentiment Reasoning | Bullish/bearish scoring | OpenRouter LLM |
| 4 | Market Correlation | Map narratives → assets | Entity extractor (50+ tickers) |
| 5 | Debate System | Bull/Bear/Arbiter 3-round | LLM adversarial reasoning |
| 6 | Risk Intelligence | Anomaly detection, confidence | Rule-based + LLM |
| 7 | Strategy | BUY/SELL/HOLD signals | Consensus weighting |
| 8 | Visualization | Dashboard, flow graph | Next.js + React Flow |

**Backtest accuracy:** 62.5% overall (10/16), 83.3% on crypto/commodities (5/6).

---

## Stack

- **Ingestion:** Apify SDK v3, Crawlee, 4 custom Actors
- **Agents:** LangGraph, OpenRouter, Python 3.12
- **Orchestration:** Zynd AI agent registry, Superplane bridge
- **LLM:** gpt-4o-mini via OpenRouter (configurable via `LLM_MODEL`)
- **Frontend:** Next.js, TailwindCSS, React Flow, Framer Motion
- **Deployment:** Render.com (bridge), Vercel (dashboard)

---

## Project Structure

```
├── data/actors/              Apify Actors (news, SEC, Twitter, Reddit)
├── data/pipelines/           Ingestion, enrichment, entity extraction
├── agents/                   8 AI agents + LangGraph workflow
│   ├── graph/workflow.py     E2E LangGraph pipeline
│   ├── debate/engine.py      3-round adversarial debate
│   └── backtest/             Historical event backtesting
├── infra/superplane/         FastAPI bridge (Render.com)
├── infra/dashboard/          Next.js frontend (Vercel)
├── agent.py                  Zynd agent wrapper
└── render.yaml               Render Blueprint
```

See [AGENTS.md](AGENTS.md) for the full system specification.

---

Built for the **Agentic Hackathon** — Agent Mesh Track.
