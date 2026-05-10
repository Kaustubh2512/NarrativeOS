/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        narrative: {
          gold: "#F59E0B",
          "gold-light": "#FBBF24",
          purple: "#8B5CF6",
          "purple-light": "#A78BFA",
          green: "#22C55E",
          red: "#EF4444",
          blue: "#3B82F6",
          cyan: "#06B6D4",
          surface: "#0F172A",
          "surface-2": "#1E293B",
          "surface-3": "#334155",
          border: "rgba(255,255,255,0.08)",
          text: "#F8FAFC",
          "text-muted": "#94A3B8",
        },
      },
      fontFamily: {
        heading: ["Orbitron", "sans-serif"],
        body: ["Exo 2", "sans-serif"],
        mono: ["Fira Code", "monospace"],
      },
      backdropBlur: {
        glass: "20px",
      },
    },
  },
  plugins: [],
};
