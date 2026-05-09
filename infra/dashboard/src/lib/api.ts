const SUPERPLANE_URL = process.env.NEXT_PUBLIC_SUPERPLANE_URL || "http://localhost:3000";
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function fetchPipelineStatus(): Promise<{
  ingress: { active: boolean; lastRun: string; events24h: number };
  analysis: { active: boolean; lastRun: string; signals24h: number };
  execution: { active: boolean; lastRun: string; executed24h: number };
}> {
  const res = await fetch(`${SUPERPLANE_URL}/api/v1/status`, {
    next: { revalidate: 10 },
  });
  if (!res.ok) throw new Error("Failed to fetch pipeline status");
  return res.json();
}

export async function fetchRecentSignals(limit = 20): Promise<NarrativeOSSignal[]> {
  const signalsUrl = `${SUPERPLANE_URL}/api/v1/datasets/executed_signals/items`;
  const res = await fetch(`${signalsUrl}?limit=${limit}&sort=desc`, {
    next: { revalidate: 10 },
  });
  if (!res.ok) return [];
  return res.json();
}

export async function fetchRecentEvents(limit = 20): Promise<NarrativeOSEvent[]> {
  const eventsUrl = `${SUPERPLANE_URL}/api/v1/datasets/narrative_events/items`;
  const res = await fetch(`${eventsUrl}?limit=${limit}&sort=desc`, {
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
