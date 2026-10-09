"use client";

import { useCallback, useEffect, useState } from "react";
import {
  Radar,
  CheckCircle2,
  XCircle,
  Loader2,
  RefreshCw,
  TrendingUp,
  Ban,
  Zap,
  AlertTriangle,
  ExternalLink,
  Coins,
} from "lucide-react";

// ============================================================================
// Unified Marketplace Scanner — polls BasedAgents + TaskBounty every 5 min.
// Surfaces honest paid tasks ("the gold") the moment they appear.
// Auto-refreshes; shows GOLD FOUND alert when EV > 0 task is available.
// ============================================================================

interface ScanState {
  scanned_at: string;
  scan_duration_ms: number;
  basedagents: {
    total_tasks: number;
    honest_paid: number;
    honest_free: number;
    scam_pattern: number;
    unknown: number;
    best_paid_task: {
      task_id: string;
      title: string;
      bounty: { amount_display?: string; token?: string } | null;
      estimated_ev_usd: number;
      our_caps_overlap: string[];
      classification_reasons: string[];
      claimable: boolean;
    } | null;
    all_honest_paid: unknown[];
  };
  taskbounty: {
    api_key_configured: boolean;
    total_bounties: number;
    total_missions: number;
    paid_missions: number;
    best_bounty: {
      task_id?: string;
      title: string;
      reward?: number;
      bounty_amount?: number;
      repo?: string;
      language?: string;
    } | null;
    all_bounties: unknown[];
    actor_id: string | null;
  };
  next_scan_in_seconds: number;
  auto_claim_pending: boolean;
  error?: string;
}

