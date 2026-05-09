import type { NextApiRequest, NextApiResponse } from "next";

const SUPERPLANE_URL = process.env.NEXT_PUBLIC_SUPERPLANE_URL || "http://localhost:3000";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    const response = await fetch(`${SUPERPLANE_URL}/api/v1/status`, {
      signal: AbortSignal.timeout(5000),
    });
    if (!response.ok) throw new Error(`Superplane status: ${response.status}`);
    const data = await response.json();
    res.status(200).json(data);
  } catch {
    // Return mock status when Superplane is offline
    res.status(200).json({
      ingress: { active: false, lastRun: "--", events24h: 0 },
      analysis: { active: false, lastRun: "--", signals24h: 0 },
      execution: { active: false, lastRun: "--", executed24h: 0 },
    });
  }
}
