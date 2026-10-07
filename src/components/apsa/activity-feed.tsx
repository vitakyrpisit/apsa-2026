"use client";

import { useEffect, useState } from "react";
import {
  Bell,
  X,
  CheckCheck,
  Trash2,
  Activity as ActivityIcon,
  ShieldCheck,
  Coins,
  Terminal,
  Search,
  Network,
  MousePointerClick,
  Sparkles,
  RotateCcw,
  MapPin,
} from "lucide-react";
import {
  useActivityFeed,
  formatRelativeTime,
  type ActivityEvent,
  type ActivityEventType,
} from "./activity-feed-provider";

interface ActivityFeedProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

const EVENT_ICONS: Record<ActivityEventType, React.ComponentType<{ className?: string }>> = {
  "suite-run": ShieldCheck,
  "wallet-scan": Coins,
  "x402-simulation": Terminal,
  "tx-verify": Search,
  "network-toggle": Network,
  "tab-change": MousePointerClick,
  "scenario-load": Sparkles,
  "scenario-reset": RotateCcw,
  "tour-start": MapPin,
  "tour-complete": CheckCheck,
};

const TONE_TEXT: Record<ActivityEvent["tone"], string> = {
  emerald: "text-emerald-400",
  amber: "text-amber-400",
  rose: "text-rose-400",
  slate: "text-slate-300",
  violet: "text-violet-400",
};

const TONE_BG: Record<ActivityEvent["tone"], string> = {
  emerald: "bg-emerald-950/60 border-emerald-800/40",
  amber: "bg-amber-950/40 border-amber-800/40",
  rose: "bg-rose-950/40 border-rose-800/40",
  slate: "bg-slate-950/60 border-slate-800/60",
  violet: "bg-violet-950/40 border-violet-800/40",
};

/**
 * ActivityFeed — a right-side slide-out panel showing recent protocol events
 * (test-suite runs, wallet scans, x402 simulations, tx verifications, tab
 * changes, etc.). Reads from the ActivityFeedProvider context. Shows an
 * unread-count badge; "Mark all read" resets it. "Clear" empties the feed.
 */
