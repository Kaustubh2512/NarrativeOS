import { memo } from "react";
import {
  Handle,
  Position,
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  Node,
  Edge,
  useNodesState,
  useEdgesState,
  MarkerType,
  NodeProps,
} from "reactflow";
import "reactflow/dist/style.css";
import type { LucideIcon } from "lucide-react";
import {
  Radio,
  Brain,
  Heart,
  TrendingUp,
  Swords,
  Shield,
  Crosshair,
  Eye,
} from "lucide-react";

interface AgentNodeData {
  label: string;
  role: string;
  description: string;
  color: string;
  icon: string;
}

const iconMap: Record<string, LucideIcon> = {
  antenna: Radio,
  brain: Brain,
  heart: Heart,
  pulse: TrendingUp,
  swords: Swords,
  shield: Shield,
  target: Crosshair,
  eye: Eye,
};

const AgentNode = memo(({ data }: NodeProps<AgentNodeData>) => {
  const Icon = iconMap[data.icon] || Eye;
  return (
    <div
      className="glass rounded-xl px-4 py-3 min-w-[180px] border border-white/10"
      style={{ borderColor: `${data.color}40` }}
    >
      <Handle type="target" position={Position.Left} className="!bg-narrative-gold !w-2 !h-2" />
      <Handle type="source" position={Position.Right} className="!bg-narrative-gold !w-2 !h-2" />
      <Handle type="target" position={Position.Top} className="!bg-narrative-gold !w-2 !h-2" />
      <Handle type="source" position={Position.Bottom} className="!bg-narrative-gold !w-2 !h-2" />
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-lg flex items-center justify-center" style={{ background: `${data.color}20` }}>
          <Icon size={18} color={data.color} />
        </div>
        <div>
          <div className="text-sm font-semibold text-narrative-text" style={{ fontFamily: "Exo 2" }}>{data.label}</div>
          <div className="text-[10px] uppercase tracking-widest" style={{ color: data.color }}>{data.role}</div>
        </div>
      </div>
      <p className="text-[10px] text-narrative-text-muted mt-2 leading-relaxed">{data.description}</p>
    </div>
  );
});
AgentNode.displayName = "AgentNode";

const AGENT_NODES: Node<AgentNodeData>[] = [
  {
    id: "data-acq",
    type: "agent",
    position: { x: 0, y: 0 },
    data: {
      label: "Data Acquisition",
      role: "Sensory",
      description: "Ingests news, SEC filings, social media via Apify",
      color: "#06B6D4",
      icon: "antenna",
    },
  },
  {
    id: "narrative",
    type: "agent",
    position: { x: 320, y: -80 },
    data: {
      label: "Narrative Intelligence",
      role: "Cognitive",
      description: "Topic clustering, trend acceleration, entity extraction",
      color: "#8B5CF6",
      icon: "brain",
    },
  },
  {
    id: "sentiment",
    type: "agent",
    position: { x: 320, y: 80 },
    data: {
      label: "Sentiment Reasoning",
      role: "Cognitive",
      description: "Bullish/bearish scoring, emotional intensity, crowd psychology",
      color: "#EC4899",
      icon: "heart",
    },
  },
  {
    id: "market-corr",
    type: "agent",
    position: { x: 320, y: 240 },
    data: {
      label: "Market Correlation",
      role: "Platform",
      description: "Maps narratives to assets, sectors, macro relationships",
      color: "#F59E0B",
      icon: "pulse",
    },
  },
  {
    id: "debate",
    type: "agent",
    position: { x: 640, y: 80 },
    data: {
      label: "Debate System",
      role: "Cognitive",
      description: "Bull/Bear/Neutral debate with arbiter consensus",
      color: "#EF4444",
      icon: "swords",
    },
  },
  {
    id: "risk",
    type: "agent",
    position: { x: 960, y: -40 },
    data: {
      label: "Risk Intelligence",
      role: "Platform",
      description: "Anomaly detection, misinformation analysis, volatility forecasting",
      color: "#22C55E",
      icon: "shield",
    },
  },
  {
    id: "strategy",
    type: "agent",
    position: { x: 960, y: 120 },
    data: {
      label: "Strategy",
      role: "Platform",
      description: "BUY/SELL/HOLD signals with confidence-weighted ranking",
      color: "#3B82F6",
      icon: "target",
    },
  },
  {
    id: "viz",
    type: "agent",
    position: { x: 1280, y: 40 },
    data: {
      label: "Visualization",
      role: "Platform",
      description: "Real-time graphs, sentiment heatmaps, agent interaction viz",
      color: "#A855F7",
      icon: "eye",
    },
  },
];

