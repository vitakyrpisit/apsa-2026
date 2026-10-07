"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

interface RevenueBreakdownChartProps {
  ticketPrice: number;
  ordersPerDay: number;
  variableCostPerOrder: number;
  fixedMonthlyCost: number;
}

interface CostSlice {
  key: string;
  label: string;
  value: number; // daily cost
  color: string;
  vendor: string;
}

/**
 * RevenueBreakdownChart — per-day cost structure breakdown for the live
 * economics scenario. Shows each cost slice (DATA / LLM / COMPUTE / RPC /
 * HOSTING / FACILITATOR / FIXED) as a horizontal bar, plus the gross
 * revenue and net profit for context. The unit-economics simulator feeds
 * the live slider values.
 *
 * Cost proportions are derived from the empirical benchmark for the
 * SentinelShield $9.50 outcome (data $0.02, LLM $0.08, compute $0.02,
 * RPC $0.01, hosting $0.00, facilitator $0.01 per order) scaled to the
 * live ticket price so the relative shape is preserved.
 */
export function RevenueBreakdownChart({
  ticketPrice,
  ordersPerDay,
  variableCostPerOrder,
  fixedMonthlyCost,
}: RevenueBreakdownChartProps) {
  // Derive the per-order cost split from the live variableCostPerOrder,
  // using the SentinelShield benchmark proportions (8:8:2:2:0:2 → scaled).
  // Benchmark total = $0.14; we scale each slice proportionally.
  const benchmark = [
    { key: "data", label: "Data Ingestion", base: 0.02, color: "#34d399", vendor: "Public Base RPC + Scraper" },
    { key: "llm", label: "LLM Synthesis", base: 0.08, color: "#fbbf24", vendor: "Gemini 2.5 Flash" },
    { key: "compute", label: "Compute & AST", base: 0.02, color: "#fb7185", vendor: "Stateless Serverless" },
    { key: "rpc", label: "RPC Calls", base: 0.01, color: "#a78bfa", vendor: "Base JSON-RPC" },
    { key: "hosting", label: "Hosting", base: 0.0, color: "#64748b", vendor: "Free Tier" },
    { key: "facilitator", label: "Facilitator Gas", base: 0.01, color: "#2dd4bf", vendor: "Base L2 Relay" },
  ];
  const benchmarkTotal = benchmark.reduce((s, b) => s + b.base, 0) || 1;
  const perOrderSplits: CostSlice[] = benchmark.map((b) => ({
    key: b.key,
    label: b.label,
    value: Number(((b.base / benchmarkTotal) * variableCostPerOrder * ordersPerDay).toFixed(4)),
    color: b.color,
    vendor: b.vendor,
  }));
  const fixedDaily = fixedMonthlyCost / 30;
  const fixedSlice: CostSlice = {
    key: "fixed",
    label: "Fixed (hosting/domain)",
    value: Number(fixedDaily.toFixed(4)),
    color: "#94a3b8",
    vendor: "Monthly ÷ 30",
  };

  const grossDaily = ticketPrice * ordersPerDay;
  const totalVarDaily = perOrderSplits.reduce((s, c) => s + c.value, 0);
  const totalCostDaily = totalVarDaily + fixedDaily;
  const netDaily = grossDaily - totalCostDaily;

  // Chart data: gross, then each cost slice (negative for a waterfall feel),
  // then net.
  const chartData = [
    { name: "GROSS", value: Number(grossDaily.toFixed(2)), fill: "#10b981", isGross: true },
    ...perOrderSplits.map((s) => ({
      name: s.label.split(" ")[0].toUpperCase(),
      value: Number((-s.value).toFixed(3)),
      fill: s.color,
      vendor: s.vendor,
    })),
    { name: "FIXED", value: Number((-fixedDaily).toFixed(3)), fill: fixedSlice.color, vendor: fixedSlice.vendor },
    { name: "NET", value: Number(netDaily.toFixed(2)), fill: netDaily >= 0 ? "#34d399" : "#f43f5e", isNet: true },
  ];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 mb-4 border-b border-slate-800">
        <div>
          <div className="text-xs font-mono text-emerald-400 uppercase tracking-wider mb-1">
            Per-Day Cost Structure Breakdown
          </div>
          <h3 className="text-base font-bold text-white tracking-tight">
            Where Every Dollar Goes (Live Sliders)
          </h3>
        </div>
        <div className="flex items-center gap-3 text-[11px] font-mono">
          <span className="text-slate-400">
            Gross:{" "}
            <span className="text-emerald-400 font-bold">
              ${grossDaily.toFixed(2)}
            </span>
            /d
          </span>
          <span className="text-slate-400">
            Costs:{" "}
            <span className="text-rose-400 font-bold">
              -${totalCostDaily.toFixed(2)}
            </span>
            /d
          </span>
          <span className="text-slate-400">
            Net:{" "}
            <span
              className={`font-bold ${
                netDaily >= 0 ? "text-emerald-400" : "text-rose-400"
              }`}
            >
              +${netDaily.toFixed(2)}
            </span>
            /d
          </span>
        </div>
      </div>

      <div className="h-64 w-full" role="img" aria-label="Cost structure bar chart">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={chartData}
            layout="vertical"
            margin={{ top: 4, right: 16, bottom: 4, left: 8 }}
          >
            <CartesianGrid
              strokeDasharray="3 3"
              stroke="#1e293b"
              horizontal={false}
            />
            <XAxis
              type="number"
              stroke="#64748b"
              tick={{ fill: "#94a3b8", fontSize: 11, fontFamily: "monospace" }}
              tickLine={false}
              axisLine={{ stroke: "#1e293b" }}
              tickFormatter={(v) => `$${v}`}
            />
            <YAxis
              type="category"
              dataKey="name"
              stroke="#64748b"
              tick={{ fill: "#cbd5e1", fontSize: 10, fontFamily: "monospace" }}
              tickLine={false}
              axisLine={{ stroke: "#1e293b" }}
              width={88}
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
              formatter={(value: number, _name, item) => {
                const vendor = (item?.payload as { vendor?: string })?.vendor;
                const v = Number(value);
                return [
                  `${v >= 0 ? "+" : ""}$${Math.abs(v).toFixed(3)}/day${vendor ? ` · ${vendor}` : ""}`,
                  (item?.payload as { name?: string })?.name ?? "",
                ];
              }}
            />
            <Legend
              wrapperStyle={{ fontSize: "10px", fontFamily: "monospace" }}
              formatter={(value) => <span className="text-slate-400">{value}</span>}
            />
            <Bar dataKey="value" name="Daily USD" radius={[0, 4, 4, 0]} maxBarSize={26}>
              {chartData.map((entry, idx) => (
                <Cell key={idx} fill={entry.fill} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Cost-slice legend table */}
      <div className="mt-4 pt-3 border-t border-slate-800 grid grid-cols-2 sm:grid-cols-4 gap-2 text-[11px] font-mono">
        {perOrderSplits.map((s) => (
          <div key={s.key} className="flex items-center gap-1.5 text-slate-400">
            <span className="w-2.5 h-2.5 rounded-sm" style={{ background: s.color }} />
            <span className="truncate">{s.label}</span>
            <span className="ml-auto text-slate-300">${s.value.toFixed(3)}</span>
          </div>
        ))}
        <div className="flex items-center gap-1.5 text-slate-400">
          <span className="w-2.5 h-2.5 rounded-sm" style={{ background: fixedSlice.color }} />
          <span className="truncate">Fixed</span>
          <span className="ml-auto text-slate-300">${fixedSlice.value.toFixed(3)}</span>
        </div>
      </div>
    </div>
  );
}