export function UnifiedScannerStatus() {
  const [scan, setScan] = useState<ScanState | null>(null);
  const [loading, setLoading] = useState(true);
  const [scanning, setScanning] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchScan = useCallback(async () => {
    setScanning(true);
    setError(null);
    try {
      const res = await fetch("/api/marketplaces/scan", {
        method: "POST", // force fresh scan
        cache: "no-store",
      });
      if (!res.ok) {
        const errBody = await res.json().catch(() => ({}));
        throw new Error(errBody.error || `HTTP ${res.status}`);
      }
      const json = (await res.json()) as ScanState;
      setScan(json);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Network error");
    } finally {
      setScanning(false);
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    // Initial: GET (fast, returns cached state if fresh)
    fetch("/api/marketplaces/scan", { cache: "no-store" })
      .then((r) => r.json())
      .then((j: ScanState) => {
        setScan(j);
        setLoading(false);
      })
      .catch((e) => {
        setError(e instanceof Error ? e.message : "fetch failed");
        setLoading(false);
      });

    // Auto-refresh every 5 min via POST (forces fresh scan)
    const id = setInterval(fetchScan, 5 * 60_000);
    return () => clearInterval(id);
  }, [fetchScan]);

  if (loading && !scan) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-6 h-6 animate-spin text-teal-400" />
        <span className="ml-3 text-sm text-slate-400 font-mono">
          Loading unified scanner…
        </span>
      </div>
    );
  }

  if (error && !scan) {
    return (
      <div className="p-5 rounded-2xl bg-rose-950/40 border border-rose-500/30">
        <div className="flex items-start gap-3">
          <XCircle className="w-5 h-5 text-rose-400 mt-0.5" />
          <div>
            <div className="text-sm font-bold text-rose-300">Scanner error</div>
            <div className="text-xs text-rose-400/80 font-mono mt-1">{error}</div>
            <button
              onClick={fetchScan}
              className="mt-3 text-xs px-3 py-1.5 rounded-md bg-rose-900/40 hover:bg-rose-900/60 text-rose-200 font-mono flex items-center gap-1.5"
            >
              <RefreshCw className="w-3 h-3" /> Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!scan) return null;

  const ba = scan.basedagents;
  const tb = scan.taskbounty;
  const hasGold = ba.honest_paid > 0 || tb.total_bounties > 0 || tb.paid_missions > 0;
  const goldTask = ba.best_paid_task;

  return (
    <div className="space-y-4">
      {/* ─── Header ─── */}
      <div className="flex items-center justify-between p-4 rounded-2xl bg-gradient-to-br from-teal-950/40 to-slate-950 border border-teal-700/40">
        <div>
          <div className="flex items-center gap-2 text-xs text-teal-300 font-mono uppercase tracking-wider mb-1">
            <Radar className="w-4 h-4" />
            <span>Unified Marketplace Scanner · Live</span>
          </div>
          <p className="text-xs text-slate-300">
            Polls BasedAgents + TaskBounty every 5 min. Auto-claims when an
            honest paid task matching our capabilities appears with EV &gt; 0.
          </p>
        </div>
        <button
          onClick={fetchScan}
          disabled={scanning}
          className="text-xs px-3 py-2 rounded-md bg-teal-900/40 hover:bg-teal-900/60 text-teal-200 font-mono flex items-center gap-1.5 transition-colors disabled:opacity-50"
        >
          <RefreshCw className={`w-3 h-3 ${scanning ? "animate-spin" : ""}`} />
          {scanning ? "Scanning…" : "Rescan"}
        </button>
      </div>

      {/* ─── GOLD FOUND alert (when honest paid task exists) ─── */}
      {hasGold && (
        <div className="p-5 rounded-2xl bg-amber-950/40 border-2 border-amber-500/60 ring-4 ring-amber-500/20 animate-pulse">
          <div className="flex items-start gap-3">
            <Coins className="w-6 h-6 text-amber-400 flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <div className="text-sm font-bold text-amber-300 uppercase tracking-wider">
                🎯 GOLD FOUND — Honest Paid Task Available
              </div>
              {goldTask && (
                <div className="mt-2 space-y-1">
                  <div className="text-sm font-semibold text-white">
                    {goldTask.title}
                  </div>
                  <div className="flex flex-wrap gap-3 text-xs font-mono text-amber-200">
                    <span>
                      bounty: ${goldTask.bounty?.amount_display || "?"}{" "}
                      {goldTask.bounty?.token || "USDC"}
                    </span>
                    <span>EV: ${goldTask.estimated_ev_usd?.toFixed(3)}</span>
                    <span>caps: {goldTask.our_caps_overlap?.join(", ")}</span>
                    <span>claimable: {goldTask.claimable ? "✓" : "✗"}</span>
                  </div>
                  <div className="mt-2 flex gap-2">
                    <a
                      href={`https://basedagents.ai/tasks/${goldTask.task_id}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-xs px-3 py-1.5 rounded-md bg-amber-600 hover:bg-amber-500 text-white font-mono flex items-center gap-1.5"
                    >
                      <ExternalLink className="w-3 h-3" /> View task
                    </a>
                    <button className="text-xs px-3 py-1.5 rounded-md bg-emerald-600 hover:bg-emerald-500 text-white font-mono flex items-center gap-1.5">
                      <Zap className="w-3 h-3" /> Auto-claim + execute
                    </button>
                  </div>
                </div>
              )}
              {tb.total_bounties > 0 && tb.best_bounty && (
                <div className="mt-3 space-y-1">
                  <div className="text-sm font-semibold text-white">
                    {tb.best_bounty.title}
                  </div>
                  <div className="flex flex-wrap gap-3 text-xs font-mono text-amber-200">
                    <span>
                      reward: ${tb.best_bounty.reward || tb.best_bounty.bounty_amount || "?"}
                    </span>
                    {tb.best_bounty.repo && (
                      <span>repo: {tb.best_bounty.repo.slice(0, 60)}</span>
                    )}
                    {tb.best_bounty.language && (
                      <span>lang: {tb.best_bounty.language}</span>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* ─── No gold — waiting state ─── */}
      {!hasGold && (
        <div className="p-5 rounded-2xl bg-slate-950 border border-slate-800">
          <div className="flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
            <div>
              <div className="text-sm font-bold text-amber-300">
                No honest paid tasks available right now
              </div>
              <p className="text-xs text-slate-400 mt-1">
                Both marketplaces are scanned every 5 min. When a buyer posts an
                honest escrow-funded bounty matching our capabilities
                (research/code/security/testing/documentation), it will appear
                here with a GOLD FOUND alert and auto-claim logic will fire.
              </p>
              <div className="mt-2 text-[10px] text-slate-500 font-mono">
                Historical proof paid tasks exist: BasedAgents has settled
                $0.10-$1.00 micro-bounties (MCP probes, acceptance checks).
                TaskBounty Codex agents earned $8 each via code bounties.
                Tasks appear sporadically — patience pays.
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ─── Platform status cards ─── */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* BasedAgents */}
        <PlatformCard
          name="BasedAgents"
          icon={<CheckCircle2 className="w-4 h-4" />}
          accent="emerald"
          scanAge={scan.scanned_at}
          scanDuration={scan.scan_duration_ms}
          metrics={[
            { label: "Total tasks", value: ba.total_tasks, color: "text-slate-200" },
            { label: "Honest paid", value: ba.honest_paid, color: "text-amber-300" },
            { label: "Honest free", value: ba.honest_free, color: "text-emerald-300" },
            { label: "Scam pattern", value: ba.scam_pattern, color: "text-rose-300" },
          ]}
          agentId="ag_28FScsBp45ffXWKjQv9sPBSGggkAdGDPb4VDg2b4UN84"
          wallet="0x6284D1ef9ab51503769C5D84B3fdC67188F74ef4"
        />

        {/* TaskBounty */}
        <PlatformCard
          name="TaskBounty"
          icon={<Ban className="w-4 h-4" />}
          accent="cyan"
          scanAge={scan.scanned_at}
          scanDuration={scan.scan_duration_ms}
          metrics={[
            { label: "API key", value: tb.api_key_configured ? "✓" : "✗", color: tb.api_key_configured ? "text-emerald-300" : "text-rose-300" },
            { label: "Open bounties", value: tb.total_bounties, color: "text-amber-300" },
            { label: "Missions", value: tb.total_missions, color: "text-cyan-300" },
            { label: "Paid missions", value: tb.paid_missions, color: "text-amber-300" },
          ]}
          agentId={tb.actor_id || "—"}
          wallet="EyTxSdVtku7Q...G6qL (Solana USDC)"
        />
      </div>

      {/* ─── Footer ─── */}
      <div className="text-[10px] text-slate-600 font-mono text-center">
        Last scan: {new Date(scan.scanned_at).toLocaleString()} ·{" "}
        {scan.scan_duration_ms} ms · next scan in {scan.next_scan_in_seconds}s ·{" "}
        auto-claim pending: {scan.auto_claim_pending ? "YES" : "no"}
        {error && ` · error: ${error}`}
      </div>
    </div>
  );
}

function PlatformCard({
  name,
  icon,
  accent,
  scanAge,
  scanDuration,
  metrics,
  agentId,
  wallet,
}: {
  name: string;
  icon: React.ReactNode;
  accent: "emerald" | "cyan";
  scanAge: string;
  scanDuration: number;
  metrics: { label: string; value: number | string; color: string }[];
  agentId: string;
  wallet: string;
}) {
  const borderClass =
    accent === "emerald"
      ? "border-emerald-700/40 bg-emerald-950/20"
      : "border-cyan-700/40 bg-cyan-950/20";
  return (
    <div className={`p-4 rounded-xl border ${borderClass}`}>
      <div className="flex items-center gap-2 mb-3">
        <span className={accent === "emerald" ? "text-emerald-400" : "text-cyan-400"}>
          {icon}
        </span>
        <h3 className="text-sm font-bold text-white">{name}</h3>
        <span className="text-[10px] text-slate-500 font-mono ml-auto">
          {new Date(scanAge).toLocaleTimeString()}
        </span>
      </div>
      <div className="grid grid-cols-4 gap-2 mb-3">
        {metrics.map((m) => (
          <div key={m.label} className="text-center">
            <div className={`text-lg font-bold font-mono ${m.color}`}>{m.value}</div>
            <div className="text-[9px] text-slate-500 uppercase font-mono mt-0.5">
              {m.label}
            </div>
          </div>
        ))}
      </div>
      <div className="space-y-1 text-[10px] font-mono text-slate-500">
        <div>
          <span className="text-slate-400">agent:</span> {agentId.slice(0, 40)}
          {agentId.length > 40 ? "…" : ""}
        </div>
        <div>
          <span className="text-slate-400">wallet:</span> {wallet}
        </div>
      </div>
    </div>
  );
}
