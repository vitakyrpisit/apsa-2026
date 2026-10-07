"use client";

import {
  createContext,
  useCallback,
  useContext,
  useRef,
  useState,
  type ReactNode,
} from "react";

export type ActivityEventType =
  | "suite-run"
  | "wallet-scan"
  | "x402-simulation"
  | "tx-verify"
  | "network-toggle"
  | "tab-change"
  | "scenario-load"
  | "scenario-reset"
  | "tour-start"
  | "tour-complete";

export interface ActivityEvent {
  id: string;
  type: ActivityEventType;
  timestamp: number;
  title: string;
  detail?: string;
  tone: "emerald" | "amber" | "rose" | "slate" | "violet";
}

interface ActivityFeedContextValue {
  events: ActivityEvent[];
  unreadCount: number;
  logEvent: (type: ActivityEventType, title: string, detail?: string, tone?: ActivityEvent["tone"]) => void;
  markAllRead: () => void;
  clear: () => void;
}

const ActivityFeedContext = createContext<ActivityFeedContextValue | null>(null);

const MAX_EVENTS = 50;

/**
 * ActivityFeedProvider — an in-memory ring buffer of recent protocol events.
 * Tracks test-suite runs, wallet scans, x402 simulations, tx verifications,
 * tab changes, and more. Events are capped at MAX_EVENTS (50) so memory is
 * bounded. Unread count resets on `markAllRead()`.
 *
 * Does NOT persist to localStorage — events are session-scoped. This keeps
 * the feed fresh and avoids stale cross-session noise.
 */
export function ActivityFeedProvider({ children }: { children: ReactNode }) {
  const [events, setEvents] = useState<ActivityEvent[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const counterRef = useRef(0);

  const logEvent = useCallback(
    (
      type: ActivityEventType,
      title: string,
      detail?: string,
      tone: ActivityEvent["tone"] = "slate",
    ) => {
      counterRef.current += 1;
      const event: ActivityEvent = {
        id: `evt-${counterRef.current}-${Date.now()}`,
        type,
        timestamp: Date.now(),
        title,
        detail,
        tone,
      };
      setEvents((prev) => [event, ...prev].slice(0, MAX_EVENTS));
      setUnreadCount((c) => Math.min(MAX_EVENTS, c + 1));
    },
    [],
  );

  const markAllRead = useCallback(() => setUnreadCount(0), []);
  const clear = useCallback(() => {
    setEvents([]);
    setUnreadCount(0);
  }, []);

  const value: ActivityFeedContextValue = {
    events,
    unreadCount,
    logEvent,
    markAllRead,
    clear,
  };

  return (
    <ActivityFeedContext.Provider value={value}>
      {children}
    </ActivityFeedContext.Provider>
  );
}

export function useActivityFeed(): ActivityFeedContextValue {
  const ctx = useContext(ActivityFeedContext);
  if (!ctx) {
    throw new Error("useActivityFeed must be used within an ActivityFeedProvider");
  }
  return ctx;
}

/** Format a timestamp as a relative "Xs ago" / "Xm ago" string. */
export function formatRelativeTime(ts: number): string {
  const seconds = Math.floor((Date.now() - ts) / 1000);
  if (seconds < 5) return "just now";
  if (seconds < 60) return `${seconds}s ago`;
  const minutes = Math.floor(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  return `${Math.floor(hours / 24)}d ago`;
}
