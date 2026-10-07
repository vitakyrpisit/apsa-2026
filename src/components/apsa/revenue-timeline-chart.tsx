"use client";

import { useMemo, useState } from "react";
import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  ReferenceLine,
} from "recharts";

interface RevenueTimelineChartProps {
  netDailyUSD: number;
}

type Horizon = "30d" | "90d" | "365d";

const HORIZONS: { id: Horizon; label: string; days: number }[] = [
  { id: "30d", label: "30 days", days: 30 },
  { id: "90d", label: "90 days", days: 90 },
  { id: "365d", label: "1 year", days: 365 },
];

/**
 * RevenueTimelineChart — forward-looking cumulative net profit projection.
 * Models compounding growth at a configurable daily rate (default 1.5%/day
 * organic discovery ramp, capped at 3× steady state) so the operator can
 * visualise the runway from $0 to a target monthly run-rate.
 *
 * Honest modelling: the chart clearly labels itself as a [MODELLED ASSUMPTION]
 * and never claims to be on-chain revenue.
 */
export function RevenueTimelineChart({ netDailyUSD }: RevenueTimelineChartProps) {
  const [horizon, setHorizon] = useState<Horizon>("90d");
  const [growthRatePct, setGrowthRatePct] = useState<number>(1.5);

  const days = HORIZONS.find((h) => h.id === horizon)!.days;

  const data = useMemo(() => {
    const out: { day: number; date: string; cumulative: number; daily: number }[] = [];
    const cap = netDailyUSD * 3; // organic ramp caps at 3× steady state
    let cumulative = 0;
    const startDate = new Date();
    for (let d = 0; d <= days; d++) {
      // Ramp factor: starts low, grows toward 1 by ~day 45, capped at 3×
      const ramp = Math.min(
        3,
        0.15 + 0.85 * (1 - Math.pow(1 - growthRatePct / 100, d)),
      );
      const daily = Math.min(cap, netDailyUSD * ramp);
      cumulative += daily;
      const date = new Date(startDate.getTime() + d * 86400000);
      out.push({
        day: d,
        date: date.toISOString().slice(0, 10),
        cumulative: Number(cumulative.toFixed(2)),
        daily: Number(daily.toFixed(2)),
      });
    }
    return out;
  }, [netDailyUSD, days, growthRatePct]);

  const finalCumulative = data[data.length - 1]?.cumulative ?? 0;
  const peakDaily = Math.max(...data.map((p) => p.daily), 0);

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 mb-4 border-b border-slate-800">
        <div>
          <div className="text-xs font-mono text-emerald-400 uppercase tracking-wider mb-1 flex items-center gap-2">
            Cumulative Net Profit Timeline
            <span className="px-1.5 py-0.5 rounded bg-amber-950 text-amber-300 border border-amber-800 text-[9px] font-bold">
              MODELLED ASSUMPTION
            </span>
          </div>
          <h3 className="text-base font-bold text-white tracking-tight">
            Forward-Looking Revenue Runway (USD)
          </h3>
        </div>
        <div className="flex items-center gap-1 bg-slate-950 p-1 rounded-lg border border-slate-800 text-xs font-mono">
          {HORIZONS.map((h) => (
            <button
              key={h.id}
              onClick={() => setHorizon(h.id)}
              className={`px-2.5 py-1 rounded transition-colors ${
                horizon === h.id
                  ? "bg-emerald-600 text-white font-medium"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {h.label}
            </button>
          ))}
        </div>
      </div>

      {/* Growth rate slider */}
      <div className="mb-4 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="md:col-span-2">
          <div className="flex justify-between text-xs font-mono mb-1.5">
            <span className="text-slate-400">Daily organic discovery ramp:</span>
            <span className="text-emerald-400 font-bold">
              +{growthRatePct.toFixed(1)}% / day
            </span>
          </div>
          <input
            type="range"
            min="0"
            max="5"
            step="0.1"
            value={growthRatePct}
            onChange={(e) => setGrowthRatePct(parseFloat(e.target.value))}
            className="w-full accent-emerald-500 cursor-pointer"
            aria-label="Daily discovery growth rate"
          />
          <div className="flex justify-between text-[10px] font-mono text-slate-500">
            <span>0% (flat)</span>
            <span>1.5% (base)</span>
            <span>5% (viral)</span>
          </div>
        </div>
        <div className="grid grid-cols-2 gap-2 text-center font-mono text-xs">
          <div className="p-2 rounded-lg bg-slate-950 border border-slate-800">
            <div className="text-[10px] text-slate-400 uppercase">
              Cumulative @ {days}d
            </div>
            <div className="text-base font-bold text-emerald-400">
              ${finalCumulative.toLocaleString("en-US", { maximumFractionDigits: 0 })}
            </div>
          </div>
          <div className="p-2 rounded-lg bg-slate-950 border border-slate-800">
            <div className="text-[10px] text-slate-400 uppercase">
              Peak Daily
            </div>
            <div className="text-base font-bold text-white">
              ${peakDaily.toFixed(2)}
            </div>
          </div>
        </div>
      </div>

      <div className="h-64 w-full" role="img" aria-label="Cumulative net profit area chart">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart
            data={data}
            margin={{ top: 10, right: 10, bottom: 0, left: -10 }}
          >
            <defs>
              <linearGradient id="revTimelineGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#10b981" stopOpacity={0.5} />
                <stop offset="60%" stopColor="#10b981" stopOpacity={0.15} />
                <stop offset="100%" stopColor="#10b981" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="#1e293b"
              vertical={false}
            />
            <XAxis
              dataKey="day"
              stroke="#64748b"
              tick={{ fill: "#94a3b8", fontSize: 11, fontFamily: "monospace" }}
              tickLine={false}
              axisLine={{ stroke: "#1e293b" }}
              tickFormatter={(v) => `D${v}`}
              interval={Math.floor(days / 8)}
            />
            <YAxis
              stroke="#64748b"
              tick={{ fill: "#94a3b8", fontSize: 11, fontFamily: "monospace" }}
              tickLine={false}
              axisLine={{ stroke: "#1e293b" }}
              tickFormatter={(v) => `$${v >= 1000 ? `${(v / 1000).toFixed(1)}k` : v}`}
            />
            <Tooltip
              contentStyle={{
                background: "#0f172a",
                border: "1px solid #1e293b",
                borderRadius: "8px",
                fontSize: "12px",
                fontFamily: "monospace",
                color: "#e2e8f0",
              }}
              labelStyle={{ color: "#94a3b8" }}
              labelFormatter={(v) => `Day ${v} · ${data[Number(v)]?.date ?? ""}`}
              formatter={(value: number, name: string) => [
                `$${value.toFixed(2)}`,
                name === "cumulative" ? "Cumulative net" : "Daily net",
              ]}
            />
            <ReferenceLine
              y={0}
              stroke="#475569"
              strokeDasharray="2 2"
            />
            <Area
              type="monotone"
              dataKey="cumulative"
              name="cumulative"
              stroke="#10b981"
              strokeWidth={2}
              fill="url(#revTimelineGrad)"
              activeDot={{ r: 5, fill: "#0a0e15", stroke: "#34d399", strokeWidth: 2 }}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div className="mt-3 pt-3 border-t border-slate-800 text-[11px] text-slate-500 font-sans leading-relaxed">
        Model: daily net = steady-state net × ramp factor, where ramp grows at{" "}
        <span className="font-mono text-emerald-400">
          +{growthRatePct.toFixed(1)}%/day
        </span>{" "}
        from 0.15× and caps at 3× steady state. This is a{" "}
        <span className="text-amber-400 font-semibold">[MODELLED ASSUMPTION]</span>{" "}
        — actual revenue is confirmed only by on-chain USDC transfers to the
        receive-only payout address (see Live RPC Scanner tab).
      </div>
    </div>
  );
}
