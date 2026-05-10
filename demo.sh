#!/usr/bin/env bash
set -euo pipefail

# ═══════════════════════════════════════════════════════════════
# NarrativeOS — Demo Script
# Decentralized Multi-Agent Narrative Intelligence for Markets
# ═══════════════════════════════════════════════════════════════
#
# Usage:  ./demo.sh [--skip-pipeline] [--fast]
#
# Walk through the full E2E flow for hackathon submission.
# Each step pauses so you can narrate for a video recording.
# ═══════════════════════════════════════════════════════════════

STEP=0
SKIP_PIPELINE=false
FAST=false
for arg in "$@"; do
  case "$arg" in
    --skip-pipeline) SKIP_PIPELINE=true ;;
    --fast) FAST=true ;;
  esac
done

GOLD='\033[38;5;214m'
PURPLE='\033[38;5;99m'
CYAN='\033[38;5;45m'
GREEN='\033[38;5;82m'
RED='\033[38;5;196m'
BOLD='\033[1m'
NC='\033[0m'
DIM='\033[2m'

step() {
  STEP=$((STEP+1))
  echo ""
  echo -e "${PURPLE}┌─────────────────────────────────────────────────────────┐${NC}"
  printf "${PURPLE}│${NC} ${GOLD}${BOLD}Step %d:${NC} %-49s ${PURPLE}│${NC}\n" "$STEP" "$1"
  echo -e "${PURPLE}└─────────────────────────────────────────────────────────┘${NC}"
  echo ""
  if [ "$FAST" = false ]; then
    sleep 1
  fi
}

header() {
  echo ""
  echo -e "${GOLD}${BOLD}  ╔══════════════════════════════════════════════╗${NC}"
  echo -e "${GOLD}${BOLD}  ║        NarrativeOS — Live Demo               ║${NC}"
  echo -e "${GOLD}${BOLD}  ╚══════════════════════════════════════════════╝${NC}"
  echo ""
  echo -e "  ${DIM}Decentralized Multi-Agent Narrative Intelligence${NC}"
  echo -e "  ${DIM}for Financial Markets${NC}"
  echo ""
  echo -e "  ${CYAN}Bridge:${NC}  https://narrativeos-bridge.onrender.com"
  echo -e "  ${CYAN}Dashboard:${NC} https://narrative-os-theta.vercel.app"
  echo ""
}

check_ok() {
  echo -e "  ${GREEN}✓${NC} $1"
}

check_fail() {
  echo -e "  ${RED}✗${NC} $1"
}

info() {
  echo -e "  ${CYAN}→${NC} $1"
}

# ── Step 0: Prerequisites ──────────────────────────────────
header

step "Prerequisites & Environment"

# Check Python venv
if [ -f ".venv/bin/python" ]; then
  check_ok "Python venv found at .venv/bin/python"
else
  check_fail "No .venv found — run: python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
  exit 1
fi

# Source .env
if [ -f ".env" ]; then
  set -a
  source .env
  set +a
  check_ok ".env loaded"
else
  check_fail ".env not found"
fi

# Check key env vars
for var in OPENROUTER_API_KEY APIFY_API_TOKEN SUPERPLANE_BRIDGE_URL; do
  if [ -n "${!var:-}" ]; then
    check_ok "$var is set"
  else
    check_fail "$var is not set"
  fi
done

# Check bridge reachable
BRIDGE="${SUPERPLANE_BRIDGE_URL:-https://narrativeos-bridge.onrender.com}"
if curl -sf "$BRIDGE/health" > /dev/null 2>&1; then
  check_ok "Render bridge reachable at $BRIDGE"
else
  check_fail "Render bridge unreachable (may be cold-starting)"
  info "Continuing anyway — data will be pushed once bridge wakes up..."
fi

echo ""
info "Venue: Agentic Hackathon — Agent Mesh Track"
info "Tech: Apify + Zynd + Superplane → 8-agent debate pipeline"
echo ""