export function ActivityFeed({ open, onOpenChange }: ActivityFeedProps) {
  const { events, unreadCount, markAllRead, clear } = useActivityFeed();
  const [, setTick] = useState(0);
  const [filter, setFilter] = useState<ActivityEventType | "all">("all");

  const filteredEvents =
    filter === "all" ? events : events.filter((e) => e.type === filter);

  // Re-render every 5s so the relative timestamps ("Xs ago") stay fresh
  // while the panel is open.
  useEffect(() => {
    if (!open) return;
    const id = setInterval(() => setTick((t) => t + 1), 5000);
    return () => clearInterval(id);
  }, [open]);

  // Esc closes.
  useEffect(() => {
    if (!open) return;
    const handler = (e: KeyboardEvent) => {
      if (e.key === "Escape") onOpenChange(false);
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [open, onOpenChange]);

  return (
    <>
      {/* Backdrop */}
      {open && (
        <div
          className="fixed inset-0 z-[95] bg-black/60 backdrop-blur-sm"
          onClick={() => onOpenChange(false)}
          aria-hidden="true"
        />
      )}

      <aside
        className={`fixed top-0 right-0 z-[96] h-full w-full max-w-md bg-slate-900 border-l border-slate-700 shadow-2xl transition-transform duration-300 ease-out flex flex-col ${
          open ? "translate-x-0" : "translate-x-full"
        }`}
        role="dialog"
        aria-modal="true"
        aria-label="Activity feed"
      >
        {/* Header */}
        <div className="flex items-center justify-between px-5 py-4 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <div className="relative">
              <Bell className="w-4 h-4 text-emerald-400" />
              {unreadCount > 0 && (
                <span className="absolute -top-1.5 -right-1.5 min-w-[14px] h-3.5 px-1 rounded-full bg-rose-500 text-white text-[8px] font-bold flex items-center justify-center apsa-badge-pulse">
                  {unreadCount > 9 ? "9+" : unreadCount}
                </span>
              )}
            </div>
            <h2 className="text-sm font-bold text-white uppercase tracking-wider font-mono">
              Activity Feed
            </h2>
            {unreadCount > 0 && (
              <span className="text-[10px] font-mono text-slate-500">
                {unreadCount} unread
              </span>
            )}
          </div>
          <button
            onClick={() => onOpenChange(false)}
            className="p-1.5 rounded-md text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            aria-label="Close activity feed"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Action bar */}
        <div className="flex items-center gap-2 px-5 py-2 border-b border-slate-800 bg-slate-950/60">
          <button
            onClick={markAllRead}
            disabled={unreadCount === 0}
            className="px-2.5 py-1 text-[11px] font-mono rounded-md bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700 disabled:opacity-40 disabled:cursor-not-allowed flex items-center gap-1.5 transition-colors"
          >
            <CheckCheck className="w-3 h-3" />
            Mark all read
          </button>
          <button
            onClick={clear}
            disabled={events.length === 0}
            className="px-2.5 py-1 text-[11px] font-mono rounded-md bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700 disabled:opacity-40 disabled:cursor-not-allowed flex items-center gap-1.5 transition-colors"
          >
            <Trash2 className="w-3 h-3" />
            Clear
          </button>
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value as ActivityEventType | "all")}
            className="ml-auto px-2 py-1 text-[11px] font-mono rounded-md bg-slate-950 border border-slate-800 text-slate-300 focus:outline-none focus:border-emerald-500 cursor-pointer"
            aria-label="Filter events by type"
          >
            <option value="all">All types ({events.length})</option>
            <option value="suite-run">Suite runs</option>
            <option value="wallet-scan">Wallet scans</option>
            <option value="x402-simulation">x402 simulations</option>
            <option value="tx-verify">Tx verifications</option>
            <option value="tab-change">Tab switches</option>
            <option value="network-toggle">Network toggles</option>
            <option value="tour-start">Tour events</option>
          </select>
        </div>

        {/* Event list */}
        <div className="flex-1 overflow-y-auto px-3 py-3 space-y-1.5">
          {filteredEvents.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center gap-3 text-slate-500">
              <ActivityIcon className="w-8 h-8 opacity-40" />
              <div>
                <div className="text-sm font-mono text-slate-400">
                  {events.length === 0 ? "No activity yet" : "No events match this filter"}
                </div>
                <div className="text-[11px] text-slate-600 mt-1">
                  {events.length === 0
                    ? "Protocol events (test runs, scans, simulations) will appear here."
                    : `Try a different filter — ${events.length} total event${events.length === 1 ? "" : "s"} in the feed.`}
                </div>
              </div>
            </div>
          ) : (
            filteredEvents.map((evt) => {
              const Icon = EVENT_ICONS[evt.type] ?? ActivityIcon;
              return (
                <div
                  key={evt.id}
                  className={`p-3 rounded-lg border ${TONE_BG[evt.tone]} transition-colors hover:border-slate-600`}
                >
                  <div className="flex items-start gap-2.5">
                    <div className={`flex-shrink-0 mt-0.5 ${TONE_TEXT[evt.tone]}`}>
                      <Icon className="w-3.5 h-3.5" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between gap-2 mb-0.5">
                        <span className={`text-xs font-mono font-semibold ${TONE_TEXT[evt.tone]} truncate`}>
                          {evt.title}
                        </span>
                        <span className="text-[10px] font-mono text-slate-500 flex-shrink-0">
                          {formatRelativeTime(evt.timestamp)}
                        </span>
                      </div>
                      {evt.detail && (
                        <p className="text-[11px] text-slate-400 font-sans leading-relaxed break-words">
                          {evt.detail}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Footer */}
        <div className="px-5 py-3 border-t border-slate-800 text-[10px] font-mono text-slate-500 flex items-center justify-between">
          <span>
            Press <kbd className="px-1 py-0.5 rounded border border-slate-700 bg-slate-950">Esc</kbd> to close
          </span>
          <span>
            {filter === "all"
              ? `${filteredEvents.length} event${filteredEvents.length === 1 ? "" : "s"}`
              : `${filteredEvents.length}/${events.length} event${filteredEvents.length === 1 ? "" : "s"}`}
            {" · "}session-scoped · max 50
          </span>
        </div>
      </aside>
    </>
  );
}
