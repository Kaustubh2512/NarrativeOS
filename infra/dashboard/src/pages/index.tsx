import { useEffect, useState } from "react";
import Head from "next/head";
import PipelineGraph from "@/components/PipelineGraph";
import StatusCard from "@/components/StatusCard";
import SignalTable from "@/components/SignalTable";

export default function Home() {
  const [signals, setSignals] = useState([]);
  const [status, setStatus] = useState({
    ingress: { active: false, lastRun: "", events24h: 0 },
    analysis: { active: false, lastRun: "", signals24h: 0 },
    execution: { active: false, lastRun: "", executed24h: 0 },
  });

  useEffect(() => {
    async function load() {
      try {
        const [signalsRes, statusRes] = await Promise.all([
          fetch("/api/signals"),
          fetch("/api/status"),
        ]);
        if (signalsRes.ok) setSignals(await signalsRes.json());
        if (statusRes.ok) setStatus(await statusRes.json());
      } catch {
        // Dashboard works with mock data when backend is offline
      }
    }
    load();
    const interval = setInterval(load, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <>
      <Head>
        <title>NarrativeOS — Platform Dashboard</title>
        <meta
          name="description"
          content="Real-time narrative intelligence pipeline observability"
        />
      </Head>

      <div className="min-h-screen bg-gray-50">
        <header className="border-b border-gray-200 bg-white">
          <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
            <div>
              <h1 className="text-xl font-bold text-gray-900">
                NarrativeOS
              </h1>
              <p className="text-sm text-gray-500">
                Platform Dashboard — Pipeline Observability
              </p>
            </div>
            <div className="flex items-center gap-3 text-xs text-gray-400">
              <span className="flex items-center gap-1">
                <span className="h-1.5 w-1.5 rounded-full bg-green-500" />
                All systems operational
              </span>
            </div>
          </div>
        </header>

        <main className="mx-auto max-w-7xl space-y-8 px-6 py-8">
          {/* Pipeline Graph */}
          <section>
            <h2 className="mb-4 text-lg font-semibold text-gray-800">
              Pipeline Architecture
            </h2>
            <PipelineGraph />
          </section>

          {/* Canvas Status Cards */}
          <section className="grid gap-4 sm:grid-cols-3">
            <StatusCard
              title="Ingress Canvas"
              active={status.ingress.active}
              lastRun={status.ingress.lastRun}
              metric={String(status.ingress.events24h)}
              metricLabel="events / 24h"
              color="#22c55e"
            />
            <StatusCard
              title="Analysis Canvas"
              active={status.analysis.active}
              lastRun={status.analysis.lastRun}
              metric={String(status.analysis.signals24h)}
              metricLabel="signals / 24h"
              color="#3b82f6"
            />
            <StatusCard
              title="Execution Canvas"
              active={status.execution.active}
              lastRun={status.execution.lastRun}
              metric={String(status.execution.executed24h)}
              metricLabel="executed / 24h"
              color="#f59e0b"
            />
          </section>

          {/* Recent Signals */}
          <section>
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-lg font-semibold text-gray-800">
                Recent Signals
              </h2>
              <span className="text-xs text-gray-400">
                Auto-refreshes every 15s
              </span>
            </div>
            <SignalTable signals={signals} />
          </section>
        </main>
      </div>
    </>
  );
}
