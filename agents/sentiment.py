from __future__ import annotations

from agents.models import NarrativeEvent, SentimentVector


class SentimentReasoningAgent:
    POSITIVE_WORDS = {
        "bullish", "surge", "soared", "surges", "surged", "soar", "soars", "beat", "beats",
        "growth", "growing", "profit", "profits", "profitable", "upgrade", "upgraded",
        "outperform", "outperformed", "outperforms", "positive", "strong", "stronger",
        "momentum", "breakout", "rally", "rallied", "rallies", "gain", "gains", "gained",
        "rising", "rise", "rises", "boom", "booming", "record", "exceed", "exceeded",
        "exceeds", "expansion", "expanding", "opportunity", "opportunities",
        "breakthrough", "innovation", "innovative", "partnership", "partnerships",
        "launch", "launches", "launched", "accelerate", "accelerates", "accelerated",
        "dominant", "leader", "leading", "ahead", "raise", "raised", "raises", "raising",
        "boost", "boosts", "boosted", "boosting", "expand", "expands", "expanded",
        "invest", "invests", "investment", "investing", "optimistic", "optimism",
        "confidence", "confident", "recovery", "recover", "recovered", "dividend",
        "buyback", "outlook", "overweight", "upgrading", "rosy", "promising", "robust",
    }
    NEGATIVE_WORDS = {
        "bearish", "plunge", "plunged", "plunges", "crash", "crashed", "crashes",
        "miss", "missed", "misses", "missing", "loss", "losses", "lost",
        "decline", "declined", "declines", "declining", "downgrade", "downgraded",
        "downgrades", "underperform", "underperformed", "negative", "weak", "weaker",
        "weakening", "weakness", "selloff", "selloffs", "breakdown", "slump", "slumped",
        "slumps", "drop", "dropped", "drops", "dropping", "falling", "fall", "fell",
        "fallen", "bust", "debt", "debts", "lawsuit", "lawsuits", "investigation",
        "investigations", "risk", "risks", "risky", "volatile", "volatility",
        "uncertainty", "uncertain", "fear", "fears", "feared", "recession",
        "inflation", "slowdown", "slowdowns", "slow", "slows", "slowed", "slowing",
        "layoff", "layoffs", "restructuring", "default", "defaulted", "defaults",
        "disaster", "disastrous", "underweight", "cut", "cuts", "cutting",
        "struggle", "struggles", "struggled", "struggling", "worst", "worse",
        "crisis", "emergency", "reduce", "reduces", "reduced", "reducing", "reduction",
        "disappoint", "disappoints", "disappointed", "disappointing", "disappointment",
        "below", "lower", "lowered", "lowering", "soft", "softening", "soften",
        "concern", "concerns", "concerned", "worry", "worries", "worried",
        "pressure", "pressures", "pressured", "headwind", "headwinds",
        "challenge", "challenges", "challenging", "threat", "threats",
        "penalty", "penalties", "fine", "fines", "sanction", "sanctions",
        "inventory", "overhang", "dilution", "dilutive",
        "disruption", "disruptions", "disrupted", "disruptive",
        "scrutiny", "regulatory", "antitrust", "probe", "probes",
        "downside", "bleak", "gloomy", "pessimistic", "pessimism",
        "warning", "warnings", "caution", "cautious", "subdued",
        "modest", "moderated", "subpar", "tepid", "lukewarm",
    }
    INTENSITY_WORDS = {
        "huge", "massive", "extreme", "panic", "euphoria", "crash", "surge", "meltdown",
        "skyrocket", "tank", "devastating", "unprecedented", "historic", "catastrophic",
        "explosive", "moon", "dump", "frenzy", "turmoil",
    }
    UNCERTAINTY_WORDS = {
        "uncertain", "unclear", "maybe", "perhaps", "unknown", "speculation", "rumor",
        "could", "might", "possible", "unpredictable", "volatile", "ambiguous",
        "mixed", "conflicting", "unstable", "doubt", "uncertainty",
    }

    def analyze(self, events: list[NarrativeEvent]) -> SentimentVector:
        if not events:
            return SentimentVector()

        combined = " ".join(f"{e.title} {e.body}" for e in events).lower()
        words = combined.split()

        pos_count = sum(1 for w in words if w in self.POSITIVE_WORDS)
        neg_count = sum(1 for w in words if w in self.NEGATIVE_WORDS)
        int_count = sum(1 for w in words if w in self.INTENSITY_WORDS)
        unc_count = sum(1 for w in words if w in self.UNCERTAINTY_WORDS)
        total = len(words)

        net = (pos_count - neg_count) / max(pos_count + neg_count, 1)
        polarity = max(-1.0, min(1.0, net))

        intensity = min(1.0, int_count / max(total * 0.05, 1))
        uncertainty = min(1.0, unc_count / max(total * 0.05, 1))

        instability = (intensity + uncertainty) / 2.0

        pre_scored = [e.sentiment_score for e in events if e.sentiment_score is not None]
        blended_polarity = (
            (polarity + (sum(pre_scored) / len(pre_scored))) / 2.0
            if pre_scored
            else polarity
        )

        event_count_confidence = min(1.0, len(events) / 15.0)
        word_count_confidence = min(1.0, total / 500.0)
        confidence = (event_count_confidence * 0.4 + word_count_confidence * 0.6 - uncertainty * 0.3)

        return SentimentVector(
            polarity=round(max(-1.0, min(1.0, blended_polarity)), 4),
            confidence=round(max(0.0, min(1.0, confidence)), 4),
            emotional_intensity=round(intensity, 4),
            instability_score=round(instability, 4),
            uncertainty=round(uncertainty, 4),
        )
