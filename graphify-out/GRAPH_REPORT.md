# Graph Report - NarrativeOS  (2026-05-09)

## Corpus Check
- 21 files · ~7,954 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 209 nodes · 254 edges · 19 communities (18 shown, 1 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 14 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b8964242`
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

## God Nodes (most connected - your core abstractions)
1. `main()` - 15 edges
2. `normalize_reddit_post()` - 9 edges
3. `normalize_article()` - 9 edges
4. `Member 2: The Cognitive Lead (Zynd)` - 9 edges
5. `Agent Topology` - 9 edges
6. `Member 1: The Sensory Lead (Apify)` - 8 edges
7. `Member 3: The Platform Lead (Superplane)` - 8 edges
8. `EventBus` - 7 edges
9. `_to_iso()` - 7 edges
10. `_now_iso()` - 7 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `EventBus`  [INFERRED]
  data/actors/sec-scraper/src/main.py → data/stream/event_bus.py
- `test_reddit_normalization()` --calls--> `normalize_reddit_post()`  [INFERRED]
  data/pipelines/test_pipeline.py → data/pipelines/normalize.py
- `main()` --calls--> `normalize_reddit_post()`  [INFERRED]
  data/actors/sec-scraper/src/main.py → data/pipelines/normalize.py
- `test_article_normalization()` --calls--> `normalize_article()`  [INFERRED]
  data/pipelines/test_pipeline.py → data/pipelines/normalize.py
- `main()` --calls--> `normalize_article()`  [INFERRED]
  data/actors/sec-scraper/src/main.py → data/pipelines/normalize.py

## Communities (19 total, 1 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.07
Nodes (29): 1. Data Acquisition Agent, 3. Sentiment Reasoning Agent, 5. Debate Agent System, 6. Risk Intelligence Agent, Agent Topology, Arbiter Agent, Bear Agent, Bull Agent (+21 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (24): Agent Communication Model, Agent Mesh Architecture, Agent Registry Layer, AI and Agent Infrastructure, Apify, Backend, code:text (Apify Actors), Core Objectives (+16 more)

### Community 2 - "Community 2"
Cohesion: 0.19
Nodes (18): NamedTuple, extract_entities(), extract_tickers(), ExtractedEntity, build_event_id(), _detect_post_type(), _extract_domain(), normalize_article() (+10 more)

### Community 3 - "Community 3"
Cohesion: 0.12
Nodes (16): AnalysisSignal (Member 2 → Member 3), API Contract — NarrativeOS Event Schemas, code:json ({), code:json ({), code:block3 (POST /api/v1/webhooks/apify-event), code:block4 (POST <zynd-agent-url>/webhook/analyze), code:block5 (POST /api/v1/webhooks/signal), Delivery (+8 more)

### Community 4 - "Community 4"
Cohesion: 0.15
Nodes (12): 1. Data & Automation Lead (Member A), 2. Agent Systems & Logic Architect (Member B), 3. Infrastructure & Platform Lead (Member C), 🤖 AI-Accelerated Development, 🏗️ Core Pillars, 👤 Member 1: The Sensory Lead, 👤 Member 2: The Cognitive Lead, 👤 Member 3: The Platform Lead (+4 more)

### Community 5 - "Community 5"
Cohesion: 0.52
Nodes (9): build_event_id(), _extract_domain(), extract_entities(), extract_tickers(), normalize_article(), normalize_reddit_post(), normalize_sec_filing(), _now_iso() (+1 more)

### Community 6 - "Community 6"
Cohesion: 0.3
Nodes (9): _clean_html(), _get_author(), _get_company_name(), _has_praw_credentials(), main(), _resolve_url(), _scrape_via_playwright(), _scrape_via_praw() (+1 more)

### Community 7 - "Community 7"
Cohesion: 0.18
Nodes (10): API Contract (Input), API Contract (Output), code:block1 (/agents/), Core Tool: Zynd AI — Full Feature Map, Deliverables, Dependencies, Domain, GitHub Copilot Usage (+2 more)

### Community 8 - "Community 8"
Cohesion: 0.27
Nodes (4): enrich_event(), main(), run_pipeline(), EventBus

### Community 9 - "Community 9"
Cohesion: 0.2
Nodes (9): API Contract (Output), code:block1 (/data/), Core Tool: Apify — Full Feature Map, Deliverables, Dependencies, Domain, GitHub Copilot Usage, Member 1: The Sensory Lead (Apify) (+1 more)

### Community 10 - "Community 10"
Cohesion: 0.2
Nodes (9): API Contract (Consumed), code:block1 (/infra/), Core Tool: Superplane — Full Feature Map, Deliverables, Dependencies, Domain, GitHub Copilot Usage, Member 3: The Platform Lead (Superplane) (+1 more)

### Community 11 - "Community 11"
Cohesion: 0.22
Nodes (8): code:bash (# Setup), code:bash (# Install Apify CLI), code:bash (source .venv/bin/activate), Deploy to Apify Cloud, NarrativeOS Data Pipeline — Local Test Runner, Set up schedules via Apify Console, Testing the pipeline, Webhook Setup

### Community 12 - "Community 12"
Cohesion: 0.29
Nodes (7): 7. Strategy Agent, Outputs, Outputs, Responsibility, Responsibility, Tasks, Tasks

### Community 13 - "Community 13"
Cohesion: 0.33
Nodes (6): 2. Narrative Intelligence Agent, Outputs, Outputs, Responsibility, Responsibility, Tasks

### Community 14 - "Community 14"
Cohesion: 0.33
Nodes (6): 4. Market Correlation Agent, Example, Responsibility, Responsibility, Tasks, Tasks

### Community 15 - "Community 15"
Cohesion: 0.4
Nodes (5): 8. Visualization Agent, Features, Frontend Stack, Responsibility, Responsibility

## Knowledge Gaps
- **110 isolated node(s):** `Quick test for the data pipeline — entity extraction + normalization. Run: pytho`, `code:block1 (/agents/)`, `Core Tool: Zynd AI — Full Feature Map`, `Sprint 1 Tasks`, `Deliverables` (+105 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Agent Topology` connect `Community 0` to `Community 1`, `Community 12`, `Community 13`, `Community 14`, `Community 15`?**
  _High betweenness centrality (0.117) - this node is a cross-community bridge._
- **Why does `main()` connect `Community 6` to `Community 8`, `Community 2`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `main()` (e.g. with `EventBus` and `normalize_reddit_post()`) actually correct?**
  _`main()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `normalize_reddit_post()` (e.g. with `extract_tickers()` and `extract_entities()`) actually correct?**
  _`normalize_reddit_post()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `normalize_article()` (e.g. with `extract_tickers()` and `extract_entities()`) actually correct?**
  _`normalize_article()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Quick test for the data pipeline — entity extraction + normalization. Run: pytho`, `code:block1 (/agents/)`, `Core Tool: Zynd AI — Full Feature Map` to the rest of the system?**
  _110 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.07 - nodes in this community are weakly interconnected._