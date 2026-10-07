"use client";

import { useEffect, useRef, useState } from "react";

/**
 * useCountUp — animates a numeric value from its previous rendered value
 * to the next target using requestAnimationFrame with an ease-out curve.
 * Returns the current animated value.
 */
export function useCountUp(target: number, durationMs = 800): number {
  const [display, setDisplay] = useState(target);
  const fromRef = useRef(target);
  const rafRef = useRef<number | null>(null);
  const startRef = useRef<number | null>(null);

  useEffect(() => {
    const from = fromRef.current;
    const to = target;
    if (from === to) return;
    startRef.current = null;

    const tick = (now: number) => {
      if (startRef.current === null) startRef.current = now;
      const elapsed = now - startRef.current;
      const t = Math.min(1, elapsed / durationMs);
      // ease-out cubic
      const eased = 1 - Math.pow(1 - t, 3);
      const next = from + (to - from) * eased;
      setDisplay(next);
      if (t < 1) {
        rafRef.current = requestAnimationFrame(tick);
      } else {
        fromRef.current = to;
        setDisplay(to);
      }
    };

    rafRef.current = requestAnimationFrame(tick);
    return () => {
      if (rafRef.current !== null) cancelAnimationFrame(rafRef.current);
      fromRef.current = target;
    };
  }, [target, durationMs]);

  return display;
}

interface AnimatedNumberProps {
  value: number;
  decimals?: number;
  prefix?: string;
  suffix?: string;
  durationMs?: number;
  className?: string;
}

/** AnimatedNumber — renders an animating numeric value with optional prefix/suffix. */
export function AnimatedNumber({
  value,
  decimals = 2,
  prefix = "",
  suffix = "",
  durationMs = 800,
  className,
}: AnimatedNumberProps) {
  const animated = useCountUp(value, durationMs);
  const formatted = animated.toLocaleString("en-US", {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
  return (
    <span className={className}>
      {prefix}
      {formatted}
      {suffix}
    </span>
  );
}