sleep 1

# ── Step 1: Architecture Overview ──────────────────────────
step "Agent Mesh Architecture (8 Specialized Agents)"

echo -e "  ${CYAN}┌─────────────────────────────────────────────────────┐${NC}"
echo -e "  ${CYAN}│${NC}  ${BOLD}Data Flow:${NC} Raw Data → Narrative → Signal            ${CYAN}│${NC}"
echo -e "  ${CYAN}├─────────────────────────────────────────────────────┤${NC}"
echo -e "  ${CYAN}│${NC}  1. ${PURPLE}Data Acquisition${NC}  — Apify Actors (News, SEC, RSS)   ${CYAN}│${NC}"
echo -e "  ${CYAN}│${NC}  2. ${PURPLE}Narrative Intel${NC}    — Topic clustering, momentum     ${CYAN}│${NC}"
echo -e "  ${CYAN}│${NC}  3. ${PURPLE}Sentiment Reasoning${NC} — Bullish/bearish scoring        ${CYAN}│${NC}"
echo -e "  ${CYAN}│${NC}  4. ${PURPLE}Market Correlation${NC} — Map narratives → assets        ${CYAN}│${NC}"
echo -e "  ${CYAN}│${NC}  5. ${PURPLE}Debate System${NC}      — Bull vs Bear vs Arbiter         ${CYAN}│${NC}"
echo -e "  ${CYAN}│${NC}  6. ${PURPLE}Risk Intelligence${NC}  — Anomaly detection               ${CYAN}│${NC}"
echo -e "  ${CYAN}│${NC}  7. ${PURPLE}Strategy${NC}           — BUY/SELL/HOLD with confidence   ${CYAN}│${NC}"
echo -e "  ${CYAN}│${NC}  8. ${PURPLE}Visualization${NC}      — Dashboard, flow graph           ${CYAN}│${NC}"
echo -e "  ${CYAN}└─────────────────────────────────────────────────────┘${NC}"
echo ""

if [ "$FAST" = false ]; then
  read -p "  Press Enter to continue..."
fi

# ── Step 2: GitHub & Codebase ──────────────────────────────
step "Codebase Tour"

echo -e "  ${CYAN}├── data/actors/${NC}          4 Apify Actors (news, SEC, Twitter, Reddit)"
echo -e "  ${CYAN}├── data/pipelines/${NC}       Data ingestion + enrichment + entity extraction"
echo -e "  ${CYAN}├── agents/${NC}               8 specialized AI agents"
echo -e "  ${CYAN}│   ├── graph/workflow.py${NC}  LangGraph E2E pipeline"
echo -e "  ${CYAN}│   ├── debate/engine.py${NC}   Bull/Bear/Arbiter 3-round debate"
echo -e "  ${CYAN}│   ├── llm.py${NC}             OpenRouter-powered LLM client"
echo -e "  ${CYAN}│   ├── tools/${NC}             Web search, price lookup, SEC lookup"
echo -e "  ${CYAN}│   └── backtest/${NC}          16 historical events, 62.5% accuracy"
echo -e "  ${CYAN}├── infra/superplane/${NC}      FastAPI bridge deployed to Render.com"
echo -e "  ${CYAN}├── infra/dashboard/${NC}       Next.js dashboard on Vercel"
echo -e "  ${CYAN}├── agent.py${NC}               Zynd agent wrapper (port 5005)"
echo -e "  ${CYAN}├── render.yaml${NC}            Render Blueprint deployment"
echo -e "  ${CYAN}└── .github/workflows/${NC}     CI/CD with lint + test + deploy"
echo ""

if [ "$FAST" = false ]; then
  read -p "  Press Enter to continue..."
fi

# ── Step 3: Run the Pipeline ───────────────────────────────
step "Running the E2E Agent Pipeline"

