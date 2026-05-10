import { useEffect, useRef, memo } from "react";

interface ThreadsProps {
  color?: [number, number, number];
  amplitude?: number;
  distance?: number;
  enableMouseInteraction?: boolean;
}

interface Point {
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
  phase: number;
}

const Threads = memo(function Threads({
  color = [0.96, 0.62, 0.04],
  amplitude = 1,
  distance = 0.25,
  enableMouseInteraction = true,
}: ThreadsProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const mouseRef = useRef({ x: 0.5, y: 0.5, prevX: 0.5, prevY: 0.5 });
  const pointsRef = useRef<Point[]>([]);
  const animationRef = useRef(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let w = window.innerWidth;
    let h = window.innerHeight;
    let time = 0;
    const COUNT = 80;
    const CONNECT_DIST = Math.min(w, h) * distance;

    const resize = () => {
      w = window.innerWidth;
      h = window.innerHeight;
      canvas!.width = w;
      canvas!.height = h;
      const cols = Math.ceil(Math.sqrt(COUNT * (w / h)));
      const rows = Math.ceil(COUNT / cols);
      pointsRef.current = [];
      for (let i = 0; i < COUNT; i++) {
        const col = i % cols;
        const row = Math.floor(i / cols);
        const x = (col + 0.5) * (w / cols);
        const y = (row + 0.5) * (h / rows);
        pointsRef.current.push({
          x: x + (Math.random() - 0.5) * (w / cols) * 0.5,
          y: y + (Math.random() - 0.5) * (h / rows) * 0.5,
          vx: (Math.random() - 0.5) * 0.3,
          vy: (Math.random() - 0.5) * 0.3,
          radius: Math.random() * 1.5 + 0.5,
          phase: Math.random() * Math.PI * 2,
        });
      }
    };
    resize();
    window.addEventListener("resize", resize);

    const handleMouse = (e: MouseEvent) => {
      if (!enableMouseInteraction) return;
      mouseRef.current.prevX = mouseRef.current.x;
      mouseRef.current.prevY = mouseRef.current.y;
      mouseRef.current.x = e.clientX / w;
      mouseRef.current.y = e.clientY / h;
    };
    window.addEventListener("mousemove", handleMouse);

    const animate = (timestamp: number) => {
      time = timestamp * 0.0003;
      ctx!.clearRect(0, 0, w, h);

      const pts = pointsRef.current;
      const mouse = mouseRef.current;

      for (let i = 0; i < pts.length; i++) {
        const p = pts[i];
        const waveX = Math.sin(time + p.phase) * amplitude * 0.5;
        const waveY = Math.cos(time * 0.7 + p.phase * 1.3) * amplitude * 0.5;

        const dx = (mouse.x - mouse.prevX) * 60;
        const dy = (mouse.y - mouse.prevY) * 60;

        p.x += p.vx + waveX + dx * 0.02;
        p.y += p.vy + waveY + dy * 0.02;

        if (p.x < 0 || p.x > w) p.vx *= -1;
        if (p.y < 0 || p.y > h) p.vy *= -1;
        p.x = Math.max(0, Math.min(w, p.x));
        p.y = Math.max(0, Math.min(h, p.y));
      }

      for (let i = 0; i < pts.length; i++) {
        for (let j = i + 1; j < pts.length; j++) {
          const a = pts[i];
          const b = pts[j];
          const dx = a.x - b.x;
          const dy = a.y - b.y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < CONNECT_DIST) {
            const alpha = (1 - dist / CONNECT_DIST) * 0.25;
            ctx!.beginPath();
            ctx!.moveTo(a.x, a.y);
            ctx!.lineTo(b.x, b.y);
            ctx!.strokeStyle = `rgba(${color[0] * 255}, ${color[1] * 255}, ${color[2] * 255}, ${alpha})`;
            ctx!.lineWidth = 0.6;
            ctx!.stroke();
          }
        }
      }

      for (let i = 0; i < pts.length; i++) {
        const p = pts[i];
        ctx!.beginPath();
        ctx!.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        ctx!.fillStyle = `rgba(${color[0] * 255}, ${color[1] * 255}, ${color[2] * 255}, 0.5)`;
        ctx!.fill();
      }

      animationRef.current = requestAnimationFrame(animate);
    };
    animationRef.current = requestAnimationFrame(animate);

    return () => {
      window.removeEventListener("resize", resize);
      window.removeEventListener("mousemove", handleMouse);
      cancelAnimationFrame(animationRef.current);
    };
  }, [color, amplitude, distance, enableMouseInteraction]);

  return (
    <canvas
      ref={canvasRef}
      className="absolute inset-0 pointer-events-none"
      style={{ opacity: 0.4 }}
    />
  );
});

export default Threads;