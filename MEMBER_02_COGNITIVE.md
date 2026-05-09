# Member 2: The Cognitive Lead (Zynd)

You own the **reasoning layer** of NarrativeOS. You build the multi-agent mesh that turns raw data into trading signals.

## Domain

```
/agents/
├── registry/          # Zynd agent cards + registration configs
├── graph/             # LangGraph flow definitions (TradingAgents-inspired)
├── debate/            # Bull/Bear structured debate protocol
├── consensus/         # Confidence-weighted signal aggregation
├── webhooks/          # Event-driven triggers from Apify pipeline
└── prompts/           # LLM prompt templates per agent role
```

## Core Tool: Zynd AI — Full Feature Map

| Feature | How You Use It |
|---------|----------------|
| **Agent DNS Registry** | Register all 8 NarrativeOS agents (Data Acquisition, Narrative, Sentiment, Market Correlation, Debate, Risk, Strategy, Visualization) as discoverable Zynd entities with stable FQANs |
| **Ed25519 Identity + HD Key Derivation** | Every agent gets a cryptographic identity linked to your developer key — verifiable audit trail for every trade signal |
| **Framework integrations** (LangChain, LangGraph, PydanticAI) | Build the TradingAgents-inspired agent graph using LangGraph for stateful multi-agent workflows |
| **Persona Agents** | Optionally represent the entire NarrativeOS as a "persona" on the Zynd network for external discovery and collaboration |
| **Agent-to-agent messaging** | Implement the Debate protocol (Bull Agent ↔ Bear Agent) and handoff chain: Analyst Team → Researcher Team → Trader → Risk Manager → Portfolio Manager |
| **Hybrid Search** (BM25 + vector semantic) | Agents dynamically discover relevant peer agents based on narrative context |
| **Heartbeat & Liveness** | Health monitoring — get alerted if Sentiment Analyst or Debate agents go silent |
| **x402 Micropayments** | Pay-per-call for premium data sources (e.g., paying Member 1's Actor per-query) or monetize agent services externally |
| **One-click hosting** (deployer.zynd.ai) | Quick iteration during development — deploy an agent in 30 seconds |
| **Webhooks** | Trigger re-analysis pipeline when new NarrativeEvents arrive from Member 1's Apify pipeline |
| **MCP Server** | Expose agent reasoning capabilities to Member 3's Superplane canvases and external tools |
| **n8n nodes** | Let Member 3 trigger agent analysis via no-code workflows |
| **SDK** (Python / TypeScript) | Full programmatic control of agent lifecycle, registration, and messaging |

## Sprint 1 Tasks

1. Install Zynd SDK + CLI, run `zynd init` to create developer identity
2. Study [TradingAgents source](https://github.com/TauricResearch/TradingAgents) — deeply understand `tradingagents/graph/trading_graph.py`, agent role separation, debate rounds, and the Portfolio Manager decision flow
3. Register NarrativeOS developer handle on Zynd DNS Registry
4. Build **Narrative Intelligence Agent**: consumes NarrativeEvents from Apify, performs topic clustering, narrative segmentation, entity extraction
5. Build **Sentiment Reasoning Agent**: scores polarity (bullish/bearish/neutral), emotional intensity, uncertainty
6. Build **Debate System**: Bull Agent + Bear Agent + Arbiter — structured debate with configurable rounds
7. Register all agents on Zynd with proper Agent Cards (`.well-known/agent.json`)
8. Set up **heartbeat + liveness** for all agents
9. Write agent-to-agent messaging handlers for the Analyst → Researcher → Trader → Risk → PM handoff chain

## Deliverables

- 3+ Zynd-registered agents with signed identities
- LangGraph state graph implementing the TradingAgents architecture
- Structured debate protocol with configurable rounds
- Agent webhook endpoints that receive NarrativeEvents from Member 1
- Confidence-weighted output signals consumed by Member 3

## API Contract (Input)

Receives `NarrativeEvent` objects (see `API_CONTRACT.md`) from Member 1's Apify pipeline. Each event contains source, title, body, ticker mentions, and metadata.

## API Contract (Output)

Produces `AnalysisSignal` objects with: `signal_id`, `ticker`, `direction` (BUY/SELL/HOLD/WATCHLIST), `confidence` (0.0–1.0), `narrative_summary`, `sentiment_polarity`, `debate_summary`, `risk_score`, `reasoning_trace`, `supporting_events[]`.

## Dependencies

- Needs Member 1's NarrativeEvent schema (defined in `API_CONTRACT.md`) to know what data shape to expect
- Needs Member 3 to route events through Superplane canvases and to provide a dashboard for signal review
- Reads TradingAgents source for architectural patterns

## GitHub Copilot Usage

- Use **Copilot Chat** with `@workspace` to navigate the repo and understand agent data flow
- Use **Copilot** to generate LangGraph node/edge boilerplate
- Use **Copilot** for prompt engineering — iterate on system prompts for each agent role
- Use **Copilot Agents** to refactor agent communication protocols repo-wide
