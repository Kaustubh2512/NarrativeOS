import { useEffect, useRef, useState } from "react";
import Head from "next/head";
import dynamic from "next/dynamic";
import {
  TrendingUp, TrendingDown, Minus, Activity, Cpu,
  Globe, Network, Layers, ArrowRight, BarChart3,
} from "lucide-react";
import type { AnalysisSignal, PipelineStatus } from "@/lib/types";
import TechStackBar from "@/components/TechStackBar";
import Threads from "@/components/Threads";
import MagicBento from "@/components/MagicBento";
import type { BentoItem } from "@/components/MagicBento";

const AgentFlow = dynamic(() => import("@/components/AgentFlow"), { ssr: false });

const MOCK_SIGNALS: AnalysisSignal[] = [
  { signal_id: "sig_001", ticker: "NVDA", direction: "BUY", confidence: 0.93, narrative_summary: "NVIDIA Q4 FY2024: Data Center Revenue Surges 409% YoY to $18.4B — AI Demand Tipping Point Reached", sentiment_polarity: 0.9, emotional_intensity: 0.8, asset_type: "equity", debate_summary: { bull_case: "Data center revenue up 409% YoY at $18.4B, Hopper GPU demand surging, supply constraints easing, CEO says 'accelerated computing and generative AI have hit the tipping point'", bear_case: "Forward PE at 35x above 5-year average, potential export restrictions on advanced chips to China, market saturation risk as competition intensifies", arbiter_ruling: "Bull case prevails — growth fundamentals outweigh valuation concerns, AI infrastructure spend cycle still in early innings, sentiment 0.90", debate_rounds: 3 }, risk_score: 0.2, risk_factors: ["Valuation multiple compression", "Geopolitical export risk"], reasoning_trace: ["Data Acq: NVDA earnings release — revenue $22.1B vs $20.4B est", "Narrative Intel: AI infrastructure spending cycle accelerating", "Sentiment: Bullish momentum 0.90 across all tracked sources", "Market Corr: Semis sector correlated upside, AMD/TSMC also moving", "Debate: 3 rounds — Bull argues demand > supply, Bear flags valuation", "Risk: Low risk score 0.20, strong fundamentals outweigh macro", "Strategy: BUY with 93% confidence — conviction-weighted consensus"], supporting_events: [], generated_at: new Date().toISOString(), agent_version: "narrativeos-v0.1.0" },
  { signal_id: "sig_002", ticker: "TSLA", direction: "SELL", confidence: 0.57, narrative_summary: "Tesla Q4 Deliveries Miss Estimates — BYD Surpasses in Quarterly EV Sales for First Time", sentiment_polarity: -0.6, emotional_intensity: 0.7, asset_type: "equity", debate_summary: { bull_case: "EV market leader with energy storage growing 125%, long-term autonomy and Optimus robot pipeline, supercharger network moat", bear_case: "Q4 deliveries 484K vs 483K est, price cuts squeezing margins from 19.8% to 17.6%, BYD surpassed Tesla in quarterly EV sales, demand softening across all markets", arbiter_ruling: "Bear case prevails — sentiment -0.60, margin compression and demand concerns outweigh energy storage growth", debate_rounds: 3 }, risk_score: 0.65, risk_factors: ["Demand decline", "Margin compression", "BYD competition"], reasoning_trace: ["Data Acq: TSLA delivery numbers miss high-end estimates", "Narrative Intel: EV demand slowdown narrative gaining traction", "Sentiment: Negative -0.60, bearish Reddit/social volume elevated", "Market Corr: Chinese EV sector headwinds, BYD overtaking in volume", "Debate: 3 rounds — Bear shows price cuts eroding margins since Q1 2023", "Risk: Elevated risk 0.65, multiple compression risk if margins stay low", "Strategy: SELL with 57% confidence — bear case stronger but uncertainty high"], supporting_events: [], generated_at: new Date().toISOString(), agent_version: "narrativeos-v0.1.0" },
  { signal_id: "sig_003", ticker: "BTC", direction: "BUY", confidence: 0.72, narrative_summary: "SEC Approves 11 Spot Bitcoin ETFs — Projected $100B in New Institutional Demand", sentiment_polarity: 0.65, emotional_intensity: 0.75, asset_type: "crypto", debate_summary: { bull_case: "SEC approved 11 spot ETFs including BlackRock iShares and Fidelity, institutional demand $100B projected, halving supply shock incoming April 2024, ETF inflows already $10B+ in first 2 months", bear_case: "Grayscale GBTC outflows creating selling pressure, regulatory uncertainty persists under Gensler, macro headwinds from delayed rate cuts could reduce risk appetite", arbiter_ruling: "Bull case prevails — ETF approval is structural demand shift, institutional onboarding just beginning, halving adds supply-side catalyst", debate_rounds: 3 }, risk_score: 0.55, risk_factors: ["Regulatory uncertainty", "ETF flow reversal", "Macro headwinds"], reasoning_trace: ["Data Acq: SEC order approving 19b-4 filings for 11 ETFs", "Narrative Intel: 'Crypto mainstream adoption' narrative at all-time high", "Sentiment: Bullish 0.65, euphoria in crypto Twitter but measured in institutional channels", "Market Corr: BTC leading, ETH/SOL correlated upside, Coinbase as proxy", "Debate: 3 rounds — Bull cites ETF flows, Bear flags GBTC overhang", "Risk: Moderate 0.55, regulatory risk balanced by bipartisan crypto support", "Strategy: BUY with 72% confidence — structural bull case with measured position size"], supporting_events: [], generated_at: new Date().toISOString(), agent_version: "narrativeos-v0.1.0" },
  { signal_id: "sig_004", ticker: "OIL", direction: "HOLD", confidence: 0.44, narrative_summary: "Crude Spikes 5% on Hamas-Israel Conflict — Strait of Hormuz Supply Risk Priced In", sentiment_polarity: 0.1, emotional_intensity: 0.5, asset_type: "commodity", debate_summary: { bull_case: "Hamas attack on Israel raises risk of broader Middle East war, Strait of Hormuz chokepoint threatens 20% of global supply, Iran involvement could trigger US sanctions tightening, SPR at multi-decade low limits defense", bear_case: "Global economic slowdown reducing demand growth, US production at record 13.2M bpd, Biden may release more SPR barrels, OPEC+ has spare capacity of 5M+ bpd", arbiter_ruling: "HOLD — mixed signals, geopolitical risk premium vs demand destruction fears create balanced risk-reward at current levels", debate_rounds: 3 }, risk_score: 0.5, risk_factors: ["Geopolitical escalation", "Demand uncertainty", "SPR intervention"], reasoning_trace: ["Data Acq: Hamas attack Oct 7 — WTI spikes 5% to $86", "Narrative Intel: 'Middle East supply disruption' narrative forming but unconfirmed", "Sentiment: Neutral 0.10, lack of clear directional conviction across sources", "Market Corr: Gold correlated upside, equities selling off, dollar bid", "Debate: 3 rounds — Bull sees supply risk, Bear sees demand destruction", "Risk: Balanced 0.50, binary event risk from further escalation", "Strategy: HOLD with 44% confidence — wait for supply disruption confirmation"], supporting_events: [], generated_at: new Date().toISOString(), agent_version: "narrativeos-v0.1.0" },
  { signal_id: "sig_005", ticker: "META", direction: "BUY", confidence: 0.93, narrative_summary: "Meta Q4 Blowout: Revenue $40.1B, First-Ever Dividend Initiated, $50B Buyback Authorized", sentiment_polarity: 0.9, emotional_intensity: 0.8, asset_type: "equity", debate_summary: { bull_case: "Revenue $40.1B vs $39.2B est (+25% YoY), first-ever $0.50 dividend, $50B buyback, DAUs 2.11B beating expectations, ad revenue accelerating, Reality Labs revenue beat", bear_case: "Regulatory scrutiny from EU DMA and US antitrust, Reality Labs losing $4.6B/quarter, ad market cyclicality if recession hits", arbiter_ruling: "Bull case prevails — earnings beat across all segments, dividend initiation signals capital return confidence, sentiment 0.90", debate_rounds: 3 }, risk_score: 0.25, risk_factors: ["Regulatory risk (EU DMA)"], reasoning_trace: ["Data Acq: META Q4 2023 earnings — revenue $40.1B beat $39.2B", "Narrative Intel: 'Meta efficiency year' narrative playing out, costs down $7B YoY", "Sentiment: Very positive 0.90, dividend initiates new investor base", "Market Corr: Digital advertising sector uplift, Snap/Google ad rev correlated", "Debate: 3 rounds — Bull emphasizes margin expansion, Bear flags regulatory", "Risk: Low 0.25, dividend provides downside support", "Strategy: BUY with 93% confidence — efficiency story + capital returns"], supporting_events: [], generated_at: new Date().toISOString(), agent_version: "narrativeos-v0.1.0" },
  { signal_id: "sig_006", ticker: "GOLD", direction: "BUY", confidence: 0.68, narrative_summary: "Gold Hits All-Time High Above $2,100 — Central Bank Buying at Record Pace, Rate Cut Cycle Imminent", sentiment_polarity: 0.55, emotional_intensity: 0.6, asset_type: "commodity", debate_summary: { bull_case: "All-time high above $2,100, Fed pivot to rate cuts in 2024, central bank gold buying at record pace led by China and Poland, dollar weakness and falling yields as tailwinds", bear_case: "Strong dollar could resume if inflation re-accelerates, crypto ETF inflows competing for safe-haven demand, equity bull market reduces haven appetite", arbiter_ruling: "Bull case prevails — central bank structural buying + rate cut cycle create multi-quarter tailwinds, sentiment moderately positive at 0.55", debate_rounds: 3 }, risk_score: 0.35, risk_factors: ["Inflation re-acceleration", "Dollar strength reversal"], reasoning_trace: ["Data Acq: XAU/USD breaks $2,100 on Powell dovish comments", "Narrative Intel: 'Safe haven + rate cut' dual narrative driving demand", "Sentiment: Moderately positive 0.55, institutional flows supportive", "Market Corr: Real rates falling, gold inversely correlated, miners following", "Debate: 3 rounds — Bull cites central bank structural demand, Bear flags crypto competition", "Risk: Moderate-low 0.35, geopolitical uncertainty adds haven bid", "Strategy: BUY with 68% confidence — structural demand + macro tailwinds"], supporting_events: [], generated_at: new Date().toISOString(), agent_version: "narrativeos-v0.1.0" },
  { signal_id: "sig_007", ticker: "ETH", direction: "BUY", confidence: 0.61, narrative_summary: "Ethereum Surges on SEC Engagement Over Spot ETF Filings — Approval Odds Jump from 25% to 75%", sentiment_polarity: 0.5, emotional_intensity: 0.65, asset_type: "crypto", debate_summary: { bull_case: "SEC suddenly engaging with ETF issuers after months of silence, Bloomberg odds jumped 25%→75%, bipartisan crypto legislation momentum, EIP-4844 driving L2 adoption and fee reduction", bear_case: "SOL and rival L1s gaining Denali/CoreDAO market share, staking classification uncertain under SEC, gas fee competition from L2 fragmentation", arbiter_ruling: "Bull case prevails — regulatory pivot on crypto is structural shift, ETF approval would unlock institutional demand similar to Bitcoin", debate_rounds: 3 }, risk_score: 0.45, risk_factors: ["ETF approval uncertainty", "L1 competition (SOL)"], reasoning_trace: ["Data Acq: SEC requests 19b-4 updates from Nasdaq/CBOE for ETH ETFs", "Narrative Intel: 'Regulatory pivot on crypto' narrative forming rapidly", "Sentiment: Positive 0.50, ETF anticipation driving institutional interest", "Market Corr: BTC leading, ETH beta trade, Coinbase/COIN correlated", "Debate: 3 rounds — Bull cites political shift, Bear cites staking regulatory gap", "Risk: Moderate 0.45, binary event risk from SEC decision", "Strategy: BUY with 61% confidence — asymmetric upside if approved"], supporting_events: [], generated_at: new Date().toISOString(), agent_version: "narrativeos-v0.1.0" },
  { signal_id: "sig_008", ticker: "AAPL", direction: "HOLD", confidence: 0.44, narrative_summary: "Apple Cuts iPhone Orders 15% in China — Huawei Competition Intensifies, Services Revenue at Record High", sentiment_polarity: -0.3, emotional_intensity: 0.55, asset_type: "equity", debate_summary: { bull_case: "Services revenue at all-time high $23.1B (+11% YoY), massive ecosystem lock-in with 2.2B active devices, AI features in iOS 18 could drive super-cycle, $90B+ buyback runway", bear_case: "iPhone orders cut 15% for March quarter in China, Huawei Mate 60 gaining share, EU DMA forcing App Store changes, China revenue -13% YoY", arbiter_ruling: "HOLD — services growth + buyback vs China headwinds + competition create balanced risk-reward at current valuation", debate_rounds: 3 }, risk_score: 0.45, risk_factors: ["China revenue exposure (20%)", "Huawei competition", "EU regulatory pressure"], reasoning_trace: ["Data Acq: Supply chain checks — iPhone orders reduced 15% for Q1", "Narrative Intel: 'China slowdown for Apple' narrative vs 'Services transformation'", "Sentiment: Slightly negative -0.30, mixed signals across news sources", "Market Corr: China tech sector weakness, but US tech overall resilient", "Debate: 3 rounds — Bull focuses on services, Bear on China demand", "Risk: Moderate 0.45, binary risk from China tariff escalation", "Strategy: HOLD with 44% confidence — wait for clearer demand signal"], supporting_events: [], generated_at: new Date().toISOString(), agent_version: "narrativeos-v0.1.0" },
];

