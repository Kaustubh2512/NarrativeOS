"""Backtest pipeline accuracy against curated historical events.

Usage:
    from agents.backtest.runner import run_backtest
    results = run_backtest()
    print(results.summary())
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from typing import Any

from agents.backtest.events import HISTORICAL_EVENTS
from agents.graph.workflow import run_analysis
from agents.models import NarrativeEvent


def _make_event(ev: dict) -> NarrativeEvent:
    return NarrativeEvent(
        id=f"btev_{ev['ticker'].lower()}_{ev['date'].replace('-','')}",
        source="news",
        source_actor="backtest",
        title=ev["title"],
        body=ev["body"],
        url="",
        author="Backtest Engine",
        published_at=ev["date"],
        collected_at=datetime.now(timezone.utc).isoformat(),
        ticker_mentions=[ev["ticker"]],
        entities=[{"name": ev["ticker"], "type": "company", "ticker": ev["ticker"]}],
        sentiment_score=None,
        metadata={"event_date": ev["date"]},
    )


def _classify_direction(signal_direction: str, change_pct: float) -> str:
    if signal_direction in ("BUY",):
        if change_pct > 2:
            return "CORRECT_BULLISH"
        elif change_pct < -2:
            return "WRONG_BEARISH"
        else:
            return "NEUTRAL_MISMATCH"
    elif signal_direction in ("SELL",):
        if change_pct < -2:
            return "CORRECT_BEARISH"
        elif change_pct > 2:
            return "WRONG_BULLISH"
        else:
            return "NEUTRAL_MISMATCH"
    else:
        if abs(change_pct) <= 2:
            return "CORRECT_NEUTRAL"
        elif change_pct > 2:
            return "MISSED_BULLISH"
        else:
            return "MISSED_BEARISH"


def _buy_sell(actual: str) -> str:
    return "BUY" if actual == "BULLISH" else "SELL" if actual == "BEARISH" else "HOLD"


def run_backtest(events: list[dict] | None = None) -> BacktestResult:
    events = events or HISTORICAL_EVENTS
    results = []
    correct = 0

    for ev in events:
        narrative_event = _make_event(ev)
        signal = run_analysis([narrative_event], ev["ticker"])

        signal_dir = signal.direction
        actual_dir = ev["actual_direction"]
        change_pct = ev["actual_change_pct"]
        classification = _classify_direction(signal_dir, change_pct)

        if signal_dir == _buy_sell(actual_dir):
            correct += 1

        results.append({
            "ticker": ev["ticker"],
            "date": ev["date"],
            "signal_direction": signal_dir,
            "signal_confidence": round(signal.confidence, 4),
            "actual_direction": actual_dir,
            "actual_change_pct": change_pct,
            "classification": classification,
            "correct": signal_dir == _buy_sell(actual_dir),
            "reasoning_trace": signal.reasoning_trace,
        })

    return BacktestResult(results)


class BacktestResult:
    def __init__(self, results: list[dict]):
        self.results = results
        self.total = len(results)
        self.correct = sum(1 for r in results if r["correct"])
        self.accuracy = self.correct / self.total if self.total > 0 else 0.0

        self.bullish_correct = sum(1 for r in results if r["actual_direction"] == "BULLISH" and r["signal_direction"] == "BUY")
        self.bearish_correct = sum(1 for r in results if r["actual_direction"] == "BEARISH" and r["signal_direction"] == "SELL")
        self.neutral_correct = sum(1 for r in results if r["actual_direction"] == "NEUTRAL" and r["signal_direction"] == "HOLD")

        self.bullish_total = sum(1 for r in results if r["actual_direction"] == "BULLISH")
        self.bearish_total = sum(1 for r in results if r["actual_direction"] == "BEARISH")
        self.neutral_total = sum(1 for r in results if r["actual_direction"] == "NEUTRAL")

    def summary(self) -> str:
        lines = [
            "=" * 70,
            "BACKTEST RESULTS — Pipeline Accuracy vs Historical Outcomes",
            "=" * 70,
            "",
            f"Total events: {self.total}",
            f"Correct predictions: {self.correct}/{self.total}",
            f"Accuracy: {self.accuracy:.1%}",
            "",
            "--- By Direction ---",
            f"  BULLISH: {self.bullish_correct}/{self.bullish_total} correct",
            f"  BEARISH: {self.bearish_correct}/{self.bearish_total} correct",
            f"  NEUTRAL: {self.neutral_correct}/{self.neutral_total} correct",
            "",
            "--- Per-Event Breakdown ---",
        ]
        for r in self.results:
            mark = "✓" if r["correct"] else "✗"
            lines.append(
                f"  {mark} {r['ticker']:5} {r['date']}  "
                f"Signal: {r['signal_direction']:5} (conf={r['signal_confidence']:.2f})  "
                f"Actual: {r['actual_direction']:8} ({r['actual_change_pct']:+.1f}%)  "
                f"→ {r['classification']}"
            )
            for trace in r.get("reasoning_trace", []):
                lines.append(f"       {trace}")
        lines.append("")
        lines.append("=" * 70)
        return "\n".join(lines)

    def to_dict(self) -> list[dict]:
        return self.results

    def __str__(self) -> str:
        return self.summary()

    def __repr__(self) -> str:
        return f"<BacktestResult accuracy={self.accuracy:.1%} ({self.correct}/{self.total})>"


if __name__ == "__main__":
    sys.path.insert(0, ".")
    result = run_backtest()
    print(result.summary())
