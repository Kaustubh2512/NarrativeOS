import type { NextApiRequest, NextApiResponse } from "next";

const BRIDGE_URL = (process.env.NEXT_PUBLIC_BRIDGE_URL || "http://localhost:8765").replace(/\/+$/, "");

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    const response = await fetch(
      `${BRIDGE_URL}/api/v1/datasets/ingress/items?limit=20`,
      { signal: AbortSignal.timeout(15000) }
    );
    if (!response.ok) throw new Error(`Bridge events: ${response.status}`);
    const data = await response.json();
    res.status(200).json(data);
  } catch {
    res.status(200).json([]);
  }
}
