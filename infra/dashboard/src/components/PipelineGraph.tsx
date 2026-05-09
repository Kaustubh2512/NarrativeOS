import { useCallback } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  Node,
  Edge,
  useNodesState,
  useEdgesState,
  MarkerType,
} from "reactflow";
import "reactflow/dist/style.css";

const initialNodes: Node[] = [
  {
    id: "apify-actors",
    type: "default",
    position: { x: 0, y: 0 },
    data: { label: "Apify Actors\nReddit · News · SEC" },
    className: "react-flow__node-trigger",
  },
  {
    id: "webhook",
    type: "default",
    position: { x: 0, y: 120 },
    data: { label: "Webhook Receiver\nPOST /apify-event" },
    className: "react-flow__node-trigger",
  },
  {
    id: "ingress-canvas",
    type: "default",
    position: { x: 0, y: 240 },
    data: {
      label:
        "Ingress Canvas\nDedup → Validate → Normalize\n→ Store → Route",
    },
    className: "react-flow__node-canvas",
  },
  {
    id: "narrative-agent",
    type: "default",
    position: { x: -200, y: 400 },
    data: { label: "Narrative Agent\nTopic Clustering\nEntity Extraction" },
    className: "react-flow__node-agent",
  },
  {
    id: "sentiment-agent",
    type: "default",
    position: { x: 0, y: 400 },
    data: { label: "Sentiment Agent\nBullish/Bearish Scoring\nEmotion" },
    className: "react-flow__node-agent",
  },
  {
    id: "debate-system",
    type: "default",
    position: { x: 200, y: 400 },
    data: { label: "Debate System\nBull · Bear · Neutral\n· Arbiter" },
    className: "react-flow__node-agent",
  },
  {
    id: "analysis-canvas",
    type: "default",
    position: { x: 0, y: 540 },
    data: {
      label:
        "Analysis Canvas\nNarrative → Sentiment → Debate\n→ Risk → Strategy",
    },
    className: "react-flow__node-canvas",
  },
  {
    id: "execution-canvas",
    type: "default",
    position: { x: 0, y: 680 },
    data: {
      label:
        "Execution Canvas\nRisk Gate → HITL → Strategy\n→ Store → Notify",
    },
    className: "react-flow__node-canvas",
  },
  {
    id: "signal-output",
    type: "default",
    position: { x: 0, y: 820 },
    data: { label: "BUY / SELL / HOLD\n/ WATCHLIST" },
    className: "react-flow__node-signal",
  },
  {
    id: "slack",
    type: "default",
    position: { x: -200, y: 820 },
    data: { label: "Slack / Discord\nNotifications" },
    className: "react-flow__node-signal",
  },
  {
    id: "pagerduty",
    type: "default",
    position: { x: 200, y: 820 },
    data: { label: "PagerDuty\nCritical Alerts" },
    className: "react-flow__node-signal",
  },
];

const initialEdges: Edge[] = [
  {
    id: "e-apify-webhook",
    source: "apify-actors",
    target: "webhook",
    markerEnd: { type: MarkerType.ArrowClosed },
    animated: true,
  },
  {
    id: "e-webhook-ingress",
    source: "webhook",
    target: "ingress-canvas",
    markerEnd: { type: MarkerType.ArrowClosed },
    animated: true,
  },
  {
    id: "e-ingress-narrative",
    source: "ingress-canvas",
    target: "narrative-agent",
    markerEnd: { type: MarkerType.ArrowClosed },
    style: { stroke: "#3b82f6" },
  },
  {
    id: "e-ingress-sentiment",
    source: "ingress-canvas",
    target: "sentiment-agent",
    markerEnd: { type: MarkerType.ArrowClosed },
    style: { stroke: "#3b82f6" },
  },
  {
    id: "e-ingress-debate",
    source: "ingress-canvas",
    target: "debate-system",
    markerEnd: { type: MarkerType.ArrowClosed },
    style: { stroke: "#3b82f6" },
  },
  {
    id: "e-narrative-analysis",
    source: "narrative-agent",
    target: "analysis-canvas",
    markerEnd: { type: MarkerType.ArrowClosed },
    animated: true,
  },
  {
    id: "e-sentiment-analysis",
    source: "sentiment-agent",
    target: "analysis-canvas",
    markerEnd: { type: MarkerType.ArrowClosed },
    animated: true,
  },
  {
    id: "e-debate-analysis",
    source: "debate-system",
    target: "analysis-canvas",
    markerEnd: { type: MarkerType.ArrowClosed },
    animated: true,
  },
  {
    id: "e-analysis-execution",
    source: "analysis-canvas",
    target: "execution-canvas",
    markerEnd: { type: MarkerType.ArrowClosed },
    animated: true,
    style: { stroke: "#22c55e", strokeWidth: 2 },
  },
  {
    id: "e-execution-signal",
    source: "execution-canvas",
    target: "signal-output",
    markerEnd: { type: MarkerType.ArrowClosed },
    animated: true,
    style: { stroke: "#f59e0b", strokeWidth: 2 },
  },
  {
    id: "e-execution-slack",
    source: "execution-canvas",
    target: "slack",
    markerEnd: { type: MarkerType.ArrowClosed },
    style: { stroke: "#94a3b8" },
  },
  {
    id: "e-execution-pagerduty",
    source: "execution-canvas",
    target: "pagerduty",
    markerEnd: { type: MarkerType.ArrowClosed },
    style: { stroke: "#ef4444" },
  },
];

export default function PipelineGraph() {
  const [nodes, , onNodesChange] = useNodesState(initialNodes);
  const [edges, , onEdgesChange] = useEdgesState(initialEdges);

  return (
    <div className="h-[600px] w-full rounded-xl border border-gray-200 bg-white shadow-sm">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        fitView
        attributionPosition="bottom-left"
        nodesDraggable={false}
        nodesConnectable={false}
        elementsSelectable={false}
      >
        <Background color="#e2e8f0" gap={24} size={1} />
        <Controls showInteractive={false} />
        <MiniMap
          nodeStrokeColor="#94a3b8"
          maskColor="rgba(0,0,0,0.08)"
          style={{ border: "1px solid #e2e8f0", borderRadius: 8 }}
        />
      </ReactFlow>
    </div>
  );
}
