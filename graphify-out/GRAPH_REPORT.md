# Graph Report - NarrativeOS  (2026-05-10)

## Corpus Check
- 79 files · ~23,412 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 484 nodes · 631 edges · 65 communities (61 shown, 4 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 91 edges (avg confidence: 0.68)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `eb8ce4c4`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]

## God Nodes (most connected - your core abstractions)
1. `main()` - 19 edges
2. `SignalAggregator` - 14 edges
3. `NarrativeIntelligenceAgent` - 13 edges
4. `SentimentVector` - 11 edges
5. `DebateEngine` - 11 edges
6. `BullAgent` - 10 edges
7. `BearAgent` - 10 edges
8. `ArbiterAgent` - 10 edges
9. `NarrativeOSDataClient` - 10 edges
10. `_to_iso()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `run_analysis_pipeline()` --calls--> `run_analysis()`  [INFERRED]
  agent.py → agents/graph/workflow.py
- `run_analysis_pipeline()` --calls--> `push_signal()`  [INFERRED]
  agent.py → infra/superplane/client.py
- `run_pipeline()` --calls--> `SourceType`  [INFERRED]
  data/pipelines/pipeline.py → agents/models.py
- `run_pipeline()` --calls--> `run_analysis()`  [INFERRED]
  data/pipelines/pipeline.py → agents/graph/workflow.py
- `_fetch_data()` --calls--> `NarrativeOSDataClient`  [INFERRED]
  agent.py → data/mcp/client.py

## Communities (65 total, 4 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.09
Nodes (26): AgentPayload, AnalysisSignal, DebatePosition, DebateRound, DebateSummary, Entity, NarrativeEvent, NarrativeEventBatch (+18 more)

### Community 1 - "Community 1"
Cohesion: 0.1
Nodes (16): AgentState, SentimentVector, SentimentReasoningAgent, SignalAggregator, create_workflow(), debate_node(), narrative_intelligence_node(), run_analysis() (+8 more)

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (24): Agent Communication Model, Agent Mesh Architecture, Agent Registry Layer, AI and Agent Infrastructure, Apify, Backend, code:text (Apify Actors), Core Objectives (+16 more)

### Community 3 - "Community 3"
Cohesion: 0.19
Nodes (19): NamedTuple, extract_entities(), extract_tickers(), ExtractedEntity, build_event_id(), _detect_post_type(), _extract_domain(), normalize_article() (+11 more)

### Community 4 - "Community 4"
Cohesion: 0.11
Nodes (10): NarrativeOSDataClient, Apify On-Demand Client — Zynd agents call Actors for fresh data.  Usage:     fro, On-demand data client for Zynd agents.      Agents call fetch_news() or fetch_se, On-demand data client for Zynd agents.      Agents call fetch_news(), fetch_sec_, _fetch_data(), narrativeos-cognitive — Zynd-registered NarrativeOS agent mesh wrapper.  Runs th, Pull fresh data from Apify actors via MCP client., run_analysis_pipeline() (+2 more)

### Community 5 - "Community 5"
Cohesion: 0.16
Nodes (14): Direction, SourceType, Enum, assess(), compute_confidence_degradation(), compute_risk_score(), detect_anomalies(), estimate_volatility() (+6 more)

### Community 6 - "Community 6"
Cohesion: 0.12
Nodes (15): End-to-end pipeline integration test — chains all 5 agents (correlation → risk →, Bearish event → correlation → risk → strategy (expected WATCHLIST or HOLD)., Execution API rejects signals below confidence threshold., Execution properly enforces human approval., Execution API rejects HOLD/WATCHLIST signals (no trade needed)., Risk agent flags anomalies in hype/fear narratives., Every agent and service reports healthy., Happy path: bullish event → correlate → assess risk → formulate → execute. (+7 more)

### Community 7 - "Community 7"
Cohesion: 0.12
Nodes (16): AnalysisSignal (Member 2 → Member 3), API Contract — NarrativeOS Event Schemas, code:json ({), code:json ({), code:block3 (POST /api/v1/webhooks/apify-event), code:block4 (POST <zynd-agent-url>/webhook/analyze), code:block5 (POST /api/v1/webhooks/signal), Delivery (+8 more)

### Community 8 - "Community 8"
Cohesion: 0.2
Nodes (10): build_reasoning_trace(), compute_confidence(), compute_position_size(), determine_direction(), formulate(), Agent 7: Strategy Agent — generates adaptive trading signals from validated narr, test_confidence_bounds(), test_determine_direction_bull() (+2 more)

### Community 9 - "Community 9"
Cohesion: 0.24
Nodes (11): _clean_html(), _get_author(), _get_company_name(), _has_praw_credentials(), main(), _resolve_url(), _scrape_via_playwright(), _scrape_via_praw() (+3 more)

### Community 10 - "Community 10"
Cohesion: 0.44
Nodes (10): build_event_id(), _extract_domain(), extract_entities(), extract_tickers(), normalize_article(), normalize_reddit_post(), normalize_sec_filing(), normalize_tweet() (+2 more)

### Community 11 - "Community 11"
Cohesion: 0.25
Nodes (10): get_events(), get_signals(), get_status(), _load_json(), _now(), _parse_time(), post_event(), post_signal() (+2 more)

### Community 12 - "Community 12"
Cohesion: 0.15
Nodes (5): initialEdges, initialNodes, directionColors, Signal, StatusCardProps

### Community 13 - "Community 13"
Cohesion: 0.15
Nodes (12): 1. Data & Automation Lead (Member A), 2. Agent Systems & Logic Architect (Member B), 3. Infrastructure & Platform Lead (Member C), 🤖 AI-Accelerated Development, 🏗️ Core Pillars, 👤 Member 1: The Sensory Lead, 👤 Member 2: The Cognitive Lead, 👤 Member 3: The Platform Lead (+4 more)

### Community 14 - "Community 14"
Cohesion: 0.25
Nodes (5): compute_sentiment(), enrich_event(), main(), run_pipeline(), EventBus

### Community 15 - "Community 15"
Cohesion: 0.18
Nodes (10): API Contract (Input), API Contract (Output), code:block1 (/agents/), Core Tool: Zynd AI — Full Feature Map, Deliverables, Dependencies, Domain, GitHub Copilot Usage (+2 more)

### Community 16 - "Community 16"
Cohesion: 0.22
Nodes (6): Approval, compute_slippage(), execute(), ExecuteRequest, ExecutionResult, Execution API — handles simulated trade execution for the execution canvas.

### Community 17 - "Community 17"
Cohesion: 0.2
Nodes (9): API Contract (Output), code:block1 (/data/), Core Tool: Apify — Full Feature Map, Deliverables, Dependencies, Domain, GitHub Copilot Usage, Member 1: The Sensory Lead (Apify) (+1 more)

### Community 18 - "Community 18"
Cohesion: 0.2
Nodes (9): API Contract (Consumed), code:block1 (/infra/), Core Tool: Superplane — Full Feature Map, Deliverables, Dependencies, Domain, GitHub Copilot Usage, Member 3: The Platform Lead (Superplane) (+1 more)

### Community 19 - "Community 19"
Cohesion: 0.22
Nodes (8): code:bash (# Setup), code:bash (# Install Apify CLI), code:bash (source .venv/bin/activate), Deploy to Apify Cloud, NarrativeOS Data Pipeline — Local Test Runner, Set up schedules via Apify Console, Testing the pipeline, Webhook Setup

### Community 21 - "Community 21"
Cohesion: 0.43
Nodes (5): correlate(), estimate_impact_direction(), extract_sectors(), Agent 4: Market Correlation Agent — maps narratives to assets, sectors, and macr, score_sector_relevance()

### Community 24 - "Community 24"
Cohesion: 0.29
Nodes (7): 6. Risk Intelligence Agent, Outputs, Outputs, Responsibility, Responsibility, Tasks, Tasks

### Community 25 - "Community 25"
Cohesion: 0.29
Nodes (7): 3. Sentiment Reasoning Agent, Outputs, Outputs, Responsibility, Responsibility, Tasks, Tasks

### Community 26 - "Community 26"
Cohesion: 0.29
Nodes (7): 7. Strategy Agent, Outputs, Outputs, Responsibility, Responsibility, Tasks, Tasks

### Community 27 - "Community 27"
Cohesion: 0.29
Nodes (6): Apify MCP Integration, Architecture, code:python (from data.mcp.client import NarrativeOSDataClient), code:block2 (Zynd Agent), MCP Server (AI Assistant Use), Quick Start

### Community 29 - "Community 29"
Cohesion: 0.33
Nodes (6): 4. Market Correlation Agent, Example, Responsibility, Responsibility, Tasks, Tasks

### Community 30 - "Community 30"
Cohesion: 0.33
Nodes (6): 2. Narrative Intelligence Agent, Outputs, Outputs, Responsibility, Responsibility, Tasks

### Community 33 - "Community 33"
Cohesion: 0.4
Nodes (5): Arbiter Agent, Bear Agent, Bull Agent, Components, Neutral Agent

### Community 34 - "Community 34"
Cohesion: 0.4
Nodes (5): 5. Debate Agent System, Agent Topology, Goal, Responsibility, Responsibility

### Community 35 - "Community 35"
Cohesion: 0.4
Nodes (5): 1. Data Acquisition Agent, Infrastructure, Outputs, Responsibility, Sources

### Community 36 - "Community 36"
Cohesion: 0.4
Nodes (5): 8. Visualization Agent, Features, Frontend Stack, Responsibility, Responsibility

### Community 37 - "Community 37"
Cohesion: 0.5
Nodes (3): AnalysisSignal, NarrativeEvent, PipelineStatus

## Knowledge Gaps
- **144 isolated node(s):** `narrativeos-cognitive — Zynd-registered NarrativeOS agent mesh wrapper.  Runs th`, `Pull fresh data from Apify actors via MCP client.`, `nextConfig`, `initialNodes`, `initialEdges` (+139 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `Community 9` to `Community 10`, `Community 3`, `Community 14`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Why does `run_analysis()` connect `Community 1` to `Community 4`, `Community 14`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Why does `run_analysis_pipeline()` connect `Community 4` to `Community 1`, `Community 5`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `main()` (e.g. with `EventBus` and `normalize_reddit_post()`) actually correct?**
  _`main()` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `SignalAggregator` (e.g. with `AnalysisSignal` and `DebateSummary`) actually correct?**
  _`SignalAggregator` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `NarrativeIntelligenceAgent` (e.g. with `Entity` and `NarrativeEvent`) actually correct?**
  _`NarrativeIntelligenceAgent` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `SentimentVector` (e.g. with `SentimentReasoningAgent` and `SignalAggregator`) actually correct?**
  _`SentimentVector` has 9 INFERRED edges - model-reasoned connections that need verification._