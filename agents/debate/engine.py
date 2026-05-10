from __future__ import annotations

import json
import logging
import re

from agents.llm import call_llm
from agents.models import (
    DebatePosition,
    DebateRound,
    DebateSummary,
    SentimentVector,
    TopicCluster,
)
from agents.tools import ResearchData, research_ticker_text

logger = logging.getLogger(__name__)


class BullAgent:
    def __init__(self):
        self.role = "bull"

    def build_case(
        self,
        ticker: str,
        clusters: list[TopicCluster],
        sentiment: SentimentVector,
        round_number: int = 1,
        research: ResearchData | None = None,
        counter_arguments: list[str] | None = None,
    ) -> DebatePosition:
        cluster = next((c for c in clusters if ticker in c.label), None)
        context_lines = []
        if cluster:
            context_lines.append(f"Narrative: {cluster.label}")
            context_lines.append(f"Momentum: {cluster.momentum_score:.0%}")
        context_lines.append(f"Sentiment Polarity: {sentiment.polarity:.2f}")
        context_lines.append(f"News events: {len(clusters)} clusters")

        if research:
            if research.price:
                p = research.price
                direction = "up" if p.get("change_pct", 0) > 0 else "down"
                context_lines.append(f"Price: ${p['price']} ({direction} {abs(p['change_pct']):.1f}%)")
            if research.news:
                context_lines.append("News headlines:")
                for h in research.news[:3]:
                    context_lines.append(f"  - {h}")
            if research.sec_filings:
                context_lines.append("Filings:")
                for f in research.sec_filings[:1]:
                    context_lines.append(f"  - {f}")

        rebut_text = ""
        if counter_arguments:
            rebut_text = f"\nRebut these bear arguments:\n" + "\n".join(counter_arguments[:3])

        prompt = (
            f"You are a Bullish Financial Analyst. Build a bull case for {ticker}.\n\n"
            + "\n".join(context_lines)
            + f"\nRound {round_number}.\n{rebut_text}\n\n"
            + "Provide:\n"
            + "1. Key bullish arguments (specific, data-driven)\n"
            + "2. Catalysts that could drive upside\n"
            + "3. Acknowledge one key risk\n"
            + "4. Confidence level (0-100%) end with CONFIDENCE: <number>"
        )

        result = call_llm(
            system_prompt="You are a professional bull analyst. Be concise and data-driven. End with CONFIDENCE: <number>%",
            user_prompt=prompt,
            temperature=0.7,
        )

        if result:
            confidence = self._parse_confidence(result)
            return DebatePosition(
                agent_role="bull",
                argument=result,
                evidence=["Bull case analysis"],
                confidence=round(confidence, 4),
            )

        return DebatePosition(
            agent_role="bull",
            argument=f"Bull Case for {ticker}: LLM unavailable.",
            evidence=[],
            confidence=0.5,
        )

    def _parse_confidence(self, text: str) -> float:
        match = re.search(r"CONFIDENCE\s*:\s*(\d+)", text, re.IGNORECASE)
        if match:
            return min(1.0, int(match.group(1)) / 100.0)
        return 0.6


class BearAgent:
    def __init__(self):
        self.role = "bear"

    def build_case(
        self,
        ticker: str,
        clusters: list[TopicCluster],
        sentiment: SentimentVector,
        round_number: int = 1,
        research: ResearchData | None = None,
        counter_arguments: list[str] | None = None,
    ) -> DebatePosition:
        cluster = next((c for c in clusters if ticker in c.label), None)
        context_lines = []
        if cluster:
            context_lines.append(f"Narrative: {cluster.label}")
            context_lines.append(f"Momentum: {cluster.momentum_score:.0%}")
        context_lines.append(f"Sentiment Polarity: {sentiment.polarity:.2f}")
        context_lines.append(f"Uncertainty: {sentiment.uncertainty:.2f}")

        if research:
            if research.price:
                p = research.price
                direction = "up" if p.get("change_pct", 0) > 0 else "down"
                context_lines.append(f"Price: ${p['price']} ({direction} {abs(p['change_pct']):.1f}%)")
            if research.news:
                context_lines.append("News headlines:")
                for h in research.news[:3]:
                    context_lines.append(f"  - {h}")

        rebut_text = ""
        if counter_arguments:
            rebut_text = f"\nRebuttal: Counter these bull arguments:\n" + "\n".join(counter_arguments[:3])

        prompt = (
            f"You are a Bearish Financial Analyst. Build a STRONG bear case for {ticker}.\n\n"
            + "\n".join(context_lines)
            + f"\nRound {round_number}.\n{rebut_text}\n\n"
            + "Focus on:\n"
            + "1. Why the market is wrong / overvalued\n"
            + "2. Specific risks, headwinds, competition\n"
            + "3. Why this is a sell, not a hold\n"
            + "4. Confidence level (0-100%) end with CONFIDENCE: <number>"
        )

        result = call_llm(
            system_prompt="You are a bearish analyst who looks for reasons to sell. Be aggressive and skeptical. End with CONFIDENCE: <number>%",
            user_prompt=prompt,
            temperature=0.7,
        )

        if result:
            confidence = self._parse_confidence(result)
            return DebatePosition(
                agent_role="bear",
                argument=result,
                evidence=["Bear case analysis"],
                confidence=round(confidence, 4),
            )

        return DebatePosition(
            agent_role="bear",
            argument=f"Bear Case for {ticker}: LLM unavailable.",
            evidence=[],
            confidence=0.3,
        )

    def _parse_confidence(self, text: str) -> float:
        match = re.search(r"CONFIDENCE\s*:\s*(\d+)", text, re.IGNORECASE)
        if match:
            return min(1.0, int(match.group(1)) / 100.0)
        return 0.4


