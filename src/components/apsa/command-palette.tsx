"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Search, CornerDownLeft, ArrowUp, ArrowDown } from "lucide-react";

export interface CommandAction {
  id: string;
  label: string;
  hint?: string;
  group: "Navigate" | "Actions" | "External";
  keywords?: string[];
  run: () => void;
}

interface CommandPaletteProps {
  actions: CommandAction[];
  /** Optional controlled open state. When omitted, the palette manages itself. */
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
}

/**
 * CommandPalette — a Cmd+K / Ctrl+K quick-switcher. Filters the provided
 * actions by label + keywords, supports arrow-key navigation and Enter
 * to execute, Esc to dismiss. Mounted once at the page root.
 */
export function CommandPalette({
  actions,
  open: controlledOpen,
  onOpenChange,
}: CommandPaletteProps) {
  const [internalOpen, setInternalOpen] = useState(false);
  const open = controlledOpen ?? internalOpen;
  const setOpen = (v: boolean) => {
    if (onOpenChange) onOpenChange(v);
    if (controlledOpen === undefined) setInternalOpen(v);
  };
  const [query, setQuery] = useState("");
  const [active, setActive] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);
  const listRef = useRef<HTMLDivElement>(null);

  // Global hotkey (always active; toggles internal state if uncontrolled)
  const handleKeydown = useCallback(
    (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        if (controlledOpen !== undefined) {
          onOpenChange?.(!controlledOpen);
        } else {
          setInternalOpen((o) => !o);
        }
      } else if (e.key === "Escape" && open) {
        setOpen(false);
      }
    },
    [open, controlledOpen, onOpenChange],
  );

  useEffect(() => {
    window.addEventListener("keydown", handleKeydown);
    return () => window.removeEventListener("keydown", handleKeydown);
  }, [handleKeydown]);

  // Focus input on open + reset state
  useEffect(() => {
    if (open) {
      setQuery("");
      setActive(0);
      setTimeout(() => inputRef.current?.focus(), 20);
    }
  }, [open]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return actions;
    return actions.filter((a) => {
      const haystack = [a.label, a.hint ?? "", ...(a.keywords ?? [])]
        .join(" ")
        .toLowerCase();
      return haystack.includes(q);
    });
  }, [actions, query]);

  // Group actions for display, preserving filtered order.
  const grouped = useMemo(() => {
    const groups: Record<string, CommandAction[]> = {};
    for (const a of filtered) {
      (groups[a.group] ??= []).push(a);
    }
    return groups;
  }, [filtered]);

  const flatFiltered = filtered;

  // Keyboard navigation
  const onKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setActive((i) => Math.min(flatFiltered.length - 1, i + 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActive((i) => Math.max(0, i - 1));
    } else if (e.key === "Enter") {
      e.preventDefault();
      const chosen = flatFiltered[active];
      if (chosen) {
        chosen.run();
        setOpen(false);
      }
    }
  };

  // Scroll active item into view
  useEffect(() => {
    const el = listRef.current?.querySelector(
      `[data-cmd-idx="${active}"]`,
    ) as HTMLElement | null;
    el?.scrollIntoView({ block: "nearest" });
  }, [active]);

  if (!open) return null;

  let runningIdx = -1;

  return (
    <div
      className="fixed inset-0 z-[100] flex items-start justify-center pt-[12vh] px-4"
      role="dialog"
      aria-modal="true"
      aria-label="Command palette"
    >
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/70 backdrop-blur-sm"
        onClick={() => setOpen(false)}
        aria-hidden="true"
      />

      {/* Panel */}
      <div className="relative w-full max-w-xl rounded-xl border border-slate-700 bg-slate-900 shadow-2xl shadow-emerald-950/30 overflow-hidden">
        {/* Search input */}
        <div className="flex items-center gap-3 px-4 py-3 border-b border-slate-800">
          <Search className="w-4 h-4 text-slate-400 flex-shrink-0" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setActive(0);
            }}
            onKeyDown={onKeyDown}
            placeholder="Jump to a tab or run an action…"
            className="flex-1 bg-transparent text-sm text-slate-100 placeholder-slate-500 outline-none font-sans"
          />
          <kbd className="hidden sm:flex items-center gap-1 px-1.5 py-0.5 rounded border border-slate-700 bg-slate-950 text-[10px] font-mono text-slate-400">
            esc
          </kbd>
        </div>

        {/* Results */}
        <div ref={listRef} className="max-h-[50vh] overflow-y-auto py-2">
          {flatFiltered.length === 0 && (
            <div className="px-4 py-8 text-center text-sm text-slate-500 font-sans">
              No matching commands for &quot;{query}&quot;
            </div>
          )}
          {Object.entries(grouped).map(([group, items]) => (
            <div key={group} className="mb-1">
              <div className="px-4 py-1.5 text-[10px] font-mono uppercase tracking-wider text-slate-500">
                {group}
              </div>
              {items.map((a) => {
                runningIdx += 1;
                const idx = runningIdx;
                const isActive = idx === active;
                return (
                  <button
                    key={a.id}
                    data-cmd-idx={idx}
                    onMouseEnter={() => setActive(idx)}
                    onClick={() => {
                      a.run();
                      setOpen(false);
                    }}
                    className={`w-full flex items-center justify-between gap-3 px-4 py-2 text-left text-sm transition-colors ${
                      isActive
                        ? "bg-emerald-950/50 text-emerald-100"
                        : "text-slate-300 hover:bg-slate-800/50"
                    }`}
                  >
                    <span className="flex items-center gap-2.5 truncate">
                      <span
                        className={`w-1 h-4 rounded-full ${
                          isActive ? "bg-emerald-400" : "bg-transparent"
                        }`}
                      />
                      <span className="truncate">{a.label}</span>
                    </span>
                    <span className="flex items-center gap-2 text-[10px] font-mono text-slate-500 flex-shrink-0">
                      {a.hint && <span>{a.hint}</span>}
                      {isActive && <CornerDownLeft className="w-3 h-3" />}
                    </span>
                  </button>
                );
              })}
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between px-4 py-2 border-t border-slate-800 text-[10px] font-mono text-slate-500">
          <div className="flex items-center gap-3">
            <span className="flex items-center gap-1">
              <ArrowUp className="w-2.5 h-2.5" />
              <ArrowDown className="w-2.5 h-2.5" /> navigate
            </span>
            <span className="flex items-center gap-1">
              <CornerDownLeft className="w-2.5 h-2.5" /> select
            </span>
          </div>
          <span>{flatFiltered.length} commands</span>
        </div>
      </div>
    </div>
  );
}