echo -e "  ${DIM}This executes the full LangGraph workflow:${NC}"
echo -e "  ${DIM}  Narrative Intelligence → Sentiment Reasoning → Debate → Signal${NC}"
echo ""

if [ "$SKIP_PIPELINE" = true ]; then
  info "Skipping pipeline (--skip-pipeline). Using existing bridge data."
else
  info "Starting pipeline with LLM-powered agents..."
  echo ""

  PIPELINE_OUTPUT=$(.venv/bin/python data/pipelines/pipeline.py 2>&1)
  echo "$PIPELINE_OUTPUT"
  echo ""

  # Extract signal info from output
  SIGNAL_TICKER=$(echo "$PIPELINE_OUTPUT" | grep "Final E2E Signal" | awk '{print $5}')
  SIGNAL_DIR=$(echo "$PIPELINE_OUTPUT" | grep "Final E2E Signal" | awk '{print $4}')
  SIGNAL_CONF=$(echo "$PIPELINE_OUTPUT" | grep "Final E2E Signal" | awk '{print $6}')
  SIGNAL_ARBITER=$(echo "$PIPELINE_OUTPUT" | grep "Arbiter:" | head -1 | sed 's/.*Arbiter: //')
  EVENT_COUNT=$(echo "$PIPELINE_OUTPUT" | grep "Pipeline complete" | grep -oP '\d+(?= events emitted)')

  if [ -n "$EVENT_COUNT" ]; then
    echo ""
    check_ok "$EVENT_COUNT events ingested and analyzed"
  fi
  if [ -n "$SIGNAL_TICKER" ]; then
    echo -e "  ${GOLD}Signal generated:${NC} $SIGNAL_DIR $SIGNAL_TICKER at $SIGNAL_CONF"
  fi
  if [ -n "$SIGNAL_ARBITER" ]; then
    echo -e "  ${GOLD}Arbiter ruling:${NC} $SIGNAL_ARBITER"
  fi
fi

echo ""

# ── Step 4: Verify Bridge Data ─────────────────────────────
step "Bridge Data Flow (Render.com)"

info "Checking bridge status..."
echo ""

BRIDGE_STATUS=$(curl -sf "$BRIDGE/api/v1/status" 2>/dev/null || echo '{"error":"unreachable"}')
EVENTS=$(echo "$BRIDGE_STATUS" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('ingress',{}).get('events24h',0))" 2>/dev/null || echo "?")
SIGNALS=$(echo "$BRIDGE_STATUS" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('analysis',{}).get('signals24h',0))" 2>/dev/null || echo "?")
ACTIVE=$(echo "$BRIDGE_STATUS" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('ingress',{}).get('active',False))" 2>/dev/null || echo "?")

echo -e "  ${CYAN}Pipeline:${NC}  $([ "$ACTIVE" = "True" ] && echo "${GREEN}Active${NC}" || echo "${RED}Inactive${NC}")"
echo -e "  ${CYAN}Events:${NC}    $EVENTS / 24h"
echo -e "  ${CYAN}Signals:${NC}   $SIGNALS / 24h"
echo ""

