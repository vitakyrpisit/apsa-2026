"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  ComposedChart,
  ReferenceLine,
} from "recharts";
import { ECONOMIC_SCENARIOS } from "@/lib/apsa/empirical-data";

const SCENARIO_COLORS: Record<string, string> = {
  CONSERVATIVE: "#f59e0b", // amber
  BASE: "#10b981", // emerald
  STRONG: "#ec4899", // pink — avoids the "indigo/blue" perception of violet
};

interface ScenarioDatum {
  name: string;
  daily: number;
  monthly: number;
  fill: string;
}

/**
 * RevenueProjectionChart — three-scenario bar+line chart showing projected
 * net monthly revenue (bars) and net daily revenue (line) across the
 * Conservative / Base / Strong scenarios from the empirical dataset.
 */
export function RevenueProjectionChart({
  ticketPrice,
  ordersPerDay,
  variableCostPerOrder,
  fixedMonthlyCost,
}: {
  ticketPrice: number;
  ordersPerDay: number;
  variableCostPerOrder: number;
  fixedMonthlyCost: number;
}) {
  // Build the live "CURRENT" scenario from the simulator sliders, plus
  // the 3 empirical benchmarks.
  const liveDaily =
    ticketPrice * ordersPerDay -
    variableCostPerOrder * ordersPerDay -
    fixedMonthlyCost / 30;
  const liveMonthly = liveDaily * 30;

  const data: ScenarioDatum[] = [
    ...ECONOMIC_SCENARIOS.map((s) => ({
      name: s.name,
      daily: Number(s.netPerDayUSD.toFixed(2)),
      monthly: Number(s.netPerMonthUSD.toFixed(2)),
      fill: SCENARIO_COLORS[s.name] ?? "#64748b",
    })),
    {
      name: "LIVE",
      daily: Number(liveDaily.toFixed(2)),
      monthly: Number(liveMonthly.toFixed(2)),
      fill: "#34d399",
    },
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
      <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-800">
        <div>
          <div className="text-xs font-mono text-emerald-400 uppercase tracking-wider mb-1">
            Revenue Projection Matrix
          </div>
          <h3 className="text-base font-bold text-white tracking-tight">
            Net Monthly &amp; Daily Revenue Scenarios (USD)
          </h3>
        </div>
        <div className="flex items-center gap-3 text-[11px] font-mono">
          <Legend2 color="#f59e0b" label="Conservative" />
          <Legend2 color="#10b981" label="Base" />
          <Legend2 color="#ec4899" label="Strong" />
          <Legend2 color="#34d399" label="Live (sliders)" />
        </div>
      </div>

      <div className="h-72 w-full" role="img" aria-label="Revenue projection bar chart">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart
            data={data}
            margin={{ top: 10, right: 10, bottom: 0, left: -10 }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="#1e293b"
              vertical={false}
            />
            <XAxis
              dataKey="name"
              stroke="#64748b"
              tick={{ fill: "#94a3b8", fontSize: 11, fontFamily: "monospace" }}
              tickLine={false}
              axisLine={{ stroke: "#1e293b" }}
            />
            <YAxis
              stroke="#64748b"
              tick={{ fill: "#94a3b8", fontSize: 11, fontFamily: "monospace" }}
              tickLine={false}
              axisLine={{ stroke: "#1e293b" }}
              tickFormatter={(v) => `$${v}`}
            />
            <Tooltip
              cursor={{ fill: "#1e293b40" }}
              contentStyle={{
                background: "#0f172a",
                border: "1px solid #1e293b",
                borderRadius: "8px",
                fontSize: "12px",
                fontFamily: "monospace",
                color: "#e2e8f0",
              }}
              labelStyle={{ color: "#94a3b8" }}
              formatter={(value: number, name: string) => [
                `$${value.toFixed(2)}`,
                name === "monthly" ? "Net / Month" : "Net / Day",
              ]}
            />
            <ReferenceLine y={0} stroke="#475569" strokeDasharray="2 2" />
            <Bar
              dataKey="monthly"
              name="monthly"
              radius={[6, 6, 0, 0]}
              maxBarSize={72}
            >
              {data.map((entry, idx) => (
                <Cell key={idx} fill={entry.fill} />
              ))}
            </Bar>
            <Line
              type="monotone"
              dataKey="daily"
              name="daily"
              stroke="#e2e8f0"
              strokeWidth={2}
              dot={{ r: 4, fill: "#0a0e15", stroke: "#e2e8f0", strokeWidth: 2 }}
              activeDot={{ r: 6 }}
            />
          </ComposedChart>
        </ResponsiveContainer>
      </div>

      <div className="mt-4 pt-3 border-t border-slate-800 grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono">
        {data.map((d) => (
          <div
            key={d.name}
            className="p-2.5 rounded-lg bg-slate-950 border border-slate-800"
          >
            <div className="flex items-center gap-1.5 mb-1">
              <span
                className="w-2 h-2 rounded-full"
                style={{ background: d.fill }}
              />
              <span className="text-slate-400 text-[10px] uppercase tracking-wider">
                {d.name}
              </span>
            </div>
            <div className="text-white font-bold">${d.monthly.toFixed(2)}</div>
            <div className="text-[10px] text-slate-500">/month</div>
            <div className="text-emerald-400 mt-1">${d.daily.toFixed(2)}/day</div>
          </div>
        ))}
      </div>
    </div>
  );
}

function Legend2({ color, label }: { color: string; label: string }) {
  return (
    <span className="flex items-center gap-1 text-slate-400">
      <span
        className="w-2.5 h-2.5 rounded-sm"
        style={{ background: color }}
      />
      {label}
    </span>
  );
}
