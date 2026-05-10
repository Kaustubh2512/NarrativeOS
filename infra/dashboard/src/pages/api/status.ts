import type { NextApiRequest, NextApiResponse } from "next";

const BRIDGE_URL = (process.env.NEXT_PUBLIC_BRIDGE_URL || "http://localhost:8765").replace(/\/+$/, "");

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    const response = await fetch(`${BRIDGE_URL}/api/v1/status`, {
      signal: AbortSignal.timeout(15000),
    });
    if (!response.ok) throw new Error(`Bridge status: ${response.status}`);
    const data = await response.json();
    res.status(200).json(data);
  } catch {
    res.status(200).json({
      ingress: { active: false, lastRun: "--", events24h: 0 },
      analysis: { active: false, lastRun: "--", signals24h: 0 },
      execution: { active: false, lastRun: "--", executed24h: 0 },
    });
  }
}
