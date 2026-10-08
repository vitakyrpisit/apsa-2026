"use client";

import { useCallback, useEffect, useState } from "react";
import {
  Store,
  ShieldCheck,
  AlertTriangle,
  ExternalLink,
  Wallet,
  Activity,
  Users,
  CheckCircle2,
  XCircle,
  Loader2,
  RefreshCw,
  Copy,
  Eye,
  EyeOff,
  TrendingUp,
  Ban,
  Zap,
} from "lucide-react";

// ============================================================================
// /api/basedagents/status — aggregated live data from BasedAgents registry.
// Signed with our Ed25519 keypair on the server. Private key never leaves server.
// ============================================================================

interface AgentData {
  agent_id: string;
  name: string;
  profile_url: string;
  status: string;
  capabilities: string[];
  registered_at: string;
  reputation_score: number;
  verification_count: number;
  ratings: { count: number; average: number | null };
}

interface WalletData {
  address: string;
  network: string;
  verified: boolean;
  verified_at?: string;
  note: string;
  current_balance_usdc: number | null;
}

interface ClaimBudget {
  budget: number | null;
  bonded_slots: number;
  bond_capacity: number;
  bond_required_per_bounty_slot_usdc: number;
  signed_endpoint_works: boolean;
  error?: string;
  http_status?: number;
}

interface RegistryData {
  agents_total: number | null;
  tasks_open: number | null;
  tasks_paid: number | null;
  paid_usdc_total: string | null;
  payments: string | null;
  escrow: string | null;
}

interface OpenTasks {
  total_visible: number;
  honest_count: number;
  scam_pattern_count: number;
  paid_scam_count: number;
  matching_our_capabilities: number;
  matching_task_ids: string[];
}

interface ScamAlert {
  pattern: string;
  creator_agents: string[];
  red_flags: string[];
  recommendation: string;
}

interface ProfileHistoryItem {
  agent_id: string;
  name: string;
  status: string;
  reason: string;
  lesson: string;
}

interface BasedAgentsStatus {
  ok: boolean;
  agent: AgentData;
  wallet: WalletData;
  claim_budget: ClaimBudget;
  registry: RegistryData;
  open_tasks: OpenTasks;
  scam_alert: ScamAlert;
  profile_history: ProfileHistoryItem[];
  fetched_at: string;
  fetch_duration_ms: number;
  error?: string;
}

// ─── /api/basedagents/scan response shape ───
interface ScanTotals {
  scanned: number;
  honest: number;
  scam_pattern: number;
  unknown: number;
  honest_paid: number;
  quick_wins: number;
  matching_our_capabilities: number;
}

interface ScanTask {
  task_id: string;
  title: string;
  creator?: string;
  category?: string;
  bounty?: { amount_display?: string; token?: string; network?: string } | null;
  escrow?: { status?: string } | null;
  required_capabilities?: string[];
  our_caps_overlap?: string[];
  estimated_effort?: "quick" | "multi-day" | "unknown";
  expires_at?: string | null;
  claimable?: boolean;
  classification_reasons?: string[];
  red_flags?: string[];
}

interface ScanResponse {
  ok: boolean;
  scanned_at: string;
  scan_duration_ms: number;
  totals: ScanTotals;
  honest_paid_tasks: ScanTask[];
  quick_wins: ScanTask[];
  matching_honest_tasks: ScanTask[];
  scam_pattern_tasks: ScanTask[];
  error?: string;
}

const NETWORK_LABEL: Record<string, string> = {
  "eip155:8453": "Base Mainnet",
  "eip155:84532": "Base Sepolia",
};

function shortAddr(addr: string, head = 8, tail = 6): string {
  if (!addr) return "";
  if (addr.length <= head + tail) return addr;
  return `${addr.slice(0, head)}…${addr.slice(-tail)}`;
}

function shortId(id: string, head = 10, tail = 6): string {
  if (!id) return "";
  if (id.length <= head + tail) return id;
  return `${id.slice(0, head)}…${id.slice(-tail)}`;
}

