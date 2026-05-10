import type { NextApiRequest, NextApiResponse } from "next";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const bridgeUrl = process.env.NEXT_PUBLIC_BRIDGE_URL || "http://localhost:8765";
  const errors: string[] = [];
  let bridgeStatus = null;

  try {
    const response = await fetch(`${bridgeUrl}/api/v1/status`, {
      signal: AbortSignal.timeout(8000),
    });
    if (response.ok) {
      bridgeStatus = await response.json();
    } else {
      errors.push(`Bridge returned ${response.status}`);
    }
  } catch (e: unknown) {
    errors.push(e instanceof Error ? e.message : String(e));
  }

  res.status(200).json({
    bridge_url: bridgeUrl,
    bridge_reachable: bridgeStatus !== null,
    bridge_status: bridgeStatus,
    errors,
    node_env: process.env.NODE_ENV,
  });
}