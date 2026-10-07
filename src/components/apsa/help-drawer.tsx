"use client";

import { useEffect, useState } from "react";
import { HelpCircle, X, ChevronRight } from "lucide-react";

export interface TabHelp {
  id: string;
  title: string;
  summary: string;
  bullets: string[];
}

interface HelpDrawerProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  helps: TabHelp[];
  activeTabId: string;
  onNavigate: (id: string) => void;
}

/**
 * HelpDrawer — a right-side slide-in panel that explains what each tab is
 * for, aimed at reducing the "information density" accessibility concern
 * flagged by VLM in round 1. Activated by a "?" button or the `?` / `Shift+/`
 * hotkey, plus a per-tab "What am I looking at?" affordance.
 *
 * The `visitedHelpId` is the user's selected help entry (defaults to the
 * active tab when first opened, then tracks the user's clicks inside the
 * drawer). It is only updated in event handlers, never in effects.
 */
export function HelpDrawer({
  open,
  onOpenChange,
  helps,
  activeTabId,
  onNavigate,
}: HelpDrawerProps) {
  const [visitedHelpId, setVisitedHelpId] = useState<string | null>(null);

  // Reset the visited selection whenever the drawer closes so the next open
  // re-syncs to the active tab.
  useEffect(() => {
    if (!open) {
      // use a microtask to avoid setState during render close-cycle
      const id = setTimeout(() => setVisitedHelpId(null), 0);
      return () => clearTimeout(id);
    }
    return;
  }, [open]);

  // Esc closes (in addition to the page-level handler)
  useEffect(() => {
    if (!open) return;
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") onOpenChange(false);
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [open, onOpenChange]);

  const activeHelpId = visitedHelpId ?? activeTabId;
  const active = helps.find((h) => h.id === activeHelpId) ?? helps[0];

  return (
    <>
      {/* Backdrop */}
      {open && (
        <div
          className="fixed inset-0 z-[90] bg-black/60 backdrop-blur-sm transition-opacity"
          onClick={() => onOpenChange(false)}
          aria-hidden="true"
        />
      )}

      {/* Drawer */}
      <aside
        className={`fixed top-0 right-0 z-[95] h-full w-full max-w-md bg-slate-900 border-l border-slate-700 shadow-2xl transition-transform duration-300 ease-out flex flex-col ${
          open ? "translate-x-0" : "translate-x-full"
        }`}
        role="dialog"
        aria-modal="true"
        aria-label="Tab help & guided tour"
      >
        {/* Header */}
        <div className="flex items-center justify-between px-5 py-4 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <HelpCircle className="w-4 h-4 text-emerald-400" />
            <h2 className="text-sm font-bold text-white uppercase tracking-wider font-mono">
              What am I looking at?
            </h2>
          </div>
          <button
            onClick={() => onOpenChange(false)}
            className="p-1.5 rounded-md text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            aria-label="Close help drawer"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Tab list */}
        <nav className="px-3 py-3 border-b border-slate-800 overflow-y-auto max-h-[30vh]">
          <ul className="space-y-1">
            {helps.map((h) => (
              <li key={h.id}>
                <button
                  onClick={() => setVisitedHelpId(h.id)}
                  className={`w-full flex items-center justify-between gap-2 px-3 py-2 rounded-lg text-left text-sm transition-colors ${
                    activeHelpId === h.id
                      ? "bg-emerald-950/60 text-emerald-100 border border-emerald-700/40"
                      : "text-slate-300 hover:bg-slate-800/60 border border-transparent"
                  }`}
                >
                  <span className="truncate font-medium">{h.title}</span>
                  {activeHelpId === h.id && (
                    <ChevronRight className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0" />
                  )}
                </button>
              </li>
            ))}
          </ul>
        </nav>

        {/* Active help content */}
        <div className="flex-1 overflow-y-auto px-5 py-5 space-y-4">
          {active && (
            <>
              <div>
                <div className="text-[10px] font-mono uppercase tracking-wider text-emerald-400 mb-1">
                  {active.title}
                </div>
                <p className="text-sm text-slate-300 leading-relaxed font-sans">
                  {active.summary}
                </p>
              </div>

              <div className="space-y-2">
                <div className="text-[10px] font-mono uppercase tracking-wider text-slate-500">
                  Key things to look at here
                </div>
                {active.bullets.map((b, i) => (
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
            </>
          )}
        </div>

        {/* Footer */}
        <div className="px-5 py-4 border-t border-slate-800 flex items-center justify-between gap-3">
          <span className="text-[10px] font-mono text-slate-500">
            Press <kbd className="px-1 py-0.5 rounded border border-slate-700 bg-slate-950">Esc</kbd> to close
          </span>
          <button
            onClick={() => {
              onNavigate(activeHelpId);
              onOpenChange(false);
            }}
            className="px-3 py-1.5 rounded-md bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-mono font-medium flex items-center gap-1.5 transition-colors"
          >
            Go to this tab
            <ChevronRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </aside>
    </>
  );
}
