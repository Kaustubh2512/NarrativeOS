import type { NextApiRequest, NextApiResponse } from "next";

const SUPERPLANE_URL = process.env.NEXT_PUBLIC_SUPERPLANE_URL || "http://localhost:3000";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    const response = await fetch(
      `${SUPERPLANE_URL}/api/v1/datasets/executed_signals/items?limit=20&sort=desc`,
      { signal: AbortSignal.timeout(5000) }
    );
    if (!response.ok) throw new Error(`Superplane signals: ${response.status}`);
    const data = await response.json();
    res.status(200).json(data);
  } catch {
    res.status(200).json([]);
  }
}
