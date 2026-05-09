## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- ALWAYS read graphify-out/GRAPH_REPORT.md before reading any source files, running grep/glob searches, or answering codebase questions. The graph is your primary map of the codebase.
- IF graphify-out/wiki/index.md EXISTS, navigate it instead of reading raw files
- For cross-module "how does X relate to Y" questions, prefer `graphify query "<question>"`, `graphify path "<A>" "<B>"`, or `graphify explain "<concept>"` over grep — these traverse the graph's EXTRACTED + INFERRED edges instead of scanning files
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).

## Team Roles & Tool Core

This project is divided among three members, each owning a core technology:

1. **Member 1: The Sensory Lead (Apify)**
   - **Agents:** Agent 1 (Data Acquisition)
   - **Domain:** `/data` - Web scraping, data extraction, and input grounding.

2. **Member 2: The Cognitive Lead (Zynd)**
   - **Agents:** Agent 2 (Narrative), Agent 3 (Sentiment), Agent 5 (Debate)
   - **Domain:** `/agents` - Multi-agent collaboration, Zynd protocol, and narrative logic.

3. **Member 3: The Platform Lead (Superplane)**
   - **Agents:** Agent 4 (Market Correlation), Agent 6 (Risk), Agent 7 (Strategy), Agent 8 (Visualization)
   - **Domain:** `/infra` - DevOps control plane, CI/CD, and system observability.

