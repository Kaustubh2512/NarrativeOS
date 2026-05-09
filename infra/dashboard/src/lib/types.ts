export interface NarrativeEvent {
  id: string;
  source: "reddit" | "news" | "sec_filing" | "twitter" | "rss";
  source_actor: string;
  title: string;
  body: string;
  url: string;
  author?: string;
  published_at: string;
  collected_at: string;
  ticker_mentions: string[];
  entities?: Array<{ name: string; type: string; ticker: string }>;
  sentiment_score?: number | null;
  metadata?: Record<string, unknown>;
}

export interface AnalysisSignal {
  signal_id: string;
  ticker: string;
  direction: "BUY" | "SELL" | "HOLD" | "WATCHLIST";
  confidence: number;
  narrative_summary: string;
  sentiment_polarity: number;
  emotional_intensity: number;
  debate_summary: {
    bull_case: string;
    bear_case: string;
    arbiter_ruling: string;
    debate_rounds: number;
  };
  risk_score: number;
  risk_factors?: string[];
  reasoning_trace: string[];
  supporting_events: string[];
  generated_at: string;
  agent_version: string;
}

export interface PipelineStatus {
  ingress: { active: boolean; lastRun: string; events24h: number };
  analysis: { active: boolean; lastRun: string; signals24h: number };
  execution: { active: boolean; lastRun: string; executed24h: number };
}
