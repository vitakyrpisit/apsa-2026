"use client";

import { useCallback, useEffect, useState } from "react";
import {
  Activity,
  TrendingUp,
  TrendingDown,
  Minus,
  RefreshCw,
  Zap,
  DollarSign,
  Cpu,
  Clock,
} from "lucide-react";
import { AnimatedNumber } from "./animated-number";
import { toast } from "sonner";
import { useActivityFeed } from "./activity-feed-provider";

interface MarketDataPoint {
  symbol: string;
  name: string;
  priceUsd: number;
  change24h: number;
  marketCap: number;
  volume24h: number;
  collectedAt: string;
  source: string;
}

interface MarketAnalysis {
  id: string;
  symbol: string;
  title: string;
  summary: string;
  keyPoints: string[];
  signal: "BULLISH" | "BEARISH" | "NEUTRAL";
  confidence: number;
  priceTarget?: number;
  generatedAt: string;
  llmModel: string;
  sha256: string;
}

interface MarketSignal {
  id: string;
  symbol: string;
  action: "BUY" | "SELL" | "HOLD";
  entryPrice: number;
  confidence: number;
  rationale: string;
  generatedAt: string;
  expiresAt: string;
}

interface AgentStats {
  dataPointsCollected: number;
  analysesGenerated: number;
  signalsGenerated: number;
  x402Requests: number;
  x402Paid: number;
  totalRevenueUSDC: number;
  lastCollectionAt: string | null;
  lastAnalysisAt: string | null;
  agentRunningSince: string;
}

interface IntelData {
  stats: AgentStats;
  marketData: MarketDataPoint[];
  analyses: MarketAnalysis[];
  signals: MarketSignal[];
}