class ArbiterAgent:
    def __init__(self):
        self.role = "arbiter"

    def arbitrate(
        self,
        ticker: str,
        rounds: list[DebateRound],
        sentiment: SentimentVector,
        research: ResearchData | None = None,
    ) -> DebateSummary:
        last_round = rounds[-1] if rounds else None
        if not last_round:
            return DebateSummary(bull_case="No debate", bear_case="No debate", arbiter_ruling="Insufficient data", debate_rounds=0)

        bull = last_round.bull_position
        bear = last_round.bear_position

        price_context = ""
        if research and research.price:
            p = research.price
            chg = p.get("change_pct", 0)
            price_context = f"Price Trend: ${p['price']} ({chg:+.1f}%)\n"

        news_context = ""
        if research and research.news:
            news_context = "News:\n" + "\n".join(f"  - {h}" for h in research.news[:3]) + "\n"

        prompt = (
            f"CIO Decision for {ticker}.\n\n"
            f"{price_context}"
            f"Sentiment Polarity: {sentiment.polarity:.2f} (<0 = bearish, >0 = bullish)\n"
            f"Risk Score: {sentiment.instability_score:.2f}\n"
            f"{news_context}"
            f"=== BULL CASE ===\n{bull.argument}\n\n"
            f"=== BEAR CASE ===\n{bear.argument}\n\n"
            f"Rules:\n"
            f"- Strong polarity (> 0.6) + strong bull arguments → BULL\n"
            f"- Strong negative polarity (< -0.4) + strong bear arguments → BEAR\n"
            f"- Moderate polarity or mixed debate → HOLD\n"
            f"- Trust the data: if sentiment is strongly positive AND bull case is solid, rule BULL\n"
            f"- bull_confidence + bear_confidence should sum to ~100\n"
            f"Return JSON:\n"
            f"{{\n"
            f'  "ruling": "bull" | "bear" | "hold",\n'
            f'  "reasoning": "brief explanation",\n'
            f'  "bull_confidence": 0-100,\n'
            f'  "bear_confidence": 0-100\n'
            f"}}"
        )

        result = call_llm(
            system_prompt="You are a data-driven CIO. Rule BULL when sentiment > 0.6 and bull case is strong. Rule BEAR when sentiment < -0.4 and bear case is strong. Rule HOLD for mixed or moderate signals. Output valid JSON only.",
            user_prompt=prompt,
            temperature=0.2,
            json_mode=True,
        )

        if result:
            try:
                data = json.loads(result)
                if isinstance(data, list):
                    data = data[0] if data else {}
                ruling_text = data.get("ruling", "hold")
                reasoning = data.get("reasoning", "")
                bull_conf = data.get("bull_confidence", 50)
                bear_conf = data.get("bear_confidence", 50)

                if ruling_text == "bull":
                    ruling = f"Bull case prevails — {reasoning}"
                elif ruling_text == "bear":
                    ruling = f"Bear case prevails — {reasoning}"
                else:
                    ruling = f"HOLD — {reasoning}"

                ruling += f" Bull confidence {bull_conf:.0f}% vs Bear confidence {bear_conf:.0f}%."
                return DebateSummary(bull_case=bull.argument, bear_case=bear.argument, arbiter_ruling=ruling, debate_rounds=len(rounds))
            except (json.JSONDecodeError, KeyError) as e:
                logger.error("Failed to parse arbiter JSON: %s", e)

        return DebateSummary(
            bull_case=bull.argument,
            bear_case=bear.argument,
            arbiter_ruling="HOLD — arbiter LLM unavailable.",
            debate_rounds=len(rounds),
        )


class DebateEngine:
    def __init__(self, rounds: int = 1, use_tools: bool = True):
        self.rounds = rounds
        self.use_tools = use_tools
        self.bull = BullAgent()
        self.bear = BearAgent()
        self.arbiter = ArbiterAgent()

    def conduct_debate(
        self,
        ticker: str,
        clusters: list[TopicCluster],
        sentiment: SentimentVector,
    ) -> tuple[list[DebateRound], DebateSummary]:
        research = research_ticker_text(ticker) if self.use_tools else None
        research_data = None
        if self.use_tools:
            from agents.tools import research_ticker
            research_data = research_ticker(ticker)

        debate_rounds: list[DebateRound] = []

        for r in range(1, self.rounds + 1):
            bull_pos = self.bull.build_case(ticker, clusters, sentiment, r, research_data)
            bear_pos = self.bear.build_case(ticker, clusters, sentiment, r, research_data)

            debate_rounds.append(DebateRound(round_number=r, bull_position=bull_pos, bear_position=bear_pos))

        summary = self.arbiter.arbitrate(ticker, debate_rounds, sentiment, research_data)
        return debate_rounds, summary
