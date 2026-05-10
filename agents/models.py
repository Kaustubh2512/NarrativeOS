from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Direction(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"
    WATCHLIST = "WATCHLIST"


class SourceType(str, Enum):
    REDDIT = "reddit"
    NEWS = "news"
    SEC_FILING = "sec_filing"
    TWITTER = "twitter"
    RSS = "rss"
    FINANCE = "finance"


class Entity(BaseModel):
    name: str
    type: str
    ticker: str | None = None


class NarrativeEvent(BaseModel):
    id: str
    source: SourceType
    source_actor: str
    title: str
    body: str
    url: str
    author: str | None = None
    published_at: str
    collected_at: str
    ticker_mentions: list[str]
    entities: list[Entity] = []
    sentiment_score: float | None = None
    metadata: dict[str, Any] = {}


class NarrativeEventBatch(BaseModel):
    events: list[NarrativeEvent]
    trigger: str = "webhook"


class TopicCluster(BaseModel):
    topic_id: str = Field(default_factory=lambda: f"topic_{uuid.uuid4().hex[:8]}")
    label: str
    keywords: list[str]
    event_ids: list[str]
    momentum_score: float = 0.0
    propagation_rate: float = 0.0
    acceleration: float = 0.0
    confidence: float = 0.0


class SentimentVector(BaseModel):
    polarity: float = 0.0
    confidence: float = 0.0
    emotional_intensity: float = 0.0
    instability_score: float = 0.0
    uncertainty: float = 0.0


class DebatePosition(BaseModel):
    agent_role: str
    argument: str
    evidence: list[str] = []
    confidence: float = 0.0


class DebateRound(BaseModel):
    round_number: int
    bull_position: DebatePosition
    bear_position: DebatePosition


class DebateSummary(BaseModel):
    bull_case: str
    bear_case: str
    arbiter_ruling: str
    debate_rounds: int = 3


class AnalysisSignal(BaseModel):
    signal_id: str = Field(default_factory=lambda: f"sig_{datetime.now(timezone.utc).strftime('%Y%m%d')}_{uuid.uuid4().hex[:6]}")
    ticker: str
    direction: Direction
    confidence: float = 0.0
    narrative_summary: str = ""
    sentiment_polarity: float = 0.0
    emotional_intensity: float = 0.0
    debate_summary: DebateSummary | None = None
    risk_score: float = 0.0
    risk_factors: list[str] = []
    reasoning_trace: list[str] = []
    supporting_events: list[str] = []
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    agent_version: str = "narrativeos-v0.1.0"


class AgentState(BaseModel):
    events: list[NarrativeEvent] = []
    ticker: str | None = None
    topic_clusters: list[TopicCluster] = []
    sentiment: SentimentVector | None = None
    narrative_summary: str = ""
    debate_history: list[DebateRound] = []
    debate_summary: DebateSummary | None = None
    signal: AnalysisSignal | None = None
    errors: list[str] = []