const MOCK_STATUS: PipelineStatus = {
  ingress: { active: true, lastRun: "2 min ago", events24h: 143 },
  analysis: { active: true, lastRun: "47 sec ago", signals24h: 34 },
  execution: { active: true, lastRun: "12 sec ago", executed24h: 18 },
};

const SPONSORS = [
  {
    name: "Apify",
    tagline: "Internet Sensory Layer",
    icon: Globe,
    color: "#22C55E",
    description: "Autonomous web scraping and structured data extraction at scale — deployed as 4 custom Actors.",
    usage: "4 Apify Actors deployed (narrativeos-news-scraper, narrativeos-sec-scraper, narrativeos-twitter-scraper, narrativeos-reddit-scraper) continuously ingest news RSS, SEC EDGAR filings, Google News feeds, and social media. Each actor outputs structured NarrativeEvent objects consumed by the agent mesh.",
    detail: "Built with Apify SDK v3 and Crawlee. News Actor uses RSS + CheerioCrawler for article extraction. SEC Actor targets EDGAR full-text filings. Twitter Actor uses Google News RSS with Playwright fallback. Proxy rotation via BUYPROXIES94952 group (5 datacenter proxies). All actors deployed to Apify cloud from /data/actors/.",
  },
  {
    name: "Zynd",
    tagline: "Agent Registry & Mesh",
    icon: Network,
    color: "#8B5CF6",
    description: "Decentralized agent discovery, identity, and inter-agent communication.",
    usage: "All 8 NarrativeOS agents register as discoverable Zynd entities. Each agent runs on port 5005 with ngrok tunnel. The agent wrapper in /agent.py uses Zynd SDK v0.6.0 on_message() handler. Agents discover each other dynamically during collaborative debate rounds.",
    detail: "Zynd A2A protocol enables structured message passing between bull/bear/arbiter agents during 3-round debate. Each agent maintains contextual memory across rounds. AgentConfig handles registration — ngrok managed externally. Webhook at /a2a/v1 receives analysis events from the Superplane bridge.",
  },
  {
    name: "Superplane",
    tagline: "Workflow Orchestration",
    icon: Layers,
    color: "#F59E0B",
    description: "Event-driven workflow engine for long-running agent pipelines with real-time tracing.",
    usage: "Superplane orchestrates Ingress → Analysis → Execution canvases. Each canvas is a directed workflow with entry/exit points. The FastAPI bridge (port 8765) in /infra/superplane/bridge.py connects Superplane to the dashboard API routes and agent webhooks.",
    detail: "Pipeline stages: Ingress (data acquisition via Apify), Analysis (LangGraph agent graph: Narrative → Sentiment → Debate → Signal), Execution (signal publishing). The bridge proxy allows the dashboard to display live pipeline status, events, and generated signals. Docker Compose deploys all 7 services (postgres, superplane, bridge, dashboard, 4 agent instances).",
  },
];

