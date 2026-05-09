interface Signal {
  signal_id: string;
  ticker: string;
  direction: string;
  confidence: number;
  risk_score: number;
  generated_at: string;
}

const directionColors: Record<string, string> = {
  BUY: "bg-green-100 text-green-800",
  SELL: "bg-red-100 text-red-800",
  HOLD: "bg-yellow-100 text-yellow-800",
  WATCHLIST: "bg-blue-100 text-blue-800",
};

export default function SignalTable({ signals }: { signals: Signal[] }) {
  if (!signals.length) {
    return (
      <div className="rounded-xl border border-gray-200 bg-white p-8 text-center text-sm text-gray-400">
        No signals generated yet. Run a pipeline to see results.
      </div>
    );
  }

  return (
    <div className="overflow-x-auto rounded-xl border border-gray-200 bg-white shadow-sm">
      <table className="min-w-full divide-y divide-gray-200 text-sm">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-4 py-3 text-left font-medium text-gray-500">
              Signal ID
            </th>
            <th className="px-4 py-3 text-left font-medium text-gray-500">
              Ticker
            </th>
            <th className="px-4 py-3 text-left font-medium text-gray-500">
              Direction
            </th>
            <th className="px-4 py-3 text-left font-medium text-gray-500">
              Confidence
            </th>
            <th className="px-4 py-3 text-left font-medium text-gray-500">
              Risk
            </th>
            <th className="px-4 py-3 text-left font-medium text-gray-500">
              Generated
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {signals.map((s) => (
            <tr key={s.signal_id} className="hover:bg-gray-50">
              <td className="px-4 py-3 font-mono text-xs text-gray-500">
                {s.signal_id}
              </td>
              <td className="px-4 py-3 font-semibold text-gray-900">
                {s.ticker}
              </td>
              <td className="px-4 py-3">
                <span
                  className={`inline-flex rounded-full px-2 py-0.5 text-xs font-medium ${
                    directionColors[s.direction] || "bg-gray-100 text-gray-800"
                  }`}
                >
                  {s.direction}
                </span>
              </td>
              <td className="px-4 py-3 tabular-nums">
                <div className="flex items-center gap-2">
                  <div className="h-1.5 w-16 rounded-full bg-gray-200">
                    <div
                      className="h-1.5 rounded-full bg-green-500"
                      style={{ width: `${s.confidence * 100}%` }}
                    />
                  </div>
                  <span className="text-xs text-gray-500">
                    {(s.confidence * 100).toFixed(0)}%
                  </span>
                </div>
              </td>
              <td className="px-4 py-3 tabular-nums">
                <span
                  className={`text-xs font-medium ${
                    s.risk_score < 0.3
                      ? "text-green-600"
                      : s.risk_score < 0.6
                        ? "text-yellow-600"
                        : "text-red-600"
                  }`}
                >
                  {(s.risk_score * 100).toFixed(0)}%
                </span>
              </td>
              <td className="px-4 py-3 text-xs text-gray-500">
                {new Date(s.generated_at).toLocaleString()}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
