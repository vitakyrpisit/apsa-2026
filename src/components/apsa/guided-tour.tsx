"use client";

import { useCallback, useEffect, useState } from "react";
import { ChevronLeft, ChevronRight, X, MapPin, Play } from "lucide-react";
import type { TabHelp } from "./help-drawer";

interface GuidedTourProps {
  open: boolean;
  onClose: () => void;
  helps: TabHelp[];
  onNavigate: (id: string) => void;
}

/**
 * GuidedTour — a sequential spotlight overlay that walks the operator
 * through every tab's help content, one step at a time. Built on the same
 * `TabHelp` data as the HelpDrawer.
 *
 * UX:
 *  - A centered card shows the current step's title, summary, and bullets.
 *  - Prev / Next buttons step through; the progress is shown as "3 / 9".
 *  - Navigating to a tab happens automatically when the step changes so the
 *    user sees the actual tab content behind the spotlight.
 *  - Esc or the X closes the tour.
 */
export function GuidedTour({
  open,
  onClose,
  helps,
  onNavigate,
}: GuidedTourProps) {
  // When open, mount the inner tour component (its initial state is step=0,
  // so no set-state-in-effect is needed to reset). When closed, unmount it.
  if (!open) return null;
  return (
    <GuidedTourInner
      key="tour"
      onClose={onClose}
      helps={helps}
      onNavigate={onNavigate}
    />
  );
}

function GuidedTourInner({
  onClose,
  helps,
  onNavigate,
}: Omit<GuidedTourProps, "open">) {
  const [step, setStep] = useState(0);

  const current = helps[step];
  const isLast = step === helps.length - 1;

  const goNext = useCallback(() => {
    if (isLast) {
      onClose();
      return;
    }
    setStep((s) => Math.min(helps.length - 1, s + 1));
  }, [isLast, helps.length, onClose]);

  const goPrev = useCallback(() => {
    setStep((s) => Math.max(0, s - 1));
  }, []);

  // Navigate to the tab matching the current step. This syncs the parent's
  // active tab (an external system from this component's perspective) with
  // the tour step.
  useEffect(() => {
    if (current) {
      onNavigate(current.id);
    }
  }, [current, onNavigate]);

  // Esc closes; arrow keys navigate.
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
      else if (e.key === "ArrowRight") goNext();
      else if (e.key === "ArrowLeft") goPrev();
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [onClose, goNext, goPrev]);

  if (!current) return null;

  return (
    <div
      className="fixed inset-0 z-[110] flex items-end sm:items-center justify-center p-4 sm:p-6"
      role="dialog"
      aria-modal="true"
      aria-label="Guided tour"
    >
      {/* Backdrop with a vignette */}
      <div
        className="absolute inset-0 bg-gradient-to-b from-black/70 via-black/50 to-black/70 backdrop-blur-[2px]"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Card */}
      <div className="relative w-full max-w-lg rounded-xl border border-emerald-600/40 bg-slate-900 shadow-2xl shadow-emerald-950/40 overflow-hidden">
        {/* Top accent bar */}
        <div className="h-1 bg-gradient-to-r from-emerald-500 via-amber-500 to-rose-500" />

        {/* Header */}
        <div className="flex items-center justify-between px-5 py-3 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <MapPin className="w-4 h-4 text-emerald-400" />
            <span className="text-[10px] font-mono uppercase tracking-wider text-emerald-400">
              Guided Tour · Step {step + 1} of {helps.length}
            </span>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-md text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            aria-label="Close tour"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Progress bar */}
        <div className="h-0.5 bg-slate-800">
          <div
            className="h-full bg-emerald-500 transition-all duration-300"
            style={{ width: `${((step + 1) / helps.length) * 100}%` }}
          />
        </div>

        {/* Content */}
        <div className="px-5 py-5 space-y-4 max-h-[60vh] overflow-y-auto">
          <div>
            <div className="text-xs font-mono text-emerald-400 uppercase tracking-wider mb-1">
              {current.title}
            </div>
            <p className="text-sm text-slate-300 leading-relaxed font-sans">
              {current.summary}
            </p>
          </div>

          <div className="space-y-2">
            <div className="text-[10px] font-mono uppercase tracking-wider text-slate-500">
              Key things to look at here
            </div>
            {current.bullets.map((b, i) => (
              <div
                key={i}
                className="flex items-start gap-2.5 text-xs text-slate-300 font-sans leading-relaxed"
              >
                <span className="w-5 h-5 rounded bg-slate-800 border border-slate-700 text-emerald-400 flex items-center justify-center font-mono font-bold text-[10px] flex-shrink-0 mt-0.5">
                  {i + 1}
                </span>
                <span>{b}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Footer controls */}
        <div className="flex items-center justify-between px-5 py-3 border-t border-slate-800 bg-slate-950/60">
          <button
            onClick={goPrev}
            disabled={step === 0}
            className="px-3 py-1.5 rounded-md text-xs font-mono text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 border border-slate-700 disabled:opacity-40 disabled:cursor-not-allowed flex items-center gap-1.5 transition-colors"
          >
            <ChevronLeft className="w-3.5 h-3.5" />
            Prev
          </button>

          <div className="flex items-center gap-1">
            {helps.map((_, i) => (
              <button
                key={i}
                onClick={() => setStep(i)}
                aria-label={`Go to step ${i + 1}`}
                className={`w-1.5 h-1.5 rounded-full transition-all ${
                  i === step
                    ? "bg-emerald-400 w-4"
                    : i < step
                      ? "bg-emerald-700"
                      : "bg-slate-700 hover:bg-slate-600"
                }`}
              />
            ))}
          </div>

          <button
            onClick={goNext}
            className="px-3 py-1.5 rounded-md text-xs font-mono font-medium text-white bg-emerald-600 hover:bg-emerald-500 flex items-center gap-1.5 transition-colors"
          >
            {isLast ? (
              <>
                <Play className="w-3.5 h-3.5 fill-white" />
                Finish
              </>
            ) : (
              <>
                Next
                <ChevronRight className="w-3.5 h-3.5" />
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