const AGENT_EDGES: Edge[] = [
  { id: "e-acq-narr", source: "data-acq", target: "narrative", markerEnd: { type: MarkerType.ArrowClosed, color: "#8B5CF6" }, animated: true, style: { stroke: "#8B5CF6", strokeWidth: 2 } },
  { id: "e-acq-sent", source: "data-acq", target: "sentiment", markerEnd: { type: MarkerType.ArrowClosed, color: "#EC4899" }, animated: true, style: { stroke: "#EC4899", strokeWidth: 2 } },
  { id: "e-acq-corr", source: "data-acq", target: "market-corr", markerEnd: { type: MarkerType.ArrowClosed, color: "#F59E0B" }, animated: true, style: { stroke: "#F59E0B", strokeWidth: 2 } },
  { id: "e-narr-debate", source: "narrative", target: "debate", markerEnd: { type: MarkerType.ArrowClosed, color: "#EF4444" }, animated: true, style: { stroke: "#EF4444", strokeWidth: 2 } },
  { id: "e-sent-debate", source: "sentiment", target: "debate", markerEnd: { type: MarkerType.ArrowClosed, color: "#EF4444" }, animated: true, style: { stroke: "#EF4444", strokeWidth: 2 } },
  { id: "e-corr-debate", source: "market-corr", target: "debate", markerEnd: { type: MarkerType.ArrowClosed, color: "#F59E0B" }, animated: false, style: { stroke: "#F59E0B", strokeWidth: 1.5, strokeDasharray: "4 4" } },
  { id: "e-debate-risk", source: "debate", target: "risk", markerEnd: { type: MarkerType.ArrowClosed, color: "#22C55E" }, animated: true, style: { stroke: "#22C55E", strokeWidth: 2 } },
  { id: "e-debate-strat", source: "debate", target: "strategy", markerEnd: { type: MarkerType.ArrowClosed, color: "#3B82F6" }, animated: true, style: { stroke: "#3B82F6", strokeWidth: 2 } },
  { id: "e-risk-strat", source: "risk", target: "strategy", markerEnd: { type: MarkerType.ArrowClosed, color: "#22C55E" }, animated: false, style: { stroke: "#22C55E", strokeWidth: 1.5, strokeDasharray: "4 4" } },
  { id: "e-risk-viz", source: "risk", target: "viz", markerEnd: { type: MarkerType.ArrowClosed, color: "#A855F7" }, animated: true, style: { stroke: "#A855F7", strokeWidth: 2 } },
  { id: "e-strat-viz", source: "strategy", target: "viz", markerEnd: { type: MarkerType.ArrowClosed, color: "#A855F7" }, animated: true, style: { stroke: "#A855F7", strokeWidth: 2 } },
];

const nodeTypes = { agent: AgentNode };

export default function AgentFlow() {
  const [nodes] = useNodesState(AGENT_NODES);
  const [edges] = useEdgesState(AGENT_EDGES);

  return (
    <div className="h-[520px] w-full rounded-xl border border-white/10 overflow-hidden" style={{ background: "rgba(15,23,42,0.6)" }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        fitView
        fitViewOptions={{ padding: 0.3 }}
        attributionPosition="bottom-left"
        nodesDraggable={false}
        nodesConnectable={false}
        elementsSelectable={false}
        proOptions={{ hideAttribution: true }}
      >
        <Background color="rgba(148,163,184,0.15)" gap={28} size={1} />
        <Controls showInteractive={false} className="!bg-narrative-surface-2 !border-white/10" />
        <MiniMap
          nodeStrokeColor="#F59E0B"
          nodeColor={(n) => `${n.data?.color || "#334155"}80`}
          maskColor="rgba(15,23,42,0.7)"
          style={{ border: "1px solid rgba(255,255,255,0.1)", borderRadius: 8, background: "#1E293B" }}
        />
      </ReactFlow>
    </div>
  );
}
