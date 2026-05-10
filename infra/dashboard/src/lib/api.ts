const BRIDGE_URL = process.env.NEXT_PUBLIC_BRIDGE_URL || "http://localhost:8765";

export async function fetchPipelineStatus(): Promise<{
  ingress: { active: boolean; lastRun: string; events24h: number };
  analysis: { active: boolean; lastRun: string; signals24h: number };
  execution: { active: boolean; lastRun: string; executed24h: number };
}> {
  const res = await fetch(`${BRIDGE_URL}/api/v1/status`, {
    next: { revalidate: 10 },
  });
  if (!res.ok) throw new Error("Failed to fetch pipeline status");
  return res.json();
}

export async function fetchRecentSignals(limit = 20): Promise<NarrativeOSSignal[]> {
  const res = await fetch(`${BRIDGE_URL}/api/v1/datasets/executed_signals/items?limit=${limit}`, {
    next: { revalidate: 10 },
  });
  if (!res.ok) return [];
  return res.json();
}

export async function fetchRecentEvents(limit = 20): Promise<NarrativeOSEvent[]> {
  const res = await fetch(`${BRIDGE_URL}/api/v1/datasets/ingress/items?limit=${limit}`, {
    next: { revalidate: 10 },
  });
  if (!res.ok) return [];
  return res.json();
}

interface NarrativeOSEvent {
  id: string;
  source: string;
  title: string;
  ticker_mentions: string[];
  published_at: string;
}

interface NarrativeOSSignal {
  signal_id: string;
  ticker: string;
  direction: string;
  confidence: number;
  risk_score: number;
  generated_at: string;
}