const ASSET_COVERAGE = [
  { type: "Equities", count: 22, color: "#3B82F6", tickers: "NVDA, AAPL, TSLA, META, AMZN, MSFT, GOOGL, AMD, JPM, SMCI, CRM, ADBE, NFLX, INTC, BA, DIS, KO, PEP, WMT, XOM, CVX, WFC" },
  { type: "Crypto", count: 8, color: "#8B5CF6", tickers: "BTC, ETH, SOL, XRP, DOGE, ADA, DOT, LINK" },
  { type: "Commodities", count: 14, color: "#F59E0B", tickers: "GOLD, OIL, NG, COPPER, SILVER, PLATINUM, CORN, WHEAT, SOYBEAN, COTTON, SUGAR, COFFEE, CATTLE, HOGS" },
  { type: "ETFs", count: 2, color: "#06B6D4", tickers: "SPY, QQQ" },
];

function SentimentGauge({ polarity, label }: { polarity: number; label: string }) {
  const pct = Math.abs(polarity) * 100;
  const color = polarity > 0.3 ? "#22C55E" : polarity < -0.3 ? "#EF4444" : "#F59E0B";
  const Icon = polarity > 0.3 ? TrendingUp : polarity < -0.3 ? TrendingDown : Minus;
  return (
    <div className="flex items-center gap-2">
      <Icon size={14} color={color} />
      <div className="w-20 h-1.5 rounded-full bg-narrative-surface-3 overflow-hidden">
        <div className="h-full rounded-full transition-all duration-1000" style={{ width: `${pct}%`, background: color }} />
      </div>
      <span className="text-xs font-semibold min-w-[40px]" style={{ color }}>{polarity > 0 ? "+" : ""}{(polarity * 100).toFixed(0)}%</span>
    </div>
  );
}

