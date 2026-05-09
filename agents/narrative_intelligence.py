from __future__ import annotations

import uuid
from collections import Counter, defaultdict
from datetime import datetime, timezone

from agents.models import Entity, NarrativeEvent, TopicCluster


class NarrativeIntelligenceAgent:
    def __init__(self):
        self.clusters: dict[str, TopicCluster] = {}

    def analyze(self, events: list[NarrativeEvent]) -> list[TopicCluster]:
        clusters = self._cluster_by_ticker(events)
        enriched = self._enrich_clusters(clusters, events)
        self.clusters = {c.topic_id: c for c in enriched}
        return enriched

    def _cluster_by_ticker(self, events: list[NarrativeEvent]) -> list[TopicCluster]:
        ticker_events: dict[str, list[NarrativeEvent]] = defaultdict(list)
        for event in events:
            for ticker in event.ticker_mentions:
                ticker_events[ticker].append(event)

        clusters: list[TopicCluster] = []
        for ticker, ticker_evts in ticker_events.items():
            titles = [e.title for e in ticker_evts]
            keywords = self._extract_keywords(titles)
            cluster = TopicCluster(
                topic_id=f"topic_{uuid.uuid4().hex[:8]}",
                label=f"{ticker}: {keywords[0] if keywords else 'Market Narrative'}",
                keywords=keywords,
                event_ids=[e.id for e in ticker_evts],
            )
            clusters.append(cluster)
        return clusters

    def _extract_keywords(self, texts: list[str]) -> list[str]:
        words: Counter = Counter()
        stopwords = {"the", "a", "an", "is", "are", "was", "were", "to", "in", "for", "of", "and", "on", "at", "by", "with", "from", "that", "this", "has", "had", "but", "not", "its", "it's", "been", "will", "all", "more", "than", "their", "about", "after", "before", "into", "over", "would", "could", "should", "very", "just", "also", "than", "then"}
        for text in texts:
            tokens = text.lower().replace(",", "").replace(".", "").replace("—", "").split()
            for token in tokens:
                if len(token) > 2 and token not in stopwords and token.isalpha():
                    words[token] += 1
        return [word for word, _ in words.most_common(8)]

    def _enrich_clusters(self, clusters: list[TopicCluster], events: list[NarrativeEvent]) -> list[TopicCluster]:
        now = datetime.now(timezone.utc)
        for cluster in clusters:
            cluster_events = [e for e in events if e.id in cluster.event_ids]
            if not cluster_events:
                continue

            sources = set(e.source.value for e in cluster_events)
            source_diversity = len(sources) / 4.0
            recency = sum(
                1 for e in cluster_events
                if (now - datetime.fromisoformat(e.collected_at.replace("Z", "+00:00"))).total_seconds() < 86400
            )
            cluster.propagation_rate = min(1.0, len(cluster_events) / 20.0 + source_diversity * 0.3)
            cluster.momentum_score = min(1.0, recency / max(len(cluster_events), 1) * 0.6 + source_diversity * 0.4)
            cluster.acceleration = min(1.0, cluster.propagation_rate * cluster.momentum_score * 1.5)
            cluster.confidence = min(1.0, (len(cluster_events) / 10.0 + source_diversity) / 2.0)
        return clusters

    def extract_entities(self, events: list[NarrativeEvent]) -> list[Entity]:
        seen: set[str] = set()
        entities: list[Entity] = []
        for event in events:
            for entity in event.entities:
                if entity.name not in seen:
                    seen.add(entity.name)
                    entities.append(entity)
        return entities
