# Graph Report - NarrativeOS  (2026-05-09)

## Corpus Check
- 71 files · ~19,323 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 419 nodes · 539 edges · 52 communities (48 shown, 4 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 85 edges (avg confidence: 0.68)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `707d45e6`
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
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]

## God Nodes (most connected - your core abstractions)
1. `main()` - 15 edges
2. `SignalAggregator` - 14 edges
3. `NarrativeIntelligenceAgent` - 13 edges
4. `SentimentVector` - 11 edges
5. `DebateEngine` - 11 edges
6. `BullAgent` - 10 edges
7. `BearAgent` - 10 edges
8. `ArbiterAgent` - 10 edges
9. `NarrativeEvent` - 9 edges
10. `TopicCluster` - 9 edges

## Surprising Connections (you probably didn't know these)
- `run_analysis_pipeline()` --calls--> `run_analysis()`  [INFERRED]
  agent.py → agents/graph/workflow.py
- `sentiment_reasoning_analyze()` --calls--> `SentimentReasoningAgent`  [INFERRED]
  agents/webhooks/server.py → agents/sentiment.py
- `narrative_intelligence_analyze()` --calls--> `NarrativeIntelligenceAgent`  [INFERRED]
  agents/webhooks/server.py → agents/narrative_intelligence.py
- `sentiment_reasoning_node()` --calls--> `SentimentReasoningAgent`  [INFERRED]
  agents/graph/workflow.py → agents/sentiment.py
- `narrative_intelligence_node()` --calls--> `NarrativeIntelligenceAgent`  [INFERRED]
  agents/graph/workflow.py → agents/narrative_intelligence.py

## Communities (52 total, 4 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (25): AnalysisSignal, DebatePosition, DebateRound, DebateSummary, Direction, Entity, NarrativeEvent, NarrativeEventBatch (+17 more)

### Community 1 - "Community 1"
Cohesion: 0.04
Nodes (46): 1. Data Acquisition Agent, 2. Narrative Intelligence Agent, 3. Sentiment Reasoning Agent, 4. Market Correlation Agent, 5. Debate Agent System, 6. Risk Intelligence Agent, 8. Visualization Agent, Agent Topology (+38 more)

### Community 2 - "Community 2"
Cohesion: 0.09
Nodes (23): AgentPayload, AnalysisSignal, CorrelationResult, DebateSummary, Entity, MarketCorrelationOutput, NarrativeEvent, RiskOutput (+15 more)

### Community 3 - "Community 3"
Cohesion: 0.08
Nodes (24): Agent Communication Model, Agent Mesh Architecture, Agent Registry Layer, AI and Agent Infrastructure, Apify, Backend, code:text (Apify Actors), Core Objectives (+16 more)

### Community 4 - "Community 4"
Cohesion: 0.19
Nodes (18): NamedTuple, extract_entities(), extract_tickers(), ExtractedEntity, build_event_id(), _detect_post_type(), _extract_domain(), normalize_article() (+10 more)

