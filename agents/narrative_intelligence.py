from __future__ import annotations

import json
import logging
import uuid
from collections import Counter, defaultdict
from datetime import datetime, timezone

from agents.llm import call_llm
from agents.models import Entity, NarrativeEvent, TopicCluster

logger = logging.getLogger(__name__)


class NarrativeIntelligenceAgent:
    def __init__(self):
        self.clusters: dict[str, TopicCluster] = {}

    def analyze(self, events: list[NarrativeEvent]) -> list[TopicCluster]:
        clusters = self._cluster_by_ticker(events)
        self._llm_enrich_labels(clusters, events)
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
            tokens = text.lower().replace(",", "").replace(".", "").replace("\u2014", "").split()
            for token in tokens:
                if len(token) > 2 and token not in stopwords and token.isalpha():
                    words[token] += 1
        return [word for word, _ in words.most_common(8)]

    def _llm_enrich_labels(self, clusters: list[TopicCluster], events: list[NarrativeEvent]) -> None:
        for cluster in clusters:
            cluster_events = [e for e in events if e.id in cluster.event_ids]
            titles = "\n".join(f"- {e.title}" for e in cluster_events[:5])
            ticker = cluster.label.split(":")[0].strip()
            prompt = (
                f"Summarize the market narrative for {ticker} based on these news headlines:\n{titles}\n\n"
                f"Return JSON:\n"
                f"{{\n"
                f'  "narrative_label": "short label describing the narrative",\n'
                f'  "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]\n'
                f"}}"
            )
            result = call_llm(
                system_prompt="You are a financial narrative analyst. Identify the core narrative and key themes from news headlines. Output valid JSON only.",
                user_prompt=prompt,
                temperature=0.3,
                json_mode=True,
                max_tokens=300,
            )
            if result:
                try:
                    data = json.loads(result)
                    label = data.get("narrative_label", "")
                    if label:
                        cluster.label = f"{ticker}: {label}"
                    keywords = data.get("keywords", [])
                    if keywords:
                        cluster.keywords = keywords[:10]
                    logger.info("LLM enriched cluster %s -> %s", ticker, cluster.label)
                except (json.JSONDecodeError, KeyError) as e:
                    logger.warning("LLM enrich failed for %s: %s", ticker, e)

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
