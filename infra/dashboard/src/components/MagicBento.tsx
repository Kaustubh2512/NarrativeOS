import { motion } from "framer-motion";
import { memo, useMemo } from "react";

interface BentoItem {
  id: string;
  title: string;
  subtitle?: string;
  value?: string;
  icon?: React.ReactNode;
  color?: string;
  size?: "sm" | "md" | "lg" | "wide";
  children?: React.ReactNode;
}

interface MagicBentoProps {
  items: BentoItem[];
  cols?: number;
}

const sizeClasses: Record<string, string> = {
  sm: "col-span-1 row-span-1",
  md: "col-span-1 row-span-2",
  lg: "col-span-2 row-span-2",
  wide: "col-span-2 row-span-1",
};

const MagicBento = memo(function MagicBento({ items, cols = 4 }: MagicBentoProps) {
  const gridStyle = useMemo(() => ({
    gridTemplateColumns: `repeat(${cols}, 1fr)`,
  }), [cols]);

  return (
    <div className="grid gap-3" style={gridStyle}>
      {items.map((item, i) => (
        <motion.div
          key={item.id}
          className={`${sizeClasses[item.size || "sm"]} glass rounded-xl p-5 border border-white/5 flex flex-col relative overflow-hidden group`}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: i * 0.05, duration: 0.4, ease: "easeOut" }}
          whileHover={{ y: -2, borderColor: "rgba(255,255,255,0.15)" }}
        >
          {item.color && (
            <div
              className="absolute top-0 left-0 w-full h-1 opacity-60"
              style={{ background: item.color }}
            />
          )}
          <div className="flex items-center justify-between mb-2">
            {item.icon && (
              <div
                className="w-8 h-8 rounded-lg flex items-center justify-center"
                style={{ background: item.color ? `${item.color}20` : "rgba(255,255,255,0.05)" }}
              >
                {item.icon}
              </div>
            )}
            {item.value && (
              <motion.span
                className="text-xl font-bold font-heading"
                style={{ color: item.color }}
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: "spring", stiffness: 200, delay: i * 0.05 + 0.2 }}
              >
                {item.value}
              </motion.span>
            )}
          </div>
          <div className="text-sm font-semibold text-narrative-text">{item.title}</div>
          {item.subtitle && (
            <div className="text-[10px] text-narrative-text-muted mt-0.5">{item.subtitle}</div>
          )}
          {item.children && <div className="mt-2 flex-1">{item.children}</div>}
        </motion.div>
      ))}
    </div>
  );
});

export default MagicBento;
export type { BentoItem, MagicBentoProps };