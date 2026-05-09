# Graph Report - NarrativeOS  (2026-05-09)

## Corpus Check
- 49 files · ~14,790 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 323 nodes · 346 edges · 40 communities (36 shown, 4 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 22 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `57f00998`
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
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]

## God Nodes (most connected - your core abstractions)
1. `main()` - 15 edges
2. `normalize_reddit_post()` - 9 edges
3. `normalize_article()` - 9 edges
4. `Agent Topology` - 9 edges
5. `Member 2: The Cognitive Lead (Zynd)` - 9 edges
6. `Member 1: The Sensory Lead (Apify)` - 8 edges
7. `Member 3: The Platform Lead (Superplane)` - 8 edges
8. `3. Sentiment Reasoning Agent` - 7 edges
9. `6. Risk Intelligence Agent` - 7 edges
10. `7. Strategy Agent` - 7 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `normalize_article()`  [INFERRED]
  data/actors/sec-scraper/src/main.py → data/pipelines/normalize.py
- `main()` --calls--> `normalize_reddit_post()`  [INFERRED]
  data/actors/sec-scraper/src/main.py → data/pipelines/normalize.py
- `main()` --calls--> `normalize_sec_filing()`  [INFERRED]
  data/actors/sec-scraper/src/main.py → data/pipelines/normalize.py
- `test_ticker_extraction()` --calls--> `extract_tickers()`  [INFERRED]
  data/pipelines/test_pipeline.py → data/pipelines/entity_extractor.py
- `test_entity_extraction()` --calls--> `extract_entities()`  [INFERRED]
  data/pipelines/test_pipeline.py → data/pipelines/entity_extractor.py

## Communities (40 total, 4 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (40): 1. Data Acquisition Agent, 2. Narrative Intelligence Agent, 5. Debate Agent System, 6. Risk Intelligence Agent, 7. Strategy Agent, 8. Visualization Agent, Agent Topology, Arbiter Agent (+32 more)

### Community 1 - "Community 1"
Cohesion: 0.11
Nodes (20): AnalysisSignal, CorrelationResult, DebateSummary, Entity, MarketCorrelationOutput, NarrativeEvent, RiskOutput, StrategyOutput (+12 more)

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (24): Agent Communication Model, Agent Mesh Architecture, Agent Registry Layer, AI and Agent Infrastructure, Apify, Backend, code:text (Apify Actors), Core Objectives (+16 more)

### Community 3 - "Community 3"
Cohesion: 0.19
Nodes (18): NamedTuple, extract_entities(), extract_tickers(), ExtractedEntity, build_event_id(), _detect_post_type(), _extract_domain(), normalize_article() (+10 more)

### Community 4 - "Community 4"
Cohesion: 0.17
Nodes (10): _clean_html(), _get_author(), _get_company_name(), _has_praw_credentials(), main(), _resolve_url(), _scrape_via_playwright(), _scrape_via_praw() (+2 more)

### Community 5 - "Community 5"
Cohesion: 0.12
Nodes (16): AnalysisSignal (Member 2 → Member 3), API Contract — NarrativeOS Event Schemas, code:json ({), code:json ({), code:block3 (POST /api/v1/webhooks/apify-event), code:block4 (POST <zynd-agent-url>/webhook/analyze), code:block5 (POST /api/v1/webhooks/signal), Delivery (+8 more)

### Community 6 - "Community 6"
Cohesion: 0.2
Nodes (10): assess(), compute_confidence_degradation(), compute_risk_score(), detect_anomalies(), estimate_volatility(), extract_risk_factors(), Agent 6: Risk Intelligence Agent — evaluates systemic uncertainty and signal rel, test_anomaly_detection() (+2 more)

### Community 7 - "Community 7"
Cohesion: 0.2
Nodes (10): build_reasoning_trace(), compute_confidence(), compute_position_size(), determine_direction(), formulate(), Agent 7: Strategy Agent — generates adaptive trading signals from validated narr, test_confidence_bounds(), test_determine_direction_bull() (+2 more)

### Community 8 - "Community 8"
Cohesion: 0.15
Nodes (5): initialEdges, initialNodes, directionColors, Signal, StatusCardProps

### Community 9 - "Community 9"
Cohesion: 0.15
Nodes (12): 1. Data & Automation Lead (Member A), 2. Agent Systems & Logic Architect (Member B), 3. Infrastructure & Platform Lead (Member C), 🤖 AI-Accelerated Development, 🏗️ Core Pillars, 👤 Member 1: The Sensory Lead, 👤 Member 2: The Cognitive Lead, 👤 Member 3: The Platform Lead (+4 more)

### Community 10 - "Community 10"
Cohesion: 0.18
Nodes (10): API Contract (Input), API Contract (Output), code:block1 (/agents/), Core Tool: Zynd AI — Full Feature Map, Deliverables, Dependencies, Domain, GitHub Copilot Usage (+2 more)

### Community 11 - "Community 11"
Cohesion: 0.2
Nodes (9): API Contract (Output), code:block1 (/data/), Core Tool: Apify — Full Feature Map, Deliverables, Dependencies, Domain, GitHub Copilot Usage, Member 1: The Sensory Lead (Apify) (+1 more)

### Community 12 - "Community 12"
Cohesion: 0.2
Nodes (9): API Contract (Consumed), code:block1 (/infra/), Core Tool: Superplane — Full Feature Map, Deliverables, Dependencies, Domain, GitHub Copilot Usage, Member 3: The Platform Lead (Superplane) (+1 more)

### Community 13 - "Community 13"
Cohesion: 0.22
Nodes (8): code:bash (# Setup), code:bash (# Install Apify CLI), code:bash (source .venv/bin/activate), Deploy to Apify Cloud, NarrativeOS Data Pipeline — Local Test Runner, Set up schedules via Apify Console, Testing the pipeline, Webhook Setup

### Community 17 - "Community 17"
Cohesion: 0.29
Nodes (7): 3. Sentiment Reasoning Agent, Outputs, Outputs, Responsibility, Responsibility, Tasks, Tasks

### Community 19 - "Community 19"
Cohesion: 0.33
Nodes (6): 4. Market Correlation Agent, Example, Responsibility, Responsibility, Tasks, Tasks

### Community 22 - "Community 22"
Cohesion: 0.5
Nodes (3): AnalysisSignal, NarrativeEvent, PipelineStatus

## Knowledge Gaps
- **126 isolated node(s):** `Execution API — handles simulated trade execution for the execution canvas.`, `Agent 4: Market Correlation Agent — maps narratives to assets, sectors, and macr`, `Agent 6: Risk Intelligence Agent — evaluates systemic uncertainty and signal rel`, `Agent 7: Strategy Agent — generates adaptive trading signals from validated narr`, `Agent 8: Visualization Agent — backend data aggregation for the real-time dashbo` (+121 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Agent Topology` connect `Community 0` to `Community 17`, `Community 2`, `Community 19`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Why does `main()` connect `Community 4` to `Community 3`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `main()` (e.g. with `EventBus` and `normalize_article()`) actually correct?**
  _`main()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `normalize_reddit_post()` (e.g. with `main()` and `extract_tickers()`) actually correct?**
  _`normalize_reddit_post()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `normalize_article()` (e.g. with `main()` and `extract_tickers()`) actually correct?**
  _`normalize_article()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Execution API — handles simulated trade execution for the execution canvas.`, `Agent 4: Market Correlation Agent — maps narratives to assets, sectors, and macr`, `Agent 6: Risk Intelligence Agent — evaluates systemic uncertainty and signal rel` to the rest of the system?**
  _126 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.05 - nodes in this community are weakly interconnected._