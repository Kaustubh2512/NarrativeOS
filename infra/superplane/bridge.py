"""Superplane runtime bridge — lightweight API server for dashboard + agent integration.

Runs alongside the Zynd agent, exposing the same endpoints the dashboard expects
from Superplane. The agent pipeline POSTs signals here; the dashboard proxies reads.

To run:  python infra/superplane/bridge.py
Uses port 8765 by default.
"""

from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse

app = FastAPI(title="NarrativeOS Superplane Bridge", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(exist_ok=True)
SIGNALS_FILE = DATA_DIR / "executed_signals.json"
EVENTS_FILE = DATA_DIR / "ingress_events.json"
CANVASES_DIR = Path(__file__).resolve().parent / "canvases"

def _load_json(path: Path) -> list[dict]:
    if path.exists():
        return json.loads(path.read_text())
    return []

def _save_json(path: Path, data: list[dict]) -> None:
    path.write_text(json.dumps(data, indent=2, default=str))

def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@app.get("/health")
async def health():
    return {"status": "ok", "service": "superplane-bridge", "version": "0.1.0"}


@app.get("/api/v1/status")
async def get_status():
    signals = _load_json(SIGNALS_FILE)
    events = _load_json(EVENTS_FILE)
    now = time.time()

    recent_events = [e for e in events if now - _parse_time(e.get("collected_at", "")) < 86400]
    recent_signals = [s for s in signals if now - _parse_time(s.get("created_at", "")) < 86400]

    return {
        "ingress": {
            "active": len(recent_events) > 0,
            "lastRun": events[-1].get("collected_at", "--") if events else "--",
            "events24h": len(recent_events),
            "canvasFile": "01-ingress.yaml",
            "canvasTitle": "NarrativeOS — Data Ingress Pipeline",
        },
        "analysis": {
            "active": len(recent_signals) > 0,
            "lastRun": signals[-1].get("created_at", "--") if signals else "--",
            "signals24h": len(recent_signals),
            "canvasFile": "02-analysis.yaml",
            "canvasTitle": "NarrativeOS — Agent Analysis Pipeline",
        },
        "execution": {
            "active": len(recent_signals) > 0,
            "lastRun": signals[-1].get("created_at", "--") if signals else "--",
            "executed24h": len(recent_signals),
            "canvasFile": "03-execution.yaml",
            "canvasTitle": "NarrativeOS — Signal Execution Pipeline",
        },
    }


@app.get("/api/v1/datasets/executed_signals/items")
async def get_signals(limit: int = 20):
    signals = _load_json(SIGNALS_FILE)
    sorted_signals = sorted(signals, key=lambda x: x.get("created_at", ""), reverse=True)
    return sorted_signals[:limit]


@app.post("/api/v1/datasets/executed_signals/items")
async def post_signal(request: Request):
    body = await request.json()
    signals = _load_json(SIGNALS_FILE)
    body.setdefault("created_at", _now())
    signals.append(body)
    _save_json(SIGNALS_FILE, signals)
    return {"status": "ok", "id": body.get("signal_id", f"sig_{len(signals)}")}


@app.get("/api/v1/datasets/ingress/items")
async def get_events(limit: int = 20):
    events = _load_json(EVENTS_FILE)
    sorted_events = sorted(events, key=lambda x: x.get("collected_at", ""), reverse=True)
    return sorted_events[:limit]


@app.post("/api/v1/datasets/ingress/items")
async def post_event(request: Request):
    body = await request.json()
    events = _load_json(EVENTS_FILE)
    body.setdefault("collected_at", _now())
    events.append(body)
    _save_json(EVENTS_FILE, events)
    return {"status": "ok", "id": body.get("id", f"evt_{len(events)}")}


@app.get("/api/v1/canvases")
async def list_canvases():
    canvases = []
    if CANVASES_DIR.exists():
        for f in sorted(CANVASES_DIR.glob("*.yaml")):
            text = f.read_text()
            title = ""
            for line in text.splitlines():
                if line.strip().startswith("title:"):
                    title = line.split(":", 1)[1].strip().strip('"')
                    break
            canvases.append({
                "filename": f.name,
                "title": title,
                "lines": len(text.splitlines()),
            })
    return canvases


@app.get("/api/v1/canvases/{filename}")
async def get_canvas(filename: str):
    if not filename.endswith(".yaml"):
        return PlainTextResponse("Not found", status_code=404)
    filepath = CANVASES_DIR / filename
    if not filepath.exists() or not filepath.is_relative_to(CANVASES_DIR):
        return PlainTextResponse("Not found", status_code=404)
    return PlainTextResponse(filepath.read_text(), media_type="text/yaml")


def _parse_time(ts: str) -> float:
    try:
        return datetime.fromisoformat(ts).timestamp()
    except (ValueError, TypeError):
        return 0


if __name__ == "__main__":
    port = int(os.environ.get("SUPERPLANE_BRIDGE_PORT", 8765))
    print(f"Superplane bridge starting on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