function SignalRow({ signal, onToggle, expanded }: { signal: AnalysisSignal; onToggle: () => void; expanded: boolean }) {
  const dirColor = signal.direction === "BUY" ? "#22C55E" : signal.direction === "SELL" ? "#EF4444" : "#F59E0B";
  const DirIcon = signal.direction === "BUY" ? TrendingUp : signal.direction === "SELL" ? TrendingDown : Minus;
  const assetColors: Record<string, string> = { equity: "#3B82F6", crypto: "#8B5CF6", commodity: "#F59E0B", etf: "#06B6D4", unknown: "#94A3B8" };
  return (
    <div>
      <div className="glass rounded-xl p-4 flex items-center gap-4 hover:border-narrative-gold/30 transition-all duration-300 cursor-pointer" onClick={onToggle}>
        <div className="flex flex-col items-center w-16">
          <DirIcon size={20} color={dirColor} />
          <span className="text-xs font-bold font-heading mt-0.5" style={{ color: dirColor }}>{signal.direction} {(signal.confidence * 100).toFixed(0)}%</span>
        </div>
        <div className="flex-1">
          <div className="flex items-center gap-2">
            <span className="text-sm font-semibold text-narrative-text">{signal.ticker}</span>
            <span className="text-[10px] px-2 py-0.5 rounded-full font-medium" style={{ background: `${assetColors[signal.asset_type || "unknown"]}20`, color: assetColors[signal.asset_type || "unknown"] }}>
              {signal.asset_type || "unknown"}
            </span>
          </div>
          <p className="text-xs text-narrative-text-muted mt-0.5">{signal.narrative_summary}</p>
        </div>
        <SentimentGauge polarity={signal.sentiment_polarity} label="sentiment" />
        <ArrowRight size={14} className={`text-narrative-text-muted transition-transform duration-200 ${expanded ? "rotate-90" : ""}`} />
      </div>
      {expanded && signal.debate_summary && (
        <div className="glass rounded-xl mt-2 p-4 border border-narrative-gold/10 space-y-3">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            <div className="bg-narrative-surface-2/50 rounded-lg p-3 border-l-2 border-narrative-green">
              <div className="text-[10px] uppercase tracking-widest text-narrative-green font-semibold mb-1">Bull Case</div>
              <p className="text-xs text-narrative-text leading-relaxed">{signal.debate_summary.bull_case}</p>
            </div>
            <div className="bg-narrative-surface-2/50 rounded-lg p-3 border-l-2 border-red-500">
              <div className="text-[10px] uppercase tracking-widest text-red-400 font-semibold mb-1">Bear Case</div>
              <p className="text-xs text-narrative-text leading-relaxed">{signal.debate_summary.bear_case}</p>
            </div>
            <div className="bg-narrative-surface-2/50 rounded-lg p-3 border-l-2 border-narrative-gold">
              <div className="text-[10px] uppercase tracking-widest text-narrative-gold font-semibold mb-1">Arbiter Ruling</div>
              <p className="text-xs text-narrative-text leading-relaxed">{signal.debate_summary.arbiter_ruling}</p>
            </div>
          </div>
          {signal.reasoning_trace && (
            <div className="flex flex-wrap gap-1.5">
              {signal.reasoning_trace.map((t, i) => (
                <span key={i} className="text-[10px] px-2 py-0.5 rounded-full bg-narrative-surface-3 text-narrative-text-muted">{t}</span>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default function Home() {
  const [signals, setSignals] = useState<AnalysisSignal[]>(MOCK_SIGNALS);
  const [status, setStatus] = useState(MOCK_STATUS);
  const [expandedSignal, setExpandedSignal] = useState<string | null>(null);
  const sectionsRef = useRef<(HTMLElement | null)[]>([]);

  useEffect(() => {
    async function load() {
      try {
        const [sr, st] = await Promise.all([fetch("/api/signals"), fetch("/api/status")]);
        if (sr.ok) { const d = await sr.json(); if (d.length) setSignals(d); }
        if (st.ok) { const d = await st.json(); setStatus(d); }
      } catch { /* use mock data */ }
    }
    load();
    const interval = setInterval(load, 15000);
    return () => clearInterval(interval);
  }, []);

  const metrics = [
    { label: "Assets Covered", value: "46", sub: "22 equities · 8 crypto · 14 commodities · 2 ETFs", color: "#8B5CF6" },
    { label: "Pipeline Accuracy", value: "62.5%", sub: "backtested on 16 historical events (crypto/commodity: 83.3%)", color: "#22C55E" },
    { label: "Active Agents", value: "8", sub: "Acquisition → Narrative → Sentiment → Correlation → Debate → Risk → Strategy → Viz", color: "#F59E0B" },
    { label: "Events / Day", value: `${status.ingress.events24h}`, sub: "ingested from News · SEC · RSS feeds", color: "#06B6D4" },
  ];

  return (
    <>
      <Head>
        <title>NarrativeOS — Multi-Agent Narrative Intelligence</title>
        <meta name="description" content="Decentralized multi-agent narrative intelligence network for financial markets" />
      </Head>

      <div className="min-h-screen">
        {/* ── Fixed Nav ── */}
        <nav className="fixed top-0 left-0 right-0 z-50 glass border-b border-white/5">
          <div className="max-w-7xl mx-auto px-6 h-14 flex items-center justify-between">
            <span className="text-lg font-bold font-heading" style={{ fontFamily: "Orbitron" }}>
              <span className="text-narrative-gold">Narrative</span><span className="text-narrative-text">OS</span>
            </span>
            <div className="flex items-center gap-6 text-xs text-narrative-text-muted">
              {["About", "Architecture", "Sponsors", "Signals"].map((s, i) => (
                <a key={s} href={`#section-${i}`} className="hover:text-narrative-gold transition-colors duration-200">{s}</a>
              ))}
            </div>
          </div>
        </nav>

        {/* ── Section 0: Hero ── */}
        <section ref={(el) => { sectionsRef.current[0] = el; }} id="section-0" className="min-h-screen flex items-center justify-center relative overflow-hidden pt-14">
          <Threads color={[0.96, 0.62, 0.04]} amplitude={1.5} distance={0.3} />
          <div className="absolute inset-0 opacity-20" style={{
            background: "radial-gradient(ellipse at 30% 50%, rgba(139,92,246,0.3) 0%, transparent 60%), radial-gradient(ellipse at 70% 50%, rgba(245,158,11,0.2) 0%, transparent 60%)",
          }} />
          <div className="max-w-5xl mx-auto px-6 text-center relative z-10">
            <div className="inline-flex items-center gap-2 glass rounded-full px-4 py-1.5 mb-8 text-xs text-narrative-text-muted border border-white/5">
              <Activity size={12} className="text-narrative-green" />
              Multi-Agent Financial Intelligence
            </div>
            <h1 className="text-5xl md:text-7xl font-bold font-heading mb-6 tracking-tight" style={{ fontFamily: "Orbitron" }}>
              <span className="text-narrative-gold">Narrative</span>
              <span className="text-narrative-text">OS</span>
            </h1>
            <p className="text-lg md:text-xl text-narrative-text max-w-3xl mx-auto leading-relaxed mb-10">
              An autonomous multi-agent system with <span className="text-narrative-gold font-semibold">8 specialized AI agents</span> that monitors narratives
              across news, SEC filings, and social media — scoring sentiment, debating market impact,
              and generating <span className="text-narrative-gold font-semibold">confidence-weighted trading signals</span>.
            </p>
            <div className="flex flex-wrap justify-center gap-3 mb-16">
              {[
                { label: "8 Specialized Agents", color: "#8B5CF6" },
                { label: "46 Assets Tracked", color: "#22C55E" },
                { label: "Apify + Zynd + Superplane", color: "#F59E0B" },
              ].map((b) => (
                <span key={b.label} className="glass rounded-full px-4 py-2 text-xs font-medium border border-white/5" style={{ color: b.color }}>
                  {b.label}
                </span>
              ))}
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-3xl mx-auto">
              {metrics.map((m) => (
                <div key={m.label} className="glass rounded-xl p-4 text-center">
                  <div className="text-2xl md:text-3xl font-bold font-heading" style={{ color: m.color }}>{m.value}</div>
                  <div className="text-xs text-narrative-text-muted mt-1">{m.sub}</div>
                </div>
              ))}
            </div>
            <div className="mt-16 max-w-4xl mx-auto">
              <p className="text-[10px] uppercase tracking-[0.3em] text-narrative-text-muted mb-4">Powered by</p>
              <TechStackBar />
            </div>
          </div>
        </section>

        {/* ── Section 1: Architecture ── */}
        <section ref={(el) => { sectionsRef.current[1] = el; }} id="section-1" className="py-24 relative">
          <div className="max-w-7xl mx-auto px-6">
            <div className="text-center mb-16">
              <span className="text-[10px] uppercase tracking-[0.3em] text-narrative-gold font-semibold">Chapter 01</span>
              <h2 className="text-3xl md:text-4xl font-bold font-heading mt-3 mb-4 text-narrative-text" style={{ fontFamily: "Orbitron" }}>Agent Mesh Architecture</h2>
              <p className="text-sm text-narrative-text-muted max-w-2xl mx-auto">
                Eight specialized AI agents collaborate in a directed reasoning pipeline — from raw data acquisition to confidence-weighted trading signals.
              </p>
            </div>
            <AgentFlow />
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-8">
              {[
                { stage: "01", title: "Sensory", desc: "Data Acquisition ingests from news, SEC, social, RSS via Apify", color: "#06B6D4" },
                { stage: "02", title: "Cognitive", desc: "Narrative + Sentiment + Debate agents reason collaboratively", color: "#8B5CF6" },
                { stage: "03", title: "Platform", desc: "Market Correlation + Risk + Strategy + Viz agents produce signals", color: "#F59E0B" },
                { stage: "04", title: "Output", desc: "BUY/SELL/HOLD with debate summary, confidence, reasoning trace", color: "#22C55E" },
              ].map((s) => (
                <div key={s.stage} className="glass rounded-xl p-4 border-l-2" style={{ borderLeftColor: s.color }}>
                  <div className="text-[10px] uppercase tracking-widest font-semibold" style={{ color: s.color }}>Stage {s.stage}</div>
                  <div className="text-sm font-semibold text-narrative-text mt-1">{s.title}</div>
                  <p className="text-xs text-narrative-text-muted mt-1">{s.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── Section 2: Sponsors ── */}
        <section ref={(el) => { sectionsRef.current[2] = el; }} id="section-2" className="py-24 relative">
          <div className="max-w-7xl mx-auto px-6">
            <div className="text-center mb-16">
              <span className="text-[10px] uppercase tracking-[0.3em] text-narrative-gold font-semibold">Chapter 02</span>
              <h2 className="text-3xl md:text-4xl font-bold font-heading mt-3 mb-4 text-narrative-text" style={{ fontFamily: "Orbitron" }}>Powered By</h2>
              <p className="text-sm text-narrative-text-muted max-w-2xl mx-auto">
                Three sponsor technologies form the infrastructure backbone of NarrativeOS.
              </p>
            </div>
            <div className="grid md:grid-cols-3 gap-6">
              {SPONSORS.map((s) => {
                const Icon = s.icon;
                return (
                  <div key={s.name} className="glass rounded-xl p-6 border border-white/5 hover:border-white/20 transition-all duration-300 group">
                    <div className="flex items-center gap-3 mb-4">
                      <div className="w-10 h-10 rounded-xl flex items-center justify-center" style={{ background: `${s.color}20` }}>
                        <Icon size={20} color={s.color} />
                      </div>
                      <div>
                        <div className="text-lg font-bold font-heading text-narrative-text">{s.name}</div>
                        <div className="text-[10px] uppercase tracking-widest" style={{ color: s.color }}>{s.tagline}</div>
                      </div>
                    </div>
                    <p className="text-xs text-narrative-text leading-relaxed mb-4">{s.description}</p>
                    <div className="glass rounded-lg p-3 border border-white/5 bg-narrative-surface-2/30">
                      <div className="text-[10px] uppercase tracking-widest text-narrative-gold font-semibold mb-1.5">In NarrativeOS</div>
                      <p className="text-xs text-narrative-text-muted leading-relaxed">{s.usage}</p>
                    </div>
                  </div>
                );
              })}
            </div>
            <div className="mt-12 grid md:grid-cols-3 gap-6">
              {SPONSORS.map((s) => (
                <div key={`${s.name}-detail`} className="glass rounded-xl p-5 border border-white/5">
                  <div className="flex items-center gap-2 mb-2">
                    <Cpu size={14} color={s.color} />
                    <span className="text-xs font-semibold text-narrative-text">Technical Detail</span>
                  </div>
                  <p className="text-xs text-narrative-text-muted leading-relaxed">{s.detail}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── Section 3: Asset Coverage ── */}
        <section ref={(el) => { sectionsRef.current[3] = el; }} className="py-24 relative">
          <div className="max-w-7xl mx-auto px-6">
            <div className="text-center mb-16">
              <span className="text-[10px] uppercase tracking-[0.3em] text-narrative-gold font-semibold">Chapter 03</span>
              <h2 className="text-3xl md:text-4xl font-bold font-heading mt-3 mb-4 text-narrative-text" style={{ fontFamily: "Orbitron" }}>Market Coverage</h2>
              <p className="text-sm text-narrative-text-muted max-w-2xl mx-auto">
                46 tickers across equities, crypto, commodities, and ETFs — each with detected narrative context and sentiment analysis.
              </p>
            </div>
            <MagicBento
              cols={4}
              items={ASSET_COVERAGE.map((a) => ({
                id: a.type,
                title: a.type,
                value: `${a.count}`,
                color: a.color,
                icon: <BarChart3 size={16} color={a.color} />,
                size: "sm" as const,
                subtitle: a.tickers,
              })) as BentoItem[]}
            />

            {/* ── Live Signals ── */}
            <div className="mb-8">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h3 className="text-lg font-bold font-heading text-narrative-text" style={{ fontFamily: "Orbitron" }}>Live Signals</h3>
                  <p className="text-xs text-narrative-text-muted mt-1">Real-time trading signals generated by the agent debate pipeline</p>
                </div>
                <div className="flex items-center gap-2 text-xs text-narrative-text-muted">
                  <span className="w-1.5 h-1.5 rounded-full bg-narrative-green pulse-dot" />
                  Auto-refreshing every 15s
                </div>
              </div>
              <div className="space-y-2">
                {signals.map((s) => (
                  <SignalRow key={s.signal_id} signal={s} expanded={expandedSignal === s.signal_id} onToggle={() => setExpandedSignal(expandedSignal === s.signal_id ? null : s.signal_id)} />
                ))}
              </div>
            </div>

            {/* ── System Status ── */}
            <div>
              <h3 className="text-lg font-bold font-heading text-narrative-text mb-6" style={{ fontFamily: "Orbitron" }}>System Status</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {[
                  { title: "Ingress Pipeline", active: status.ingress.active, metric: `${status.ingress.events24h}`, label: "events / 24h", lastRun: status.ingress.lastRun, color: "#06B6D4" },
                  { title: "Analysis Engine", active: status.analysis.active, metric: `${status.analysis.signals24h}`, label: "signals / 24h", lastRun: status.analysis.lastRun, color: "#8B5CF6" },
                  { title: "Execution", active: status.execution.active, metric: `${status.execution.executed24h}`, label: "executed / 24h", lastRun: status.execution.lastRun, color: "#22C55E" },
                ].map((s) => (
                  <div key={s.title} className="glass rounded-xl p-5 border border-white/5">
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-sm font-semibold text-narrative-text">{s.title}</span>
                      <span className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-[10px] font-medium ${s.active ? "bg-green-500/10 text-narrative-green" : "bg-gray-500/10 text-narrative-text-muted"}`}>
                        <span className={`w-1.5 h-1.5 rounded-full ${s.active ? "bg-narrative-green" : "bg-gray-400"}`} />
                        {s.active ? "Active" : "Inactive"}
                      </span>
                    </div>
                    <div className="flex items-baseline gap-1">
                      <span className="text-2xl font-bold font-heading" style={{ color: s.color }}>{s.metric}</span>
                      <span className="text-xs text-narrative-text-muted">{s.label}</span>
                    </div>
                    <p className="text-[10px] text-narrative-text-muted mt-2">Last run: {s.lastRun}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* ── Footer / CTA ── */}
        <footer className="border-t border-white/5 py-12">
          <div className="max-w-7xl mx-auto px-6 text-center">
            <p className="text-lg font-bold font-heading text-narrative-text mb-2" style={{ fontFamily: "Orbitron" }}>
              <span className="text-narrative-gold">Narrative</span>OS
            </p>
            <p className="text-xs text-narrative-text-muted mb-8">Decentralized multi-agent narrative intelligence for financial markets</p>
            <div className="flex justify-center gap-6 text-xs text-narrative-text-muted">
              <span>Powered by Apify</span>
              <span className="text-narrative-gold">&#183;</span>
              <span>Registered on Zynd</span>
              <span className="text-narrative-gold">&#183;</span>
              <span>Orchestrated by Superplane</span>
            </div>
            <p className="text-[10px] text-narrative-text-muted mt-8">&copy; {new Date().getFullYear()} NarrativeOS. Built for the Agentic Hackathon.</p>
          </div>
        </footer>
      </div>
    </>
  );
}
