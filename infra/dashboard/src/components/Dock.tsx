import { motion } from "framer-motion";
import { memo } from "react";

interface DockItem {
  icon: React.ReactNode;
  label: string;
  sectionIndex: number;
}

interface DockProps {
  items: DockItem[];
  activeSection: number;
  onSectionChange: (index: number) => void;
}

const Dock = memo(function Dock({ items, activeSection, onSectionChange }: DockProps) {
  return (
    <motion.div
      className="fixed bottom-6 left-1/2 z-50 flex items-end gap-1.5 rounded-2xl border border-white/10 bg-narrative-surface/80 backdrop-blur-xl px-3 py-2"
      initial={{ y: 100, opacity: 0, x: "-50%" }}
      animate={{ y: 0, opacity: 1, x: "-50%" }}
      transition={{ type: "spring", stiffness: 200, damping: 20, delay: 1 }}
    >
      {items.map((item) => {
        const isActive = activeSection === item.sectionIndex;
        return (
          <motion.button
            key={item.label}
            className="relative flex flex-col items-center justify-center rounded-xl transition-colors"
            style={{
              width: isActive ? 52 : 44,
              height: isActive ? 52 : 44,
              background: isActive ? "rgba(245, 158, 11, 0.15)" : "transparent",
            }}
            whileHover={{ width: 52, height: 52, background: "rgba(245, 158, 11, 0.1)" }}
            whileTap={{ scale: 0.9 }}
            onClick={() => onSectionChange(item.sectionIndex)}
          >
            <motion.div
              className="text-narrative-text-muted"
              style={{ color: isActive ? "#F59E0B" : undefined }}
              whileHover={{ scale: 1.2 }}
              transition={{ type: "spring", stiffness: 300 }}
            >
              {item.icon}
            </motion.div>
            {isActive && (
              <motion.span
                className="absolute -top-6 left-1/2 -translate-x-1/2 text-[10px] text-narrative-gold font-semibold whitespace-nowrap"
                initial={{ opacity: 0, y: 4 }}
                animate={{ opacity: 1, y: 0 }}
              >
                {item.label}
              </motion.span>
            )}
          </motion.button>
        );
      })}
    </motion.div>
  );
});

export default Dock;
export type { DockItem, DockProps };