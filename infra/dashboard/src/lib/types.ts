export interface NarrativeEvent {
  id: string;
  source: "reddit" | "news" | "sec_filing" | "twitter" | "rss" | "finance";
  source_actor: string;
  title: string;
  body: string;
  url: string;
  author?: string;
  published_at: string;
  collected_at: string;
  ticker_mentions: string[];
  entities?: Array<{ name: string; type: string; ticker: string; asset_type?: string }>;
  sentiment_score?: number | null;
  metadata?: Record<string, unknown>;
}

export type AssetType = "equity" | "crypto" | "commodity" | "etf" | "unknown";

export interface AnalysisSignal {
  signal_id: string;
  ticker: string;
  direction: "BUY" | "SELL" | "HOLD" | "WATCHLIST";
  confidence: number;
  narrative_summary: string;
  sentiment_polarity: number;
  emotional_intensity: number;
  asset_type?: AssetType;
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

export interface AgentInfo {
  id: string;
  name: string;
  role: string;
  emoji: string;
  color: string;
  description: string;
}

export const AGENTS: AgentInfo[] = [
  { id: "agent-1", name: "Data Acquisition", role: "Sensory", emoji: "antenna", color: "#06B6D4", description: "Ingests news, SEC filings, social media, RSS feeds via Apify Actors" },
  { id: "agent-2", name: "Narrative Intelligence", role: "Cognitive", emoji: "brain", color: "#8B5CF6", description: "Detects emerging narratives, clusters topics, tracks momentum" },
  { id: "agent-3", name: "Sentiment Reasoning", role: "Cognitive", emoji: "heart", color: "#EC4899", description: "Analyzes emotional direction, crowd psychology, uncertainty" },
  { id: "agent-4", name: "Market Correlation", role: "Platform", emoji: "pulse", color: "#F59E0B", description: "Maps narratives to assets, sectors, macroeconomic relationships" },
  { id: "agent-5", name: "Debate System", role: "Cognitive", emoji: "swords", color: "#EF4444", description: "Bull/Bear/Neutral debate with arbiter consensus" },
  { id: "agent-6", name: "Risk Intelligence", role: "Platform", emoji: "shield", color: "#22C55E", description: "Evaluates systemic uncertainty, anomaly detection, signal reliability" },
  { id: "agent-7", name: "Strategy", role: "Platform", emoji: "target", color: "#3B82F6", description: "Generates BUY/SELL/HOLD signals with confidence-weighted ranking" },
  { id: "agent-8", name: "Visualization", role: "Platform", emoji: "eye", color: "#A855F7", description: "Real-time narrative graphs, sentiment heatmaps, agent interaction viz" },
];
