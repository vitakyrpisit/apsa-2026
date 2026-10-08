"use client";

import { useCallback, useEffect, useState } from "react";
import {
  Store,
  ShieldCheck,
  AlertTriangle,
  ExternalLink,
  Wallet,
  Activity,
  CheckCircle2,
  XCircle,
  Loader2,
  RefreshCw,
  Copy,
  Ban,
  Skull,
  Eye,
  Zap,
} from "lucide-react";

// ============================================================================
// /api/marketplaces/identities — unified view of all our agent identities
// across every known AI agent marketplace. Some are registered, some auth-only,
// some couldn't be reached.
// ============================================================================

type MarketplaceStatus =
  | "registered"
  | "auth_only"
  | "dead"
  | "spa_only"
  | "not_an_agent_market"
  | "not_attempted";

interface Identity {
  platform: string;
  slug: string;
  status: MarketplaceStatus;
  agent_id: string | null;
  agent_id_field?: string;
  profile_url: string | null;
  api_base: string;
  credential_path: string | null;
  registered_at: string | null;
  capabilities: string[] | null;
  payout_wallet: string | null;
  payout_wallet_verified: boolean | null;
  reputation_score: number | null;
  reputation_label: string | null;
  live: {
    fetched_at: string;
    profile_reachable: boolean;
    fields_seen: string[];
  } | null;
  notes: string | null;
}

interface IdentitiesResponse {
  ok: boolean;
  agent_name: string;
  summary: {
    total_platforms: number;
    registered: number;
    auth_only: number;
    dead: number;
    spa_only: number;
    not_an_agent_market: number;
    not_attempted: number;
    payout_wallets_used: string[];
  };
  identities: Identity[];
  fetched_at: string;
  fetch_duration_ms: number;
  error?: string;
}

const STATUS_STYLES: Record<
  MarketplaceStatus,
  { label: string; badge: string; icon: typeof CheckCircle2 }
> = {
  registered: {
    label: "Registered",
    badge: "bg-emerald-950 text-emerald-300 border-emerald-700/40",
    icon: CheckCircle2,
  },
  auth_only: {
    label: "Auth only",
    badge: "bg-sky-950 text-sky-300 border-sky-700/40",
    icon: ShieldCheck,
  },
  dead: {
    label: "Dead",
    badge: "bg-rose-950 text-rose-300 border-rose-700/40",
    icon: Skull,
  },
  spa_only: {
    label: "SPA only",
    badge: "bg-amber-950 text-amber-300 border-amber-700/40",
    icon: Eye,
  },
  not_an_agent_market: {
    label: "Not agent market",
    badge: "bg-slate-800 text-slate-400 border-slate-700",
    icon: Ban,
  },
  not_attempted: {
    label: "Not attempted",
    badge: "bg-slate-800 text-slate-400 border-slate-700",
    icon: Activity,
  },
};

function shortAddr(addr: string | null, head = 8, tail = 6): string {
  if (!addr) return "—";
  if (addr.length <= head + tail) return addr;
  return `${addr.slice(0, head)}…${addr.slice(-tail)}`;
}

function shortId(id: string | null, head = 14, tail = 8): string {
  if (!id) return "—";
  if (id.length <= head + tail) return id;
  return `${id.slice(0, head)}…${id.slice(-tail)}`;
}