### Community 5 - "Community 5"
Cohesion: 0.12
Nodes (16): AnalysisSignal (Member 2 → Member 3), API Contract — NarrativeOS Event Schemas, code:json ({), code:json ({), code:block3 (POST /api/v1/webhooks/apify-event), code:block4 (POST <zynd-agent-url>/webhook/analyze), code:block5 (POST /api/v1/webhooks/signal), Delivery (+8 more)

### Community 6 - "Community 6"
Cohesion: 0.19
Nodes (11): assess(), compute_confidence_degradation(), compute_risk_score(), detect_anomalies(), estimate_volatility(), extract_risk_factors(), Agent 6: Risk Intelligence Agent — evaluates systemic uncertainty and signal rel, str (+3 more)

### Community 7 - "Community 7"
Cohesion: 0.2
Nodes (10): build_reasoning_trace(), compute_confidence(), compute_position_size(), determine_direction(), formulate(), Agent 7: Strategy Agent — generates adaptive trading signals from validated narr, test_confidence_bounds(), test_determine_direction_bull() (+2 more)

### Community 8 - "Community 8"
Cohesion: 0.15
Nodes (8): AgentState, run_analysis(), narrativeos-cognitive — Zynd-registered NarrativeOS agent mesh wrapper.  Runs th, run_analysis_pipeline(), narrative_intelligence_analyze(), sentiment_reasoning_analyze(), strategy_generate(), webhook_analyze()

### Community 9 - "Community 9"
Cohesion: 0.15
Nodes (5): initialEdges, initialNodes, directionColors, Signal, StatusCardProps

### Community 10 - "Community 10"
Cohesion: 0.15
Nodes (12): 1. Data & Automation Lead (Member A), 2. Agent Systems & Logic Architect (Member B), 3. Infrastructure & Platform Lead (Member C), 🤖 AI-Accelerated Development, 🏗️ Core Pillars, 👤 Member 1: The Sensory Lead, 👤 Member 2: The Cognitive Lead, 👤 Member 3: The Platform Lead (+4 more)

### Community 11 - "Community 11"
Cohesion: 0.52
Nodes (9): build_event_id(), _extract_domain(), extract_entities(), extract_tickers(), normalize_article(), normalize_reddit_post(), normalize_sec_filing(), _now_iso() (+1 more)

### Community 12 - "Community 12"
Cohesion: 0.3
Nodes (9): _clean_html(), _get_author(), _get_company_name(), _has_praw_credentials(), main(), _resolve_url(), _scrape_via_playwright(), _scrape_via_praw() (+1 more)

### Community 13 - "Community 13"
Cohesion: 0.18
Nodes (10): API Contract (Input), API Contract (Output), code:block1 (/agents/), Core Tool: Zynd AI — Full Feature Map, Deliverables, Dependencies, Domain, GitHub Copilot Usage (+2 more)

### Community 14 - "Community 14"
Cohesion: 0.27
Nodes (4): enrich_event(), main(), run_pipeline(), EventBus

### Community 15 - "Community 15"
Cohesion: 0.2
Nodes (9): API Contract (Output), code:block1 (/data/), Core Tool: Apify — Full Feature Map, Deliverables, Dependencies, Domain, GitHub Copilot Usage, Member 1: The Sensory Lead (Apify) (+1 more)

### Community 16 - "Community 16"
Cohesion: 0.2
Nodes (9): API Contract (Consumed), code:block1 (/infra/), Core Tool: Superplane — Full Feature Map, Deliverables, Dependencies, Domain, GitHub Copilot Usage, Member 3: The Platform Lead (Superplane) (+1 more)

### Community 17 - "Community 17"
Cohesion: 0.22
Nodes (8): code:bash (# Setup), code:bash (# Install Apify CLI), code:bash (source .venv/bin/activate), Deploy to Apify Cloud, NarrativeOS Data Pipeline — Local Test Runner, Set up schedules via Apify Console, Testing the pipeline, Webhook Setup

### Community 21 - "Community 21"
Cohesion: 0.29
Nodes (7): 7. Strategy Agent, Outputs, Outputs, Responsibility, Responsibility, Tasks, Tasks

### Community 25 - "Community 25"
Cohesion: 0.5
Nodes (3): AnalysisSignal, NarrativeEvent, PipelineStatus

## Knowledge Gaps
- **127 isolated node(s):** `narrativeos-cognitive — Zynd-registered NarrativeOS agent mesh wrapper.  Runs th`, `nextConfig`, `initialNodes`, `initialEdges`, `Signal` (+122 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Agent Topology` connect `Community 1` to `Community 3`, `Community 21`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `Direction` connect `Community 0` to `Community 6`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `main()` (e.g. with `EventBus` and `normalize_article()`) actually correct?**
  _`main()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `SignalAggregator` (e.g. with `AnalysisSignal` and `DebateSummary`) actually correct?**
  _`SignalAggregator` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `NarrativeIntelligenceAgent` (e.g. with `Entity` and `NarrativeEvent`) actually correct?**
  _`NarrativeIntelligenceAgent` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `SentimentVector` (e.g. with `SentimentReasoningAgent` and `SignalAggregator`) actually correct?**
  _`SentimentVector` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `narrativeos-cognitive — Zynd-registered NarrativeOS agent mesh wrapper.  Runs th`, `nextConfig`, `initialNodes` to the rest of the system?**
  _127 weakly-connected nodes found - possible documentation gaps or missing edges._