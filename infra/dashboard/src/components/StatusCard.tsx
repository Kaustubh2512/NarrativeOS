interface StatusCardProps {
  title: string;
  active: boolean;
  lastRun: string;
  metric: string;
  metricLabel: string;
  color: string;
}

export default function StatusCard({
  title,
  active,
  lastRun,
  metric,
  metricLabel,
  color,
}: StatusCardProps) {
  return (
    <div className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-semibold text-gray-800">{title}</h3>
        <span
          className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-medium ${
            active
              ? "bg-green-50 text-green-700 ring-1 ring-green-600/20"
              : "bg-gray-50 text-gray-600 ring-1 ring-gray-500/20"
          }`}
        >
          <span
            className={`h-1.5 w-1.5 rounded-full ${
              active ? "bg-green-500" : "bg-gray-400"
            }`}
          />
          {active ? "Active" : "Inactive"}
        </span>
      </div>
      <div className="flex items-baseline gap-1">
        <span
          className="text-3xl font-bold tabular-nums"
          style={{ color }}
        >
          {metric}
        </span>
        <span className="text-sm text-gray-500">{metricLabel}</span>
      </div>
      <p className="mt-2 text-xs text-gray-400">
        Last run: {lastRun || "N/A"}
      </p>
    </div>
  );
}
