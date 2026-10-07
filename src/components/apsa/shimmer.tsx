"use client";

import { cn } from "@/lib/utils";

/**
 * Skeleton shimmer block — used as a loading placeholder for async data.
 * Uses the project's emerald accent so it reads as "live/loading" rather
 * than a dead grey box.
 */
export function Shimmer({ className }: { className?: string }) {
  return (
    <div
      className={cn(
        "relative overflow-hidden rounded bg-slate-800/60",
        className,
      )}
      aria-hidden="true"
    >
      <div className="absolute inset-0 -translate-x-full animate-[shimmer_1.6s_infinite] bg-gradient-to-r from-transparent via-emerald-400/10 to-transparent" />
    </div>
  );
}
