"""Agent 8: Visualization Agent — backend data aggregation for the real-time dashboard."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Visualization Agent", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

PIPELINE_STAGES = ["ingress", "analysis", "execution"]

MOCK_PIPELINE_STATUS = {
    "ingress": {"active": True, "lastRun": "2026-05-09T22:00:00Z", "events24h": 142},
    "analysis": {"active": True, "lastRun": "2026-05-09T21:58:00Z", "signals24h": 18},
    "execution": {"active": True, "lastRun": "2026-05-09T21:55:00Z", "executed24h": 7},
}

MOCK_EVENTS = [
    {
        "id": "evt_20260509_r_001", "source": "reddit", "title": "NVDA earnings beat expectations by 15%",
        "ticker_mentions": ["NVDA", "AMD"], "published_at": "2026-05-09T14:30:00Z",
    },
    {
        "id": "evt_20260509_n_002", "source": "news", "title": "Fed signals rate hold amid sticky inflation",
        "ticker_mentions": ["SPY", "QQQ"], "published_at": "2026-05-09T15:00:00Z",
    },
    {
        "id": "evt_20260509_s_003", "source": "sec_filing", "title": "TSLA files updated production timeline",
        "ticker_mentions": ["TSLA"], "published_at": "2026-05-09T16:00:00Z",
    },
]

MOCK_SIGNALS = [
    {
        "signal_id": "sig_20260509_nvda_001", "ticker": "NVDA", "direction": "BUY",
        "confidence": 0.78, "risk_score": 0.35, "generated_at": "2026-05-09T15:00:00Z",
    },
    {
        "signal_id": "sig_20260509_amd_002", "ticker": "AMD", "direction": "HOLD",
        "confidence": 0.50, "risk_score": 0.55, "generated_at": "2026-05-09T15:05:00Z",
    },
    {
        "signal_id": "sig_20260509_tsla_003", "ticker": "TSLA", "direction": "WATCHLIST",
        "confidence": 0.35, "risk_score": 0.70, "generated_at": "2026-05-09T16:10:00Z",
    },
]

agent_traces = {
    "narrative": "AI-driven semiconductor demand continues to accelerate as hyperscalers increase CapEx",
    "sentiment": {"polarity": 0.65, "intensity": 0.4, "confidence": 0.8},
    "debate": {
        "bull": "Growth fundamentals intact, Blackwell ramp driving record revenues",
        "bear": "Valuation stretched, competition from custom ASICs increasing",
        "arbiter": "Bull case prevails — growth trajectory supports continued upside",
    },
    "risk": {"score": 0.35, "factors": ["Valuation compression", "Geopolitical export risk"]},
    "strategy": {"direction": "BUY", "confidence": 0.78, "allocation_pct": 12.5},
}


@app.get("/health")
def health():
    return {"status": "ok", "agent": "visualization", "version": "0.1.0"}


@app.get("/api/v1/status")
def pipeline_status():
    return MOCK_PIPELINE_STATUS


@app.get("/api/v1/datasets/narrative_events/items")
def events(limit: int = 20, sort: str = "desc"):
    items = sorted(MOCK_EVENTS, key=lambda e: e["published_at"], reverse=(sort == "desc"))
    return items[:limit]


@app.get("/api/v1/datasets/analysis_signals/items")
def analysis_signals(limit: int = 20, sort: str = "desc"):
    items = sorted(MOCK_SIGNALS, key=lambda s: s["generated_at"], reverse=(sort == "desc"))
    return items[:limit]


@app.get("/api/v1/datasets/executed_signals/items")
def executed_signals(limit: int = 20, sort: str = "desc"):
    items = sorted(MOCK_SIGNALS, key=lambda s: s["generated_at"], reverse=(sort == "desc"))
    return items[:limit]


@app.get("/api/v1/traces")
def agent_trace():
    return agent_traces