**Shared Accelerator:** [GitHub Copilot](https://github.com/features/copilot) is used by all members for development velocity and repo-wide context.

---



# AGENTS.md

# NarrativeOS

Decentralized Multi-Agent Narrative Intelligence Network for Financial Markets

---

# Overview

NarrativeOS is an autonomous multi-agent financial intelligence system designed to analyze how narratives propagate across the internet and predict their potential financial impact before markets fully react.

The platform combines:

* TradingAgents-inspired collaborative financial reasoning
* Zynd AI decentralized agent infrastructure
* Apify-powered autonomous internet intelligence
* Superplane event-driven workflow orchestration
* GitHub Copilot accelerated development workflows

NarrativeOS continuously monitors:

* news platforms,
* Reddit,
* social media,
* SEC filings,
* macroeconomic events,
* financial reports,
* and internet-scale sentiment propagation in real time.

Unlike traditional sentiment analysis systems that classify text as simply positive or negative, NarrativeOS models:

* narrative propagation,
* emotional momentum,
* information acceleration,
* market psychology,
* cross-platform sentiment evolution,
* and event-driven market cognition.

The system operates as a decentralized collaborative agent mesh where specialized AI agents independently analyze, debate, validate, and refine financial interpretations before generating confidence-weighted trading signals.

---

# Core Objectives

NarrativeOS is designed to:

* Detect emerging financial narratives early
* Monitor internet-scale sentiment propagation
* Correlate narratives with assets and sectors
* Simulate adaptive trading strategies
* Visualize market psychology in real time
* Enable collaborative autonomous financial reasoning
* Generate explainable AI trading signals
* Build a distributed narrative cognition engine for markets

---

# High-Level System Architecture

```text
Apify Actors
        ↓
Narrative Event Stream
        ↓
Zynd Agent Mesh
        ↓
Collaborative Financial Reasoning
        ↓
Superplane Workflow Orchestration
        ↓
Trading Signal Generation
        ↓
Visualization + Execution
```

---

# Sponsor Technology Integration

## Zynd AI
https://docs.zynd.ai/
Zynd AI powers:

* decentralized agent registration,
* agent identity,
* agent discovery,
* collaborative reasoning workflows,
* inter-agent communication,
* and distributed orchestration across the NarrativeOS network.

Each NarrativeOS agent functions as an independently discoverable and callable intelligent service within the Zynd agent ecosystem.

Zynd AI enables:

* modular agent scaling,
* dynamic workflow composition,
* decentralized execution,
* and collaborative autonomous financial reasoning.

---

## Apify
https://docs.apify.com/

Apify functions as the internet sensory layer of NarrativeOS.

Apify Actors continuously ingest structured web intelligence from:

* news platforms,
* financial websites,
* Reddit,
* social media,
* RSS feeds,
* and public financial data sources.

Apify enables:

* autonomous data acquisition,
* live internet monitoring,
* structured event extraction,
* and real-time narrative ingestion pipelines.

Apify MCP-compatible Actors allow NarrativeOS agents to dynamically access external web intelligence tools and structured datasets.

---

## Superplane
 https://docs.superplane.com/ 

Superplane orchestrates long-running event-driven workflows across distributed NarrativeOS agents.

Superplane manages:

* workflow execution,
* state transitions,
* execution tracing,
* asynchronous task coordination,
* workflow observability,
* and agent runtime management.

Superplane enables scalable multi-agent execution for continuously evolving financial intelligence workflows.

---

## GitHub Copilot

GitHub Copilot accelerates:

* rapid prototyping,
* workflow implementation,
* debugging,
* infrastructure integration,
* and autonomous agent development during hackathon execution.

---

# Agent Mesh Architecture

NarrativeOS operates as a distributed network of specialized financial reasoning agents.

Each agent:

* performs a focused responsibility,
* maintains contextual memory,
* exchanges structured reasoning outputs,
* validates upstream analysis,
* and contributes to collaborative market interpretation.

Final trading signals emerge through:

* multi-agent reasoning,
* adversarial debate,
* risk-adjusted consensus,
* and confidence-weighted validation.

---

# Agent Registry Layer

All NarrativeOS agents are registered as discoverable intelligent services through the Zynd decentralized registry layer.

Each registered agent contains:

* agent identity,
* callable endpoints,
* workflow metadata,
* reasoning capabilities,
* and communication interfaces.

Agents can dynamically discover and collaborate with other agents during workflow execution.

---

# Agent Topology

## 1. Data Acquisition Agent

### Responsibility

Continuously collect and normalize internet-scale financial intelligence.

### Sources

* News websites
* Reddit
* Social media
* SEC filings
* Financial blogs
* RSS feeds
* Public APIs

### Infrastructure

* Apify Actors
* Playwright
* Reddit API
* NewsAPI

### Outputs

Structured event objects:

* title
* source
* entities
* timestamps
* links
* metadata
* narrative indicators

---

## 2. Narrative Intelligence Agent

### Responsibility

Detect emerging narratives and thematic market shifts.

### Tasks

* topic clustering
* narrative segmentation
* entity extraction
* trend acceleration analysis
* information velocity tracking
* macro narrative identification

### Outputs

Narrative intelligence objects with:

* momentum score
* propagation rate
* thematic category
* narrative confidence
* acceleration metrics

---

## 3. Sentiment Reasoning Agent

### Responsibility

Analyze emotional direction and crowd psychology.

### Tasks

* bullish/bearish scoring
* emotional intensity estimation
* uncertainty analysis
* crowd sentiment tracking
* volatility estimation

### Outputs

Sentiment vectors:

* polarity
* confidence
* emotional intensity
* instability score

---

## 4. Market Correlation Agent

### Responsibility

Map narratives to assets, sectors, and macroeconomic relationships.

### Tasks

* sector correlation
* asset association
* historical similarity analysis
* dependency mapping
* cross-market impact estimation

### Example

Narrative:
"Semiconductor supply chain disruption"

Potential impact:

* NVIDIA
* AMD
* TSMC
* logistics sector
* commodities

---

## 5. Debate Agent System

### Responsibility

Perform adversarial collaborative reasoning.

### Components

#### Bull Agent

Argues optimistic market interpretation.

#### Bear Agent

Argues pessimistic market interpretation.

#### Neutral Agent

Evaluates ambiguity and uncertainty.

#### Arbiter Agent

Combines reasoning into final weighted consensus.

### Goal

Improve robustness of autonomous financial reasoning.

---

## 6. Risk Intelligence Agent

### Responsibility

Evaluate systemic uncertainty and signal reliability.

### Tasks

* anomaly detection
* misinformation analysis
* confidence degradation
* narrative instability estimation
* volatility forecasting

### Outputs

Risk-adjusted confidence metrics.

---

## 7. Strategy Agent

### Responsibility

Generate adaptive trading strategies from validated narratives.

### Tasks

* signal generation
* simulated trade execution
* portfolio allocation
* confidence-weighted ranking
* position sizing

### Outputs

* BUY
* SELL
* HOLD
* WATCHLIST

with:

* reasoning trace,
* supporting narratives,
* confidence score,
* and risk evaluation.

---

## 8. Visualization Agent

### Responsibility

Transform collaborative agent reasoning into real-time visual intelligence.

### Features

* narrative propagation graph
* sentiment heatmaps
* agent interaction visualization
* confidence flow mapping
* trend acceleration indicators
* market psychology dashboard
* live narrative intelligence stream

### Frontend Stack

* Next.js
* React Flow
* D3.js
* TailwindCSS

---

# Agent Communication Model

Agents communicate through structured event-driven pipelines.

Each event contains:

* source metadata
* timestamps
* narrative identifiers
* extracted entities
* sentiment vectors
* confidence metrics
* reasoning outputs

Agents can:

* validate upstream outputs,
* challenge conflicting interpretations,
* enrich incomplete analysis,
* and escalate uncertain market events.

---

# Workflow Orchestration

NarrativeOS uses:

* Zynd AI agent coordination
* Superplane event orchestration
* asynchronous distributed workflows
* persistent agent memory
* collaborative reasoning pipelines

The orchestration layer handles:

* task routing,
* workflow execution,
* dependency management,
* agent communication,
* execution tracing,
* and consensus aggregation.

---

# TradingAgents Integration

NarrativeOS extends the TradingAgents architecture with:

* real-time narrative intelligence,
* internet-scale event monitoring,
* autonomous web cognition,
* narrative propagation analysis,
* collaborative sentiment reasoning,
* and event-driven market interpretation.

TradingAgents-inspired collaborative financial reasoning forms the core decision-making layer of the system.

NarrativeOS adds:

* distributed narrative cognition,
* autonomous internet monitoring,
* and real-time market psychology visualization.

---

# Tech Stack

## Backend

* Python
* FastAPI
* PostgreSQL

## AI and Agent Infrastructure

* Zynd AI SDK
* LangGraph
* OpenAI API

## Workflow Infrastructure

* Superplane

## Internet Intelligence Layer

* Apify Actors
* Playwright
* Reddit API
* NewsAPI
* Polygon.io

## Frontend

* Next.js
* TypeScript
* TailwindCSS
* React Flow
* D3.js

---

# Long-Term Vision

NarrativeOS aims to evolve into a decentralized narrative cognition engine for autonomous financial intelligence.

Future capabilities may include:

* geopolitical event forecasting,
* macroeconomic narrative monitoring,
* coordinated misinformation detection,
* autonomous hedge-fund-style reasoning,
* and internet-scale market psychology analysis.

The long-term objective is to build infrastructure for narrative-aware autonomous financial systems capable of interpreting global information flow in real time.

