"use client";

import { useEffect } from "react";
import { Keyboard, X, ArrowUp, ArrowDown, CornerDownLeft } from "lucide-react";

interface KeyboardShortcutsOverlayProps {
  open: boolean;
  onClose: () => void;
}

interface Shortcut {
  keys: string;
  description: string;
  group: "Navigation" | "Actions" | "Overlays";
}

const SHORTCUTS: Shortcut[] = [
  { keys: "1 – 9", description: "Jump to tab 1-9 (Mission → Scanner)", group: "Navigation" },
  { keys: "←  →", description: "Guided Tour: previous / next step (while tour is open)", group: "Navigation" },
  { keys: "⌘ K  /  Ctrl K", description: "Open the Command Palette", group: "Overlays" },
  { keys: "?", description: "Toggle the Help Drawer (per-tab explanations)", group: "Overlays" },
  { keys: "b", description: "Toggle the Activity Feed (recent protocol events)", group: "Overlays" },
  { keys: "g", description: "Start the Guided Tour", group: "Overlays" },
  { keys: "h", description: "Show this keyboard-shortcuts cheat sheet", group: "Overlays" },
  { keys: "Esc", description: "Close any open overlay / panel / tour", group: "Actions" },
  { keys: "Enter", description: "Command Palette: execute the highlighted action", group: "Actions" },
];

/**
 * KeyboardShortcutsOverlay — a centered modal showing all available keyboard
 * shortcuts, grouped by category. Activated by pressing `h`. Esc closes.
 */
export function KeyboardShortcutsOverlay({
  open,
  onClose,
}: KeyboardShortcutsOverlayProps) {
  // Esc closes.
  useEffect(() => {
    if (!open) return;
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [open, onClose]);

  if (!open) return null;

  const groups = ["Navigation", "Overlays", "Actions"] as const;

  return (
    <div
      className="fixed inset-0 z-[120] flex items-center justify-center p-4"
      role="dialog"
      aria-modal="true"
      aria-label="Keyboard shortcuts cheat sheet"
    >
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/70 backdrop-blur-sm"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Panel */}
      <div className="relative w-full max-w-lg rounded-xl border border-slate-700 bg-slate-900 shadow-2xl shadow-emerald-950/30 overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-5 py-4 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <Keyboard className="w-4 h-4 text-emerald-400" />
            <h2 className="text-sm font-bold text-white uppercase tracking-wider font-mono">
              Keyboard Shortcuts
            </h2>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-md text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            aria-label="Close shortcuts overlay"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Shortcut groups */}
        <div className="px-5 py-4 space-y-5 max-h-[60vh] overflow-y-auto">
          {groups.map((group) => {
            const items = SHORTCUTS.filter((s) => s.group === group);
            if (items.length === 0) return null;
            return (
              <div key={group}>
                <div className="text-[10px] font-mono uppercase tracking-wider text-slate-500 mb-2">
                  {group}
                </div>
                <div className="space-y-1.5">
                  {items.map((s, i) => (
                    <div
                      key={i}
                      className="flex items-center justify-between gap-3 py-1"
                    >
                      <span className="text-xs text-slate-300 font-sans">
                        {s.description}
                      </span>
                      <kbd className="px-2 py-0.5 rounded border border-slate-700 bg-slate-950 text-[10px] font-mono text-emerald-300 whitespace-nowrap">
                        {s.keys}
                      </kbd>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>

        {/* Footer */}
        <div className="px-5 py-3 border-t border-slate-800 text-[10px] font-mono text-slate-500 flex items-center justify-between">
          <span>
            Press <kbd className="px-1 py-0.5 rounded border border-slate-700 bg-slate-950">Esc</kbd> to close
          </span>
          <span className="flex items-center gap-1">
            <ArrowUp className="w-2.5 h-2.5" />
            <ArrowDown className="w-2.5 h-2.5" />
            <CornerDownLeft className="w-2.5 h-2.5" />
            <span className="ml-1">available</span>
          </span>
        </div>
      </div>
    </div>
  );
}