export function MarketplacesIntegration() {
  const [data, setData] = useState<IdentitiesResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState<string | null>(null);

  const fetchIdentities = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/marketplaces/identities", {
        cache: "no-store",
      });
      if (!res.ok) {
        const errBody = await res.json().catch(() => ({}));
        throw new Error(
          errBody.error || `HTTP ${res.status}: ${res.statusText}`,
        );
      }
      const json = (await res.json()) as IdentitiesResponse;
      setData(json);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Network error");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchIdentities();
    const id = setInterval(fetchIdentities, 5 * 60_000); // refresh every 5 min
    return () => clearInterval(id);
  }, [fetchIdentities]);

  const copyToClipboard = (text: string, key: string) => {
    navigator.clipboard.writeText(text).then(() => {
      setCopied(key);
      setTimeout(() => setCopied(null), 1500);
    });
  };

  if (loading && !data) {
    return (
      <div className="flex items-center justify-center py-20">
        <Loader2 className="w-6 h-6 animate-spin text-cyan-400" />
        <span className="ml-3 text-sm text-slate-400 font-mono">
          Loading identities across all marketplaces…
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
              Could not load marketplace identities
            </div>
            <div className="text-xs text-rose-400/80 font-mono mt-1">
              {error}
            </div>
            <button
              onClick={fetchIdentities}
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

  const s = data.summary;
  const registered = data.identities.filter(
    (i) => i.status === "registered" || i.status === "auth_only",
  );
  const failed = data.identities.filter(
    (i) =>
      i.status === "dead" ||
      i.status === "spa_only" ||
      i.status === "not_an_agent_market" ||
      i.status === "not_attempted",
  );

  return (
    <div className="space-y-6">
      {/* ─── Header ─── */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 p-5 rounded-2xl bg-gradient-to-br from-cyan-950/40 to-slate-950 border border-cyan-700/40">
        <div>
          <div className="flex items-center gap-2 text-xs text-cyan-300 font-mono uppercase tracking-wider mb-1.5">
            <Store className="w-4 h-4" />
            <span>Marketplace Presence · Multi-platform Agent Identity</span>
          </div>
          <h2 className="text-xl font-bold text-white tracking-tight">
            {data.agent_name}
          </h2>
          <p className="text-xs text-slate-300 mt-1 max-w-3xl">
            Live registry of our agent&apos;s identities across every known AI
            agent marketplace. Each row is a real registration with a profile
            you can visit, or a documented reason why we couldn&apos;t register.
          </p>
        </div>
        <button
          onClick={fetchIdentities}
          disabled={loading}
          className="text-xs px-3 py-2 rounded-md bg-cyan-900/40 hover:bg-cyan-900/60 text-cyan-200 font-mono flex items-center gap-1.5 transition-colors disabled:opacity-50"
        >
          <RefreshCw className={`w-3 h-3 ${loading ? "animate-spin" : ""}`} />
          Refresh
        </button>
      </div>

      {/* ─── Summary stat cards ─── */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-7 gap-3">
        <SummaryStat
          icon={<Store className="w-4 h-4" />}
          label="Total platforms"
          value={s.total_platforms}
          color="text-slate-200"
        />
        <SummaryStat
          icon={<CheckCircle2 className="w-4 h-4" />}
          label="Registered"
          value={s.registered}
          color="text-emerald-300"
        />
        <SummaryStat
          icon={<ShieldCheck className="w-4 h-4" />}
          label="Auth only"
          value={s.auth_only}
          color="text-sky-300"
        />
        <SummaryStat
          icon={<Skull className="w-4 h-4" />}
          label="Dead"
          value={s.dead}
          color="text-rose-300"
        />
        <SummaryStat
          icon={<Eye className="w-4 h-4" />}
          label="SPA only"
          value={s.spa_only}
          color="text-amber-300"
        />
        <SummaryStat
          icon={<Ban className="w-4 h-4" />}
          label="Not agent market"
          value={s.not_an_agent_market}
          color="text-slate-400"
        />
        <SummaryStat
          icon={<Activity className="w-4 h-4" />}
          label="Not attempted"
          value={s.not_attempted}
          color="text-slate-400"
        />
      </div>

      {/* ─── Payout wallets ─── */}
      <div className="p-5 rounded-2xl bg-slate-950 border border-slate-800">
        <div className="flex items-center gap-2 text-xs text-slate-400 font-mono uppercase tracking-wider mb-3">
          <Wallet className="w-4 h-4" />
          <span>Payout wallets in use</span>
        </div>
        <div className="space-y-2">
          {s.payout_wallets_used.map((w) => {
            const purpose =
              w === "0x829f877daAb94D766BB2b8511ad486C40f2C2BDA"
                ? "Operator's receive-only wallet (APSA-2026 service + Agent402 router)"
                : "Sandbox-generated EVM wallet for BasedAgents BountyBook tasks (we control private key)";
            return (
              <div
                key={w}
                className="flex flex-col md:flex-row md:items-center gap-2 p-3 rounded-md bg-slate-900"
              >
                <code className="flex-1 text-xs font-mono text-emerald-300 break-all">
                  {w}
                </code>
                <span className="text-[10px] text-slate-500 font-mono md:text-right max-w-md">
                  {purpose}
                </span>
                <button
                  onClick={() => copyToClipboard(w, `wallet-${w}`)}
                  className="text-[10px] px-2 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 font-mono flex items-center gap-1 flex-shrink-0"
                >
                  {copied === `wallet-${w}` ? (
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
            );
          })}
        </div>
      </div>

      {/* ─── Live registrations (registered + auth_only) ─── */}
      <div>
        <div className="flex items-center gap-2 text-xs text-emerald-400 font-mono uppercase tracking-wider mb-3">
          <CheckCircle2 className="w-4 h-4" />
          <span>Live registrations · {registered.length} platforms</span>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
          {registered.map((id) => (
            <IdentityCard
              key={id.slug}
              identity={id}
              onCopy={copyToClipboard}
              copied={copied}
            />
          ))}
        </div>
      </div>

      {/* ─── Couldn't register ─── */}
      <div>
        <div className="flex items-center gap-2 text-xs text-rose-400 font-mono uppercase tracking-wider mb-3">
          <Ban className="w-4 h-4" />
          <span>Couldn&apos;t register · {failed.length} platforms</span>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {failed.map((id) => (
            <FailedCard key={id.slug} identity={id} />
          ))}
        </div>
      </div>

      {/* ─── Footer metadata ─── */}
      <div className="text-[10px] text-slate-600 font-mono text-center">
        Fetched {new Date(data.fetched_at).toLocaleString()} ·{" "}
        {data.fetch_duration_ms} ms · {s.registered} live registrations across{" "}
        {s.total_platforms} explored platforms
      </div>
    </div>
  );
}

function SummaryStat({
  icon,
  label,
  value,
  color,
}: {
  icon: React.ReactNode;
  label: string;
  value: number;
  color: string;
}) {
  return (
    <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
      <div className="flex items-center gap-1.5 text-[10px] text-slate-500 uppercase font-mono mb-1.5">
        {icon}
        <span>{label}</span>
      </div>
      <div className={`text-2xl font-bold font-mono ${color}`}>{value}</div>
    </div>
  );
}

function IdentityCard({
  identity,
  onCopy,
  copied,
}: {
  identity: Identity;
  onCopy: (text: string, key: string) => void;
  copied: string | null;
}) {
  const status = STATUS_STYLES[identity.status];
  const StatusIcon = status.icon;
  const isAuthOnly = identity.status === "auth_only";

  return (
    <div
      className={`p-4 rounded-xl border ${
        isAuthOnly
          ? "bg-sky-950/20 border-sky-700/40"
          : "bg-emerald-950/20 border-emerald-700/40"
      } hover:border-slate-600 transition-colors`}
    >
      {/* Header: platform name + status badge */}
      <div className="flex items-start justify-between gap-2 mb-3">
        <div className="flex-1 min-w-0">
          <h3 className="text-sm font-bold text-white truncate">
            {identity.platform}
          </h3>
          <a
            href={identity.profile_url || "#"}
            target="_blank"
            rel="noopener noreferrer"
            className="text-[10px] text-slate-400 hover:text-slate-200 font-mono flex items-center gap-1 mt-0.5 break-all"
          >
            {identity.profile_url ? (
              <>
                <ExternalLink className="w-3 h-3 flex-shrink-0" />
                <span className="truncate">{identity.profile_url}</span>
              </>
            ) : (
              <span className="italic">no public profile</span>
            )}
          </a>
        </div>
        <span
          className={`text-[10px] px-2 py-0.5 rounded border font-mono flex items-center gap-1 flex-shrink-0 ${status.badge}`}
        >
          <StatusIcon className="w-3 h-3" />
          {status.label}
        </span>
      </div>

      {/* Agent ID */}
      <div className="mb-2">
        <div className="text-[10px] text-slate-500 uppercase font-mono mb-0.5">
          {identity.agent_id_field || "agent_id"}
        </div>
        <div className="flex items-center gap-1">
          <code className="flex-1 text-xs font-mono text-emerald-300 bg-slate-900 px-2 py-1 rounded break-all">
            {identity.agent_id || "—"}
          </code>
          {identity.agent_id && (
            <button
              onClick={() => onCopy(identity.agent_id || "", `id-${identity.slug}`)}
              className="text-[10px] px-1.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-400 font-mono flex-shrink-0"
            >
              {copied === `id-${identity.slug}` ? (
                <CheckCircle2 className="w-3 h-3 text-emerald-400" />
              ) : (
                <Copy className="w-3 h-3" />
              )}
            </button>
          )}
        </div>
      </div>

      {/* Metadata grid */}
      <div className="grid grid-cols-2 gap-2 text-[10px] font-mono">
        <Meta label="Registered" value={identity.registered_at?.slice(0, 10) || "—"} />
        <Meta
          label="Reputation"
          value={
            identity.reputation_label ||
            (identity.reputation_score !== null
              ? String(identity.reputation_score)
              : "—")
          }
        />
        <Meta
          label="Payout wallet"
          value={
            identity.payout_wallet ? shortAddr(identity.payout_wallet) : "—"
          }
          highlight={!!identity.payout_wallet_verified}
        />
        <Meta
          label="Wallet verified"
          value={
            identity.payout_wallet_verified === null
              ? "—"
              : identity.payout_wallet_verified
                ? "✓ yes"
                : "✗ no"
          }
          highlight={!!identity.payout_wallet_verified}
        />
      </div>

      {/* Capabilities */}
      {identity.capabilities && identity.capabilities.length > 0 && (
        <div className="mt-2 flex flex-wrap gap-1">
          {identity.capabilities.map((c) => (
            <span
              key={c}
              className="text-[9px] px-1.5 py-0.5 rounded bg-cyan-950/40 border border-cyan-700/30 text-cyan-300 font-mono"
            >
              {c}
            </span>
          ))}
        </div>
      )}

      {/* Live fetch status (when applicable) */}
      {identity.live && (
        <div className="mt-2 text-[10px] text-slate-500 font-mono">
          {identity.live.profile_reachable ? (
            <span className="text-emerald-400">
              ✓ live profile fetched
            </span>
          ) : (
            <span className="text-amber-400">
              ⚠ live fetch failed
            </span>
          )}
          {identity.live.fields_seen.length > 0 && (
            <span className="ml-2 text-slate-600">
              · {identity.live.fields_seen.length} fields
            </span>
          )}
        </div>
      )}

      {/* Credential path (informational) */}
      {identity.credential_path && (
        <div className="mt-2 text-[10px] text-slate-600 font-mono">
          <ShieldCheck className="w-3 h-3 inline mr-1" />
          credentials: {identity.credential_path} (mode 0600, .gitignored)
        </div>
      )}

      {/* Notes */}
      {identity.notes && (
        <p className="mt-2 text-[10px] text-slate-400 leading-relaxed border-t border-slate-800 pt-2">
          {identity.notes}
        </p>
      )}
    </div>
  );
}

function FailedCard({ identity }: { identity: Identity }) {
  const status = STATUS_STYLES[identity.status];
  const StatusIcon = status.icon;

  return (
    <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
      <div className="flex items-center gap-2 mb-1.5">
        <StatusIcon className="w-4 h-4 text-slate-400 flex-shrink-0" />
        <span className="text-sm font-semibold text-slate-200 flex-1 truncate">
          {identity.platform}
        </span>
        <span
          className={`text-[9px] px-1.5 py-0.5 rounded border font-mono flex-shrink-0 ${status.badge}`}
        >
          {status.label}
        </span>
      </div>
      {identity.profile_url && (
        <a
          href={identity.profile_url}
          target="_blank"
          rel="noopener noreferrer"
          className="block text-[10px] text-slate-500 hover:text-slate-300 font-mono mb-1.5 truncate"
        >
          {identity.profile_url}
        </a>
      )}
      <p className="text-[10px] text-slate-400 leading-relaxed">
        {identity.notes}
      </p>
    </div>
  );
}

function Meta({
  label,
  value,
  highlight,
}: {
  label: string;
  value: string;
  highlight?: boolean;
}) {
  return (
    <div className="px-2 py-1.5 rounded-md bg-slate-900">
      <div className="text-[9px] text-slate-500 uppercase mb-0.5">{label}</div>
      <div
        className={`font-mono ${highlight ? "text-emerald-300" : "text-slate-200"}`}
      >
        {value}
      </div>
    </div>
  );
}
