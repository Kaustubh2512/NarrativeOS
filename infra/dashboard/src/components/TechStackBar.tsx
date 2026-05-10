import { memo } from "react";
import LogoLoop from "./LogoLoop/LogoLoop";

interface Tech {
  name: string;
  color: string;
}

const TECH_LOGOS: Tech[] = [
  { name: "Apify", color: "#22C55E" },
  { name: "Zynd", color: "#8B5CF6" },
  { name: "Superplane", color: "#F59E0B" },
  { name: "Python", color: "#3776AB" },
  { name: "FastAPI", color: "#009688" },
  { name: "Next.js", color: "#FFFFFF" },
  { name: "React Flow", color: "#FF0072" },
  { name: "LangGraph", color: "#FF6B35" },
  { name: "OpenAI", color: "#74AA9C" },
  { name: "PostgreSQL", color: "#4169E1" },
  { name: "Docker", color: "#2496ED" },
  { name: "GitHub Actions", color: "#2088FF" },
  { name: "Tailwind CSS", color: "#06B6D4" },
  { name: "D3.js", color: "#F9A03C" },
  { name: "yfinance", color: "#9945FF" },
];

const TechBadge = memo(({ name, color }: Tech) => (
  <span className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg border border-white/10 bg-narrative-surface-2/50">
    <span className="w-2 h-2 rounded-full" style={{ background: color }} />
    <span className="text-xs font-semibold text-narrative-text whitespace-nowrap">{name}</span>
  </span>
));
TechBadge.displayName = "TechBadge";

const logos = TECH_LOGOS.map((t) => ({
  node: <TechBadge name={t.name} color={t.color} />,
  title: t.name,
}));

export default memo(function TechStackBar() {
  return (
    <div className="w-full overflow-hidden py-2">
      <LogoLoop
        logos={logos}
        speed={60}
        direction="left"
        logoHeight={36}
        gap={16}
        pauseOnHover={true}
        fadeOut={true}
        fadeOutColor="#0F172A"
        ariaLabel="Technology stack"
      />
    </div>
  );
});