export function BasedAgentsIntegration() {
  const [data, setData] = useState<BasedAgentsStatus | null>(null);
  const [scan, setScan] = useState<ScanResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [scanning, setScanning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showWallet, setShowWallet] = useState(false);
  const [copied, setCopied] = useState<string | null>(null);

  const fetchStatus = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/basedagents/status", { cache: "no-store" });
      if (!res.ok) {
        const errBody = await res.json().catch(() => ({}));
        throw new Error(
          errBody.error || `HTTP ${res.status}: ${res.statusText}`,
        );
      }
      const json = (await res.json()) as BasedAgentsStatus;
      setData(json);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Network error");
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchScan = useCallback(async () => {
    setScanning(true);
    try {
      const res = await fetch("/api/basedagents/scan", { cache: "no-store" });
      if (res.ok) {
        const json = (await res.json()) as ScanResponse;
        if (json.ok) setScan(json);
      }
    } catch {
      // scan errors are non-fatal; status is the primary data source
    } finally {
      setScanning(false);
    }
  }, []);

  useEffect(() => {
    fetchStatus();
    fetchScan();
    // Refresh status every 90s, scan every 5 minutes (scan is heavier)
    const statusId = setInterval(fetchStatus, 90_000);
    const scanId = setInterval(fetchScan, 5 * 60_000);
    return () => {
      clearInterval(statusId);
      clearInterval(scanId);
    };
  }, [fetchStatus, fetchScan]);

  const copyToClipboard = (text: string, key: string) => {
    navigator.clipboard.writeText(text).then(() => {
      setCopied(key);
      setTimeout(() => setCopied(null), 1500);
    });
  };

  if (loading && !data) {
    return (
      <div className="flex items-center justify-center py-20">
        <Loader2 className="w-6 h-6 animate-spin text-emerald-400" />
        <span className="ml-3 text-sm text-slate-400 font-mono">
          Fetching live BasedAgents registry status (signed request)…
        </span>
      </div>
    );
  }

  if (error && !data) {
    return (
      <div className="p-6 rounded-2xl bg-rose-950/40 border border-rose-500/30">
        <div className="flex items-start gap-3">
          <XCircle className="w-5 h-5 text-rose-400 mt-0.5 flex-shrink-0" />
          <div>
            <div className="text-sm font-bold text-rose-300">
              Could not reach /api/basedagents/status
            </div>
            <div className="text-xs text-rose-400/80 font-mono mt-1">{error}</div>
            <button
              onClick={fetchStatus}
              className="mt-3 text-xs px-3 py-1.5 rounded-md bg-rose-900/40 hover:bg-rose-900/60 text-rose-200 font-mono flex items-center gap-1.5"
            >
              <RefreshCw className="w-3 h-3" /> Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!data) return null;

  const agent = data.agent;
  const wallet = data.wallet;
  const cb = data.claim_budget;
  const reg = data.registry;
  const ot = data.open_tasks;
  const scam = data.scam_alert;

  return (
    <div className="space-y-6">
      {/* ─── Header ─── */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 p-5 rounded-2xl bg-gradient-to-br from-slate-900 to-slate-950 border border-slate-800">
        <div>
          <div className="flex items-center gap-2 text-xs text-emerald-400 font-mono uppercase tracking-wider mb-1.5">
            <Store className="w-4 h-4" />
            <span>BasedAgents Marketplace Integration · Live</span>
          </div>
          <h2 className="text-xl font-bold text-white tracking-tight">
            {agent.name}
          </h2>
          <p className="text-xs text-slate-300 mt-1 max-w-2xl">
            Registered on BasedAgents — the task marketplace for AI agents. Bounty
            payouts settle in USDC on Base Mainnet via x402. Agent signs every
            request with its Ed25519 keypair.
          </p>
        </div>
        <div className="flex items-center gap-2 flex-shrink-0">
          <a
            href={agent.profile_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-xs px-3 py-2 rounded-md bg-emerald-600 hover:bg-emerald-500 text-white font-mono flex items-center gap-1.5 transition-colors"
          >
            <ExternalLink className="w-3 h-3" />
            Open profile
          </a>
          <button
            onClick={fetchStatus}
            disabled={loading}
            className="text-xs px-3 py-2 rounded-md bg-slate-800 hover:bg-slate-700 text-slate-200 font-mono flex items-center gap-1.5 transition-colors disabled:opacity-50"
          >
            <RefreshCw className={`w-3 h-3 ${loading ? "animate-spin" : ""}`} />
            Refresh
          </button>
        </div>
      </div>

      {/* ─── Agent identity grid ─── */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        {/* Agent ID */}
        <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
          <div className="text-[10px] text-slate-500 uppercase font-mono mb-1.5">
            Agent ID
          </div>
          <div className="text-sm font-mono text-emerald-300 break-all">
            {agent.agent_id}
          </div>
          <button
            onClick={() => copyToClipboard(agent.agent_id, "agent_id")}
            className="mt-2 text-[10px] text-slate-500 hover:text-slate-300 font-mono flex items-center gap-1"
          >
            {copied === "agent_id" ? (
              <>
                <CheckCircle2 className="w-3 h-3" /> copied
              </>
            ) : (
              <>
                <Copy className="w-3 h-3" /> copy
              </>
            )}
          </button>
        </div>

        {/* Status */}
        <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
          <div className="text-[10px] text-slate-500 uppercase font-mono mb-1.5">
            Status
          </div>
          <div className="flex items-center gap-2">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500" />
            </span>
            <span className="text-sm font-bold text-emerald-300 capitalize">
              {agent.status}
            </span>
          </div>
          <div className="text-[10px] text-slate-500 mt-1.5 font-mono">
            since {agent.registered_at?.slice(0, 10)}
          </div>
        </div>

        {/* Reputation */}
        <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
          <div className="text-[10px] text-slate-500 uppercase font-mono mb-1.5">
            Reputation
          </div>
          <div className="text-2xl font-bold text-white font-mono">
            {agent.reputation_score.toFixed(2)}
          </div>
          <div className="text-[10px] text-slate-500 mt-1.5 font-mono">
            {agent.verification_count} verification
            {agent.verification_count === 1 ? "" : "s"} ·{" "}
            {agent.ratings.count} rating
            {agent.ratings.count === 1 ? "" : "s"}
            {agent.ratings.average
              ? ` · avg ${agent.ratings.average.toFixed(1)}/5`
              : ""}
          </div>
        </div>

        {/* Claim budget */}
        <div className="p-4 rounded-xl bg-slate-950 border border-slate-800">
          <div className="text-[10px] text-slate-500 uppercase font-mono mb-1.5">
            Claim budget
          </div>
          <div className="text-2xl font-bold text-white font-mono">
            {cb.budget ?? "—"}
          </div>
          <div className="text-[10px] text-slate-500 mt-1.5 font-mono">
            {cb.bonded_slots} bonded / {cb.bond_capacity} slots · 1 USDC each
          </div>
        </div>
      </div>

      {/* ─── Wallet card ─── */}
      <div className="p-5 rounded-2xl bg-slate-950 border border-slate-800">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2 text-xs text-slate-400 font-mono uppercase tracking-wider">
            <Wallet className="w-4 h-4" />
            <span>Agent wallet (for BasedAgents bounty payouts)</span>
          </div>
          {wallet.verified ? (
            <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 font-mono flex items-center gap-1">
              <CheckCircle2 className="w-3 h-3" /> verified
            </span>
          ) : (
            <span className="text-[10px] px-2 py-0.5 rounded bg-amber-950 text-amber-300 font-mono flex items-center gap-1">
              <AlertTriangle className="w-3 h-3" /> unverified
            </span>
          )}
        </div>

        <div className="flex flex-col md:flex-row md:items-center gap-3">
          <code className="flex-1 text-sm font-mono text-emerald-300 bg-slate-900 px-3 py-2 rounded-md break-all">
            {showWallet ? wallet.address : shortAddr(wallet.address, 10, 8)}
          </code>
          <div className="flex items-center gap-2 flex-shrink-0">
            <button
              onClick={() => setShowWallet((s) => !s)}
              className="text-xs px-2.5 py-2 rounded-md bg-slate-800 hover:bg-slate-700 text-slate-300 font-mono flex items-center gap-1.5"
            >
              {showWallet ? (
                <>
                  <EyeOff className="w-3 h-3" /> Hide
                </>
              ) : (
                <>
                  <Eye className="w-3 h-3" /> Reveal
                </>
              )}
            </button>
            <button
              onClick={() => copyToClipboard(wallet.address, "wallet")}
              className="text-xs px-2.5 py-2 rounded-md bg-slate-800 hover:bg-slate-700 text-slate-300 font-mono flex items-center gap-1.5"
            >
              {copied === "wallet" ? (
                <>
                  <CheckCircle2 className="w-3 h-3" /> copied
                </>
              ) : (
                <>
                  <Copy className="w-3 h-3" /> Copy
                </>
              )}
            </button>
          </div>
        </div>

        <div className="mt-3 grid grid-cols-2 md:grid-cols-4 gap-2 text-xs font-mono">
          <div className="px-3 py-2 rounded-md bg-slate-900">
            <div className="text-[10px] text-slate-500 uppercase mb-0.5">
              Network
            </div>
            <div className="text-slate-200">
              {NETWORK_LABEL[wallet.network] || wallet.network}
            </div>
          </div>
          <div className="px-3 py-2 rounded-md bg-slate-900">
            <div className="text-[10px] text-slate-500 uppercase mb-0.5">
              Verified at
            </div>
            <div className="text-slate-200">
              {wallet.verified_at
                ? wallet.verified_at.slice(0, 19).replace("T", " ") + "Z"
                : "—"}
            </div>
          </div>
          <div className="px-3 py-2 rounded-md bg-slate-900">
            <div className="text-[10px] text-slate-500 uppercase mb-0.5">
              Balance USDC
            </div>
            <div className="text-slate-200">
              {wallet.current_balance_usdc !== null
                ? `$${wallet.current_balance_usdc.toFixed(2)}`
                : "n/a (RPC fetch off)"}
            </div>
          </div>
          <div className="px-3 py-2 rounded-md bg-slate-900">
            <div className="text-[10px] text-slate-500 uppercase mb-0.5">
              Bond needed
            </div>
            <div className="text-slate-200">
              1 USDC per bounty slot
            </div>
          </div>
        </div>

        <p className="mt-3 text-[11px] text-slate-500 leading-relaxed">
          {wallet.note}
        </p>
      </div>

      {/* ─── Registry snapshot ─── */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
        <StatCard
          icon={<Users className="w-4 h-4" />}
          label="Agents in registry"
          value={reg.agents_total?.toLocaleString() ?? "—"}
          accent="text-emerald-300"
        />
        <StatCard
          icon={<Activity className="w-4 h-4" />}
          label="Open tasks"
          value={reg.tasks_open?.toString() ?? "—"}
          accent="text-emerald-300"
        />
        <StatCard
          icon={<CheckCircle2 className="w-4 h-4" />}
          label="Paid tasks (all time)"
          value={reg.tasks_paid?.toString() ?? "—"}
          accent="text-emerald-300"
        />
        <StatCard
          icon={<TrendingUp className="w-4 h-4" />}
          label="USDC paid (all time)"
          value={reg.paid_usdc_total ? `$${reg.paid_usdc_total}` : "—"}
          accent="text-emerald-300"
        />
        <StatCard
          icon={<ShieldCheck className="w-4 h-4" />}
          label="Payments / Escrow"
          value={
            reg.payments && reg.escrow
              ? `${reg.payments} / ${reg.escrow}`
              : "—"
          }
          accent="text-emerald-300"
        />
      </div>

      {/* ─── Open tasks breakdown ─── */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <div className="p-4 rounded-xl bg-emerald-950/30 border border-emerald-700/40">
          <div className="text-[10px] text-emerald-400 uppercase font-mono mb-1">
            Honest tasks (BasedAgents_bot)
          </div>
          <div className="text-3xl font-bold text-emerald-300 font-mono">
            {ot.honest_count}
          </div>
          <div className="text-[10px] text-slate-400 mt-1">
            Free, reputation-only. Multi-day hard engineering work. Posted by
            BasedAgents project automation.
          </div>
        </div>

        <div className="p-4 rounded-xl bg-rose-950/30 border border-rose-700/40">
          <div className="text-[10px] text-rose-400 uppercase font-mono mb-1">
            Scam-pattern tasks (Industrial Sentinel)
          </div>
          <div className="text-3xl font-bold text-rose-300 font-mono">
            {ot.scam_pattern_count}
          </div>
          <div className="text-[10px] text-slate-400 mt-1">
            {ot.paid_scam_count} paid +{" "}
            {ot.scam_pattern_count - ot.paid_scam_count} free. All require
            running unverified docker with wallet access.
          </div>
        </div>

        <div className="p-4 rounded-xl bg-sky-950/30 border border-sky-700/40">
          <div className="text-[10px] text-sky-400 uppercase font-mono mb-1">
            Matching our capabilities
          </div>
          <div className="text-3xl font-bold text-sky-300 font-mono">
            {ot.matching_our_capabilities}
          </div>
          <div className="text-[10px] text-slate-400 mt-1">
            Honest tasks where capabilities overlap with research/code/security/
            testing/documentation.
          </div>
        </div>
      </div>

      {/* ─── Scam alert ─── */}
      <div className="p-5 rounded-2xl bg-rose-950/30 border border-rose-700/40">
        <div className="flex items-start gap-3">
          <div className="p-2 rounded-lg bg-rose-950 border border-rose-700/40 flex-shrink-0">
            <Ban className="w-5 h-5 text-rose-400" />
          </div>
          <div className="flex-1">
            <div className="text-sm font-bold text-rose-300">
              Scam pattern detected: {scam.pattern}
            </div>
            <div className="text-xs text-slate-300 mt-1.5">
              Creator agents:
            </div>
            <ul className="text-[11px] text-slate-400 font-mono mt-1 ml-4 list-disc">
              {scam.creator_agents.map((c) => (
                <li key={c}>{c}</li>
              ))}
            </ul>
            <div className="text-xs text-slate-300 mt-3">Red flags:</div>
            <ul className="text-[11px] text-slate-400 mt-1 ml-4 list-disc space-y-1">
              {scam.red_flags.map((r) => (
                <li key={r}>{r}</li>
              ))}
            </ul>
            <div className="mt-3 p-3 rounded-md bg-rose-950/60 border border-rose-800/40">
              <div className="text-[10px] text-rose-400 uppercase font-mono mb-1">
                Recommendation
              </div>
              <p className="text-xs text-rose-200">{scam.recommendation}</p>
            </div>
          </div>
        </div>
      </div>

      {/* ─── Capabilities ─── */}
      <div className="p-5 rounded-2xl bg-slate-950 border border-slate-800">
        <div className="text-[10px] text-slate-500 uppercase font-mono mb-3">
          Declared capabilities
        </div>
        <div className="flex flex-wrap gap-2">
          {agent.capabilities.map((c) => (
            <span
              key={c}
              className="text-xs px-2.5 py-1 rounded-md bg-emerald-950/40 border border-emerald-700/30 text-emerald-300 font-mono"
            >
              {c}
            </span>
          ))}
        </div>
      </div>

      {/* ─── Profile history (v1 lost, v2 active) ─── */}
      {data.profile_history.length > 0 && (
        <div className="p-5 rounded-2xl bg-slate-950 border border-slate-800">
          <div className="text-[10px] text-slate-500 uppercase font-mono mb-3">
            Profile history
          </div>
          <div className="space-y-3">
            {data.profile_history.map((h) => (
              <div
                key={h.agent_id}
                className="p-3 rounded-md bg-amber-950/20 border border-amber-800/30"
              >
                <div className="flex items-center justify-between gap-2 mb-1.5">
                  <div className="text-xs font-mono text-amber-300">
                    {h.name}
                  </div>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-amber-950 text-amber-400 font-mono uppercase">
                    {h.status}
                  </span>
                </div>
                <div className="text-[11px] text-slate-400 font-mono mb-1">
                  {h.agent_id}
                </div>
                <p className="text-xs text-slate-300 mb-2">{h.reason}</p>
                <div className="text-[11px] text-amber-300/80 italic">
                  Lesson: {h.lesson}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ─── Honest Task Monitor (live scan) ─── */}
      <HonestTaskMonitor scan={scan} onRescan={fetchScan} scanning={scanning} />

      {/* ─── Fetch metadata ─── */}
      <div className="text-[10px] text-slate-600 font-mono text-center">
        Status fetched {new Date(data.fetched_at).toLocaleString()} ·{" "}
        {data.fetch_duration_ms} ms ·{" "}
        {cb.signed_endpoint_works
          ? "AgentSig signing works ✓"
          : "AgentSig signing broken ✗"}
        {scan && (
          <>
            {" · "}
            Scan {scan.totals.scanned} tasks in {scan.scan_duration_ms} ms ·{" "}
            {scan.totals.honest_paid} honest paid ·{" "}
            {scan.totals.quick_wins} quick wins
          </>
        )}
      </div>
    </div>
  );
}

// ============================================================================
// Honest Task Monitor — surfaces real paid honest work the moment it appears.
// ============================================================================

function HonestTaskMonitor({
  scan,
  onRescan,
  scanning,
}: {
  scan: ScanResponse | null;
  onRescan: () => void;
  scanning: boolean;
}) {
  if (!scan) {
    return (
      <div className="p-5 rounded-2xl bg-slate-950 border border-slate-800">
        <div className="flex items-center gap-2 text-xs text-slate-400 font-mono uppercase tracking-wider mb-3">
          <Activity className="w-4 h-4 animate-pulse" />
          <span>Honest Task Monitor · scanning board…</span>
        </div>
      </div>
    );
  }

  const t = scan.totals;
  const hasHonestPaid = scan.honest_paid_tasks.length > 0;
  const hasQuickWin = scan.quick_wins.length > 0;

  return (
    <div className="space-y-4">
      {/* Monitor header */}
      <div className="flex items-center justify-between p-4 rounded-2xl bg-gradient-to-br from-cyan-950/40 to-slate-950 border border-cyan-700/40">
        <div>
          <div className="flex items-center gap-2 text-xs text-cyan-300 font-mono uppercase tracking-wider mb-1">
            <Activity className="w-4 h-4" />
            <span>Honest Task Monitor · live scan</span>
          </div>
          <p className="text-xs text-slate-300">
            Scans {t.scanned} open tasks every 5 min. Classifies each by
            creator + content + escrow model. Surfaces honest paid tasks (the
            gold), quick wins, and matching honest work the moment it appears.
          </p>
        </div>
        <button
          onClick={onRescan}
          disabled={scanning}
          className="text-xs px-3 py-2 rounded-md bg-cyan-900/40 hover:bg-cyan-900/60 text-cyan-200 font-mono flex items-center gap-1.5 disabled:opacity-50"
        >
          <RefreshCw className={`w-3 h-3 ${scanning ? "animate-spin" : ""}`} />
          {scanning ? "Scanning…" : "Rescan"}
        </button>
      </div>

      {/* Classification totals */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <ScanStatCard
          label="Scanned"
          value={t.scanned}
          sub="total open"
          color="text-slate-200"
        />
        <ScanStatCard
          label="Honest"
          value={t.honest}
          sub={`${t.honest_paid} paid · ${t.honest - t.honest_paid} free`}
          color="text-emerald-300"
        />
        <ScanStatCard
          label="Scam pattern"
          value={t.scam_pattern}
          sub="auto-detected"
          color="text-rose-300"
        />
        <ScanStatCard
          label="Match our caps"
          value={t.matching_our_capabilities}
          sub="honest + overlap"
          color="text-cyan-300"
        />
      </div>

      {/* Honest paid tasks — the gold */}
      <div
        className={`p-5 rounded-2xl border ${
          hasHonestPaid
            ? "bg-amber-950/40 border-amber-600/50 ring-2 ring-amber-500/30"
            : "bg-slate-950 border-slate-800"
        }`}
      >
        <div className="flex items-center gap-2 mb-3">
          {hasHonestPaid ? (
            <TrendingUp className="w-5 h-5 text-amber-400" />
          ) : (
            <Activity className="w-5 h-5 text-slate-500" />
          )}
          <h3 className="text-sm font-bold text-amber-300">
            Honest paid tasks (the gold)
          </h3>
          <span className="text-[10px] px-2 py-0.5 rounded bg-amber-950 text-amber-400 font-mono ml-auto">
            {scan.honest_paid_tasks.length}
          </span>
        </div>
        {hasHonestPaid ? (
          <div className="space-y-2">
            {scan.honest_paid_tasks.map((task) => (
              <TaskRow key={task.task_id} task={task} variant="gold" />
            ))}
          </div>
        ) : (
          <p className="text-xs text-slate-400 italic">
            None right now. The board currently has 0 honest escrow-funded
            bounty tasks. All 10 paid tasks are Industrial Sentinel scam
            pattern. This monitor will surface honest paid tasks the moment
            they appear — keep this tab open or check the activity feed.
          </p>
        )}
      </div>

      {/* Quick wins */}
      <div
        className={`p-5 rounded-2xl border ${
          hasQuickWin
            ? "bg-emerald-950/40 border-emerald-600/50"
            : "bg-slate-950 border-slate-800"
        }`}
      >
        <div className="flex items-center gap-2 mb-3">
          <Zap
            className={`w-5 h-5 ${hasQuickWin ? "text-emerald-400" : "text-slate-500"}`}
          />
          <h3 className="text-sm font-bold text-emerald-300">Quick wins</h3>
          <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 font-mono ml-auto">
            {scan.quick_wins.length}
          </span>
        </div>
        {hasQuickWin ? (
          <div className="space-y-2">
            {scan.quick_wins.map((task) => (
              <TaskRow key={task.task_id} task={task} variant="quick" />
            ))}
          </div>
        ) : (
          <p className="text-xs text-slate-400 italic">
            None right now. Quick wins are honest tasks with time-boxed scope
            (≤15 min execution) matching our capabilities. The single compat
            pilot task on the board requires macOS — we&apos;re on Linux
            sandbox, so it doesn&apos;t match.
          </p>
        )}
      </div>

      {/* Matching honest tasks (any effort) */}
      <div className="p-5 rounded-2xl bg-slate-950 border border-slate-800">
        <div className="flex items-center gap-2 mb-3">
          <ShieldCheck className="w-5 h-5 text-cyan-400" />
          <h3 className="text-sm font-bold text-cyan-300">
            Matching honest tasks (any effort)
          </h3>
          <span className="text-[10px] px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 font-mono ml-auto">
            {scan.matching_honest_tasks.length}
          </span>
        </div>
        {scan.matching_honest_tasks.length > 0 ? (
          <div className="space-y-2 max-h-96 overflow-y-auto pr-1 basedagents-scroll">
            {scan.matching_honest_tasks.map((task) => (
              <TaskRow key={task.task_id} task={task} variant="matching" />
            ))}
          </div>
        ) : (
          <p className="text-xs text-slate-400 italic">
            None currently. Check back when new tasks are posted.
          </p>
        )}
      </div>
    </div>
  );
}

function ScanStatCard({
  label,
  value,
  sub,
  color,
}: {
  label: string;
  value: number;
  sub: string;
  color: string;
}) {
  return (
    <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
      <div className="text-[10px] text-slate-500 uppercase font-mono mb-1">
        {label}
      </div>
      <div className={`text-2xl font-bold font-mono ${color}`}>{value}</div>
      <div className="text-[10px] text-slate-500 mt-0.5 font-mono">{sub}</div>
    </div>
  );
}

function TaskRow({
  task,
  variant,
}: {
  task: ScanTask;
  variant: "gold" | "quick" | "matching";
}) {
  const variantAccent =
    variant === "gold"
      ? "border-amber-700/40 hover:border-amber-500/60 bg-amber-950/20"
      : variant === "quick"
        ? "border-emerald-700/40 hover:border-emerald-500/60 bg-emerald-950/20"
        : "border-slate-700/40 hover:border-slate-500/60 bg-slate-900/40";
  const bounty = task.bounty?.amount_display
    ? `$${task.bounty.amount_display} ${task.bounty.token || "USDC"}`
    : "free";
  const escrowBadge = task.escrow?.status
    ? task.escrow.status === "funded"
      ? "escrow ✓"
      : `escrow: ${task.escrow.status}`
    : "no escrow";

  return (
    <div
      className={`p-3 rounded-lg border ${variantAccent} transition-colors`}
    >
      <div className="flex items-start justify-between gap-2 mb-1">
        <a
          href={`https://basedagents.ai/tasks/${task.task_id}`}
          target="_blank"
          rel="noopener noreferrer"
          className="text-sm font-semibold text-slate-100 hover:text-white flex-1 flex items-start gap-1.5"
        >
          <span>{task.title}</span>
          <ExternalLink className="w-3 h-3 flex-shrink-0 mt-0.5 text-slate-500" />
        </a>
        <div className="flex items-center gap-1.5 flex-shrink-0">
          <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 font-mono">
            {bounty}
          </span>
          <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 font-mono">
            {escrowBadge}
          </span>
          {task.estimated_effort && (
            <span
              className={`text-[10px] px-1.5 py-0.5 rounded font-mono ${
                task.estimated_effort === "quick"
                  ? "bg-emerald-950 text-emerald-300"
                  : "bg-amber-950 text-amber-300"
              }`}
            >
              {task.estimated_effort}
            </span>
          )}
        </div>
      </div>
      <div className="flex items-center gap-2 text-[10px] text-slate-500 font-mono">
        <span>{task.task_id}</span>
        {task.category && <span>· {task.category}</span>}
        {task.expires_at && (
          <span>· expires {task.expires_at.slice(0, 10)}</span>
        )}
        {!task.claimable && (
          <span className="text-rose-400">· not claimable</span>
        )}
      </div>
      {task.our_caps_overlap && task.our_caps_overlap.length > 0 && (
        <div className="flex flex-wrap gap-1 mt-2">
          {task.our_caps_overlap.map((c) => (
            <span
              key={c}
              className="text-[9px] px-1.5 py-0.5 rounded bg-cyan-950/40 border border-cyan-700/30 text-cyan-300 font-mono"
            >
              {c}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

function StatCard({
  icon,
  label,
  value,
  accent,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
  accent: string;
}) {
  return (
    <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
      <div className="flex items-center gap-1.5 text-[10px] text-slate-500 uppercase font-mono mb-1.5">
        {icon}
        <span>{label}</span>
      </div>
      <div className={`text-lg font-bold font-mono ${accent}`}>{value}</div>
    </div>
  );
}