export function MarketIntelAgent() {
  const [data, setData] = useState<IntelData | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const { logEvent } = useActivityFeed();

  const fetchIntel = useCallback(async () => {
    try {
      const res = await fetch("/api/market-intel");
      const d: IntelData = await res.json();
      setData(d);
    } catch {
      // silent
    } finally {
      setLoading(false);
    }
  }, []);

  const triggerCycle = useCallback(async () => {
    setRefreshing(true);
    logEvent("suite-run", "Market Intel cycle triggered", "Manual data collection + LLM analysis", "violet");
    toast.info("Triggering market intel cycle…", {
      description: "Collecting data + generating LLM analyses",
    });
    try {
      await fetch("/api/market-intel", { method: "POST" });
      // Wait a moment for the cycle to complete, then refetch
      setTimeout(() => {
        fetchIntel();
        setRefreshing(false);
        toast.success("Market intel cycle completed");
      }, 5000);
    } catch {
      setRefreshing(false);
      toast.error("Cycle failed");
    }
  }, [fetchIntel, logEvent]);

  useEffect(() => {
    fetchIntel();
    const interval = setInterval(fetchIntel, 30000); // Poll every 30s
    return () => clearInterval(interval);
  }, [fetchIntel]);

  const stats = data?.stats;
  const marketData = data?.marketData ?? [];
  const analyses = data?.analyses ?? [];
  const signals = data?.signals ?? [];

  return (
    <div className="space-y-6">
      {/* Agent banner */}
      <div className="bg-gradient-to-br from-violet-950/30 via-slate-900 to-slate-950 border border-violet-800/40 rounded-xl p-6">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-4 border-b border-slate-800">
          <div>
            <div className="flex items-center gap-2 text-xs text-violet-400 font-mono uppercase tracking-wider mb-1">
              <Cpu className="w-4 h-4" />
              <span>Autonomous Financial Information Agent</span>
              <span className="w-1.5 h-1.5 rounded-full bg-violet-400 apsa-live-dot" />
            </div>
            <h2 className="text-xl font-bold text-white tracking-tight">
              MarketIntelAgent — AgoraFX-style Revenue Engine
            </h2>
            <p className="text-xs text-slate-400 mt-1 max-w-3xl">
              Collects real market data from CoinGecko + Base RPC, generates LLM-powered
              analyses and trading signals, sells them via x402 micropayments ($0.05/analysis,
              $0.01/signal). Revenue flows to{" "}
              <code className="text-emerald-300 font-mono">0x829f…2BDA</code>.
            </p>
          </div>
          <button
            onClick={triggerCycle}
            disabled={refreshing}
            className="px-4 py-2 rounded-lg bg-violet-600 hover:bg-violet-500 text-white text-xs font-mono font-medium flex items-center gap-2 transition-colors disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${refreshing ? "animate-spin" : ""}`} />
            {refreshing ? "Collecting + Analyzing…" : "Trigger Cycle"}
          </button>
        </div>

        {/* Agent stats grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-6 gap-3 mt-4">
          <StatCard
            icon={<Activity className="w-3.5 h-3.5" />}
            label="Data Points"
            value={stats?.dataPointsCollected ?? 0}
            tone="slate"
          />
          <StatCard
            icon={<Cpu className="w-3.5 h-3.5" />}
            label="Analyses"
            value={stats?.analysesGenerated ?? 0}
            tone="violet"
          />
          <StatCard
            icon={<Zap className="w-3.5 h-3.5" />}
            label="Signals"
            value={stats?.signalsGenerated ?? 0}
            tone="amber"
          />
          <StatCard
            icon={<Clock className="w-3.5 h-3.5" />}
            label="x402 Requests"
            value={stats?.x402Requests ?? 0}
            tone="slate"
          />
          <StatCard
            icon={<DollarSign className="w-3.5 h-3.5" />}
            label="Paid Requests"
            value={stats?.x402Paid ?? 0}
            tone="emerald"
          />
          <StatCard
            icon={<DollarSign className="w-3.5 h-3.5" />}
            label="Revenue USDC"
            value={stats?.totalRevenueUSDC ?? 0}
            decimals={2}
            prefix="$"
            tone="emerald"
          />
        </div>

        {/* Last activity */}
        <div className="mt-3 flex flex-wrap items-center gap-4 text-[11px] font-mono text-slate-400">
          <span>Agent running since: {stats ? new Date(stats.agentRunningSince).toLocaleTimeString() : "—"}</span>
          {stats?.lastCollectionAt && (
            <span>Last collection: {new Date(stats.lastCollectionAt).toLocaleTimeString()}</span>
          )}
          {stats?.lastAnalysisAt && (
            <span>Last analysis: {new Date(stats.lastAnalysisAt).toLocaleTimeString()}</span>
          )}
        </div>
      </div>

      {/* Market data table */}
      {marketData.length > 0 && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="text-xs font-mono text-violet-400 uppercase tracking-wider mb-3 flex items-center gap-2">
            <Activity className="w-3.5 h-3.5" />
            Live Market Data (CoinGecko)
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-mono text-slate-300">
              <thead className="bg-slate-950 text-slate-400 uppercase text-[10px]">
                <tr>
                  <th className="py-2 px-3">Symbol</th>
                  <th className="py-2 px-3 text-right">Price</th>
                  <th className="py-2 px-3 text-right">24h %</th>
                  <th className="py-2 px-3 text-right">Market Cap</th>
                  <th className="py-2 px-3 text-right">Volume 24h</th>
                  <th className="py-2 px-3">Source</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {marketData.map((d) => (
                  <tr key={d.symbol} className="hover:bg-slate-800/40">
                    <td className="py-2 px-3 font-semibold text-white">{d.symbol}</td>
                    <td className="py-2 px-3 text-right text-slate-200">
                      ${d.priceUsd < 1 ? d.priceUsd.toFixed(6) : d.priceUsd.toLocaleString()}
                    </td>
                    <td className={`py-2 px-3 text-right font-bold ${d.change24h >= 0 ? "text-emerald-400" : "text-rose-400"}`}>
                      {d.change24h >= 0 ? "+" : ""}{d.change24h.toFixed(2)}%
                    </td>
                    <td className="py-2 px-3 text-right text-slate-400">
                      ${(d.marketCap / 1e9).toFixed(2)}B
                    </td>
                    <td className="py-2 px-3 text-right text-slate-400">
                      ${(d.volume24h / 1e6).toFixed(2)}M
                    </td>
                    <td className="py-2 px-3 text-slate-500">{d.source}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Analyses */}
      {analyses.length > 0 && (
        <div className="space-y-3">
          <div className="text-xs font-mono text-violet-400 uppercase tracking-wider">
            LLM-Generated Market Analyses ($0.05/each via x402)
          </div>
          {analyses.map((a) => (
            <div
              key={a.id}
              className="bg-slate-900 border border-slate-800 rounded-xl p-4"
            >
              <div className="flex items-start justify-between gap-3 mb-2">
                <div>
                  <span className="text-xs font-mono text-slate-400">{a.symbol}</span>
                  <h3 className="text-sm font-bold text-white">{a.title}</h3>
                </div>
                <SignalBadge signal={a.signal} confidence={a.confidence} />
              </div>
              <p className="text-xs text-slate-400 leading-relaxed mb-2">{a.summary}</p>
              {a.keyPoints.length > 0 && (
                <ul className="space-y-1">
                  {a.keyPoints.map((p, i) => (
                    <li key={i} className="text-[11px] text-slate-500 flex items-start gap-1.5">
                      <span className="text-violet-400 mt-0.5">•</span>
                      {p}
                    </li>
                  ))}
                </ul>
              )}
              <div className="mt-3 pt-2 border-t border-slate-800 flex items-center justify-between text-[10px] font-mono text-slate-500">
                <span>Model: {a.llmModel}</span>
                <span className="truncate">{a.sha256.slice(0, 24)}…</span>
                <span>{new Date(a.generatedAt).toLocaleTimeString()}</span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Signals */}
      {signals.length > 0 && (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="text-xs font-mono text-amber-400 uppercase tracking-wider mb-3">
            Trading Signals ($0.01/each via x402)
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {signals.map((s) => (
              <div
                key={s.id}
                className={`p-3 rounded-lg border ${
                  s.action === "BUY"
                    ? "bg-emerald-950/20 border-emerald-900/40"
                    : s.action === "SELL"
                      ? "bg-rose-950/20 border-rose-900/40"
                      : "bg-slate-950/40 border-slate-800"
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs font-mono font-bold text-white">{s.symbol}</span>
                  <span
                    className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold ${
                      s.action === "BUY"
                        ? "bg-emerald-900 text-emerald-200"
                        : s.action === "SELL"
                          ? "bg-rose-900 text-rose-200"
                          : "bg-slate-700 text-slate-200"
                    }`}
                  >
                    {s.action}
                  </span>
                </div>
                <div className="text-xs font-mono text-slate-300">
                  @ ${s.entryPrice < 1 ? s.entryPrice.toFixed(6) : s.entryPrice.toLocaleString()}
                </div>
                <div className="text-[10px] font-mono text-slate-500 mt-1">
                  Confidence: {s.confidence}%
                </div>
                <div className="text-[10px] font-mono text-slate-600 mt-1">
                  Expires: {new Date(s.expiresAt).toLocaleTimeString()}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Empty state */}
      {loading && (
        <div className="flex items-center justify-center py-12 text-slate-500">
          <RefreshCw className="w-5 h-5 animate-spin mr-2" />
          <span className="text-sm font-mono">Starting MarketIntelAgent…</span>
        </div>
      )}
    </div>
  );
}

function StatCard({
  icon,
  label,
  value,
  tone = "slate",
  decimals = 0,
  prefix = "",
}: {
  icon: React.ReactNode;
  label: string;
  value: number;
  tone?: "slate" | "emerald" | "amber" | "violet";
  decimals?: number;
  prefix?: string;
}) {
  const toneMap = {
    slate: "text-slate-300",
    emerald: "text-emerald-400",
    amber: "text-amber-400",
    violet: "text-violet-400",
  };
  return (
    <div className="p-2.5 rounded-lg bg-slate-950/60 border border-slate-800">
      <div className="flex items-center gap-1.5 text-[10px] font-mono text-slate-500 uppercase mb-1">
        {icon}
        {label}
      </div>
      <div className={`text-lg font-mono font-bold ${toneMap[tone]}`}>
        {prefix}
        <AnimatedNumber value={value} decimals={decimals} durationMs={600} />
      </div>
    </div>
  );
}

function SignalBadge({
  signal,
  confidence,
}: {
  signal: "BULLISH" | "BEARISH" | "NEUTRAL";
  confidence: number;
}) {
  const Icon = signal === "BULLISH" ? TrendingUp : signal === "BEARISH" ? TrendingDown : Minus;
  const color =
    signal === "BULLISH"
      ? "bg-emerald-950 text-emerald-300 border-emerald-800"
      : signal === "BEARISH"
        ? "bg-rose-950 text-rose-300 border-rose-800"
        : "bg-slate-800 text-slate-300 border-slate-700";
  return (
    <span
      className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold border flex items-center gap-1 ${color}`}
    >
      <Icon className="w-3 h-3" />
      {signal} {confidence}%
    </span>
  );
}
