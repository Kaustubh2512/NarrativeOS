from __future__ import annotations

from agents.models import (
    AnalysisSignal,
    DebateSummary,
    Direction,
    NarrativeEvent,
    SentimentVector,
    TopicCluster,
)


class SignalAggregator:
    def generate_signal(
        self,
        ticker: str,
        clusters: list[TopicCluster],
        sentiment: SentimentVector,
        debate_summary: DebateSummary,
        events: list[NarrativeEvent],
    ) -> AnalysisSignal:
        cluster = next((c for c in clusters if ticker in c.label.split(": ")[0]), None)

        debate_score = self._score_debate(debate_summary)
        momentum_score = (cluster.momentum_score if cluster else 0.5)
        sentiment_score = sentiment.polarity

        blended = (
            debate_score * 0.5
            + (momentum_score * 2 - 1) * 0.3
            + sentiment_score * 0.2
        )

        direction = self._determine_direction(blended, debate_score)
        confidence = min(1.0, abs(blended) + 0.2)
        risk_score = max(0.0, min(1.0, sentiment.instability_score * 0.4 + sentiment.uncertainty * 0.3 + (1 - confidence) * 0.3))
        risk_factors = self._assess_risk_factors(sentiment)
        reasoning_trace = self._build_reasoning_trace(ticker, clusters, sentiment, debate_summary)

        signal = AnalysisSignal(
            ticker=ticker,
            direction=direction,
            confidence=round(confidence, 4),
            narrative_summary=cluster.label if cluster else f"{ticker} market analysis",
            sentiment_polarity=round(sentiment.polarity, 4),
            emotional_intensity=round(sentiment.emotional_intensity, 4),
            debate_summary=debate_summary,
            risk_score=round(risk_score, 4),
            risk_factors=risk_factors,
            reasoning_trace=reasoning_trace,
            supporting_events=[e.id for e in events if ticker in e.ticker_mentions],
        )

        return signal

    def _score_debate(self, debate: DebateSummary) -> float:
        ruling_lower = debate.arbiter_ruling.lower()
        if "bull case prevails" in ruling_lower:
            return 1.0
        elif "bear case prevails" in ruling_lower:
            return -1.0
        else:
            return 0.0

    def _determine_direction(self, blended: float, debate_score: float) -> Direction:
        if debate_score > 0.3:
            return Direction.BUY
        elif debate_score < -0.3:
            return Direction.SELL
        elif blended > 0.2:
            return Direction.BUY
        elif blended < -0.2:
            return Direction.SELL
        else:
            return Direction.HOLD

    def _assess_risk_factors(self, sentiment: SentimentVector) -> list[str]:
        factors = []
        if sentiment.instability_score > 0.6:
            factors.append("High narrative instability")
        if sentiment.uncertainty > 0.6:
            factors.append("Elevated uncertainty levels")
        if sentiment.emotional_intensity > 0.7:
            factors.append("Extreme emotional intensity")
        if sentiment.polarity < -0.5:
            factors.append("Strong bearish consensus")
        if sentiment.polarity > 0.8:
            factors.append("Bullish momentum strong")
        return factors

    def _build_reasoning_trace(self, ticker: str, clusters: list[TopicCluster], sentiment: SentimentVector, debate: DebateSummary) -> list[str]:
        trace = []
        cluster = next((c for c in clusters if ticker in c.label.split(": ")[0]), None)
        if cluster:
            trace.append(f"Narrative Intelligence: {cluster.label} (momentum: {cluster.momentum_score:.0%})")
        trace.append(f"Sentiment Reasoning: Polarity {sentiment.polarity:.2f}, Intensity {sentiment.emotional_intensity:.0%}")
        trace.append(f"Debate System: {debate.arbiter_ruling[:200]}")
        return trace