# Show latest signal
LATEST_SIGNAL=$(curl -sf "$BRIDGE/api/v1/datasets/executed_signals/items?limit=1" 2>/dev/null | python3 -c "
import sys, json
d = json.load(sys.stdin)
if d:
    s = d[0]
    print(f\"{s.get('direction','?')} {s.get('ticker','?')} @ {s.get('confidence',0)*100:.0f}% | {s.get('narrative_summary','')[:80]}\")
" 2>/dev/null || echo "No data yet")

if [ -n "$LATEST_SIGNAL" ]; then
  echo -e "  ${GOLD}Latest signal:${NC} $LATEST_SIGNAL"
fi
echo ""

check_ok "Bridge endpoints:"
info "  GET /api/v1/status                      → pipeline health"
info "  GET /api/v1/datasets/executed_signals/items → signals"
info "  GET /api/v1/datasets/ingress/items      → raw events"
info "  POST /api/v1/datasets/.../items         → agent push endpoint"
echo ""

# ── Step 5: Dashboard ─────────────────────────────────────
step "Live Dashboard (Vercel)"

DASHBOARD_URL="https://narrative-os-theta.vercel.app"

echo -e "  ${CYAN}Dashboard:${NC} $DASHBOARD_URL"
echo ""
echo -e "  The dashboard shows:"
echo -e "  ${GOLD}●${NC}  Hero section with Threads particle animation"
echo -e "  ${GOLD}●${NC}  Agent Mesh graph (React Flow — 8 glassmorphism nodes)"
echo -e "  ${GOLD}●${NC}  Market Coverage grid (46 tickers across 4 asset types)"
echo -e "  ${GOLD}●${NC}  Live Signals table with expandable debate details"
echo -e "  ${GOLD}●${NC}  System Status cards (Ingress / Analysis / Execution)"
echo -e "  ${GOLD}●${NC}  Sponsor section (Apify, Zynd, Superplane)"
echo -e "  ${GOLD}●${NC}  TechStackBar with 15 technology badges"
echo ""
echo -e "  ${DIM}Every 15s, the dashboard fetches /api/status and /api/signals${NC}"
echo -e "  ${DIM}(proxied through Vercel serverless functions → Render bridge).${NC}"
echo ""
info "Open in browser:"
echo -e "  open $DASHBOARD_URL"
echo ""

# ── Step 6: Architecture Summary ──────────────────────────
step "System Architecture Summary"

echo -e "  ${BOLD}Data Layer${NC}        Apify Actors → RSS feeds, SEC EDGAR, Google News"
echo -e "  ${BOLD}Cognitive Layer${NC}   LangGraph agent graph with 8 specialized agents"
echo -e "  ${BOLD}Debate Engine${NC}     Bull/Bear/Arbiter 3-round adversarial reasoning"
echo -e "  ${BOLD}LLM Backend${NC}       OpenRouter → configurable model (gpt-4o-mini)"
echo -e "  ${BOLD}Orchestration${NC}     Superplane bridge + Zynd agent registry"
echo -e "  ${BOLD}Frontend${NC}          Next.js + TailwindCSS + React Flow + Framer Motion"
echo -e "  ${BOLD}Deployment${NC}        Render.com (bridge) + Vercel (dashboard)"
echo ""

echo -e "  ${GOLD}Backtest accuracy:${NC} 62.5% overall, 83.3% on crypto/commodities"
echo -e "  ${GOLD}Entities tracked:${NC}  50+ tickers across equities/crypto/commodities/ETFs"
echo -e "  ${GOLD}Asset type enum:${NC}   equity | crypto | commodity | etf"
echo ""

# ── Done ──────────────────────────────────────────────────
step "Demo Complete"

echo -e "  ${GOLD}${BOLD}  ╔══════════════════════════════════════════════╗${NC}"
echo -e "  ${GOLD}${BOLD}  ║     NarrativeOS — Submission Ready           ║${NC}"
echo -e "  ${GOLD}${BOLD}  ╚══════════════════════════════════════════════╝${NC}"
echo ""
echo -e "  ${CYAN}Bridge API:${NC}  https://narrativeos-bridge.onrender.com/docs"
echo -e "  ${CYAN}Dashboard:${NC}  https://narrative-os-theta.vercel.app"
echo -e "  ${CYAN}GitHub:${NC}     https://github.com/0xYuvi/NarrativeOS"
echo -e "  ${CYAN}Demo script:${NC} ./demo.sh"
echo ""
echo -e "  ${DIM}Built with: Apify · Zynd · Superplane · LangGraph · OpenRouter${NC}"
echo -e "  ${DIM}Agentic Hackathon — Agent Mesh Track${NC}"
echo ""
