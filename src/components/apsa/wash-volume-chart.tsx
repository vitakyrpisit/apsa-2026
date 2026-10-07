"use client";

import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";
import { MAJOR_SELLER_AUDITS } from "@/lib/apsa/empirical-data";

/**
 * WashVolumeChart — a donut chart breaking down the ecosystem-wide
 * wash vs external (E3–E5) settlement volume split, plus a per-seller
 * breakdown panel. Reads directly from the empirical audit dataset.
 */
export function WashVolumeChart() {
  // Aggregate across all audited sellers.
  const totalReported = MAJOR_SELLER_AUDITS.reduce(
    (sum, s) => sum + s.totalReportedVolumeUSDC,
    0,
  );
  const totalExternal = MAJOR_SELLER_AUDITS.reduce(
    (sum, s) => sum + s.externalVolumeUSDC,
    0,
  );
  const totalWash = Math.max(0, totalReported - totalExternal);
  const washPct = totalReported > 0 ? (totalWash / totalReported) * 100 : 0;
  const externalPct = 100 - washPct;

  const donutData = [
    { name: "Wash / Sybil (E0–E2)", value: Number(totalWash.toFixed(2)), color: "#f43f5e" },
    { name: "External (E3–E5)", value: Number(totalExternal.toFixed(2)), color: "#10b981" },
  ];

  // Per-seller mini breakdown (top 6 by reported volume).
  const perSeller = [...MAJOR_SELLER_AUDITS]
    .sort((a, b) => b.totalReportedVolumeUSDC - a.totalReportedVolumeUSDC)
    .slice(0, 6)
    .map((s) => ({
      name: s.sellerName,
      external: Number(s.externalVolumeUSDC.toFixed(2)),
      wash: Number(Math.max(0, s.totalReportedVolumeUSDC - s.externalVolumeUSDC).toFixed(2)),
    }));

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Donut */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="text-xs font-mono text-rose-400 uppercase tracking-wider mb-1">
          Ecosystem Wash vs External Volume
        </div>
        <h3 className="text-base font-bold text-white tracking-tight mb-3">
          {washPct.toFixed(1)}% Wash · {externalPct.toFixed(1)}% Independent
        </h3>
        <div className="relative h-60">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={donutData}
                dataKey="value"
                nameKey="name"
                innerRadius={62}
                outerRadius={92}
                paddingAngle={3}
                stroke="#0a0e15"
                strokeWidth={2}
              >
                {donutData.map((entry, idx) => (
                  <Cell key={idx} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  background: "#0f172a",
                  border: "1px solid #1e293b",
                  borderRadius: "8px",
                  fontSize: "12px",
                  fontFamily: "monospace",
                  color: "#e2e8f0",
                }}
                formatter={(value: number, name: string) => [
                  `$${value.toFixed(2)} (${((value / totalReported) * 100).toFixed(1)}%)`,
                  name,
                ]}
              />
            </PieChart>
          </ResponsiveContainer>
          {/* Center label */}
          <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
            <div className="text-[10px] text-slate-400 font-mono uppercase tracking-wider">
              Total Audited
            </div>
            <div className="text-xl font-mono font-bold text-white">
              ${totalReported.toFixed(0)}
            </div>
            <div className="text-[10px] text-slate-500 font-mono">
              USDC volume
            </div>
          </div>
        </div>
        <div className="mt-3 flex items-center justify-center gap-5 text-[11px] font-mono">
          <span className="flex items-center gap-1.5 text-rose-300">
            <span className="w-2.5 h-2.5 rounded-sm bg-rose-500" />
            Wash ${totalWash.toFixed(0)}
          </span>
          <span className="flex items-center gap-1.5 text-emerald-300">
            <span className="w-2.5 h-2.5 rounded-sm bg-emerald-500" />
            External ${totalExternal.toFixed(0)}
          </span>
        </div>
      </div>

      {/* Per-seller stacked bars */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="text-xs font-mono text-emerald-400 uppercase tracking-wider mb-1">
          Per-Seller Volume Breakdown
        </div>
        <h3 className="text-base font-bold text-white tracking-tight mb-4">
          External vs Wash Volume by Seller (Top 6)
        </h3>
        <div className="space-y-2.5">
          {perSeller.map((s) => {
            const total = s.external + s.wash;
            const externalPct = total > 0 ? (s.external / total) * 100 : 0;
            const washPct = 100 - externalPct;
            return (
              <div key={s.name}>
                <div className="flex items-center justify-between text-[11px] font-mono mb-1">
                  <span className="text-slate-200 font-medium truncate pr-2">
                    {s.name}
                  </span>
                  <span className="text-slate-400 whitespace-nowrap">
                    ${total.toFixed(0)}
                  </span>
                </div>
                <div className="flex h-2.5 rounded-full overflow-hidden bg-slate-950 border border-slate-800">
                  <div
                    className="bg-emerald-500 transition-all duration-500"
                    style={{ width: `${externalPct}%` }}
                    title={`External: $${s.external.toFixed(2)} (${externalPct.toFixed(1)}%)`}
                  />
                  <div
                    className="bg-rose-500 transition-all duration-500"
                    style={{ width: `${washPct}%` }}
                    title={`Wash: $${s.wash.toFixed(2)} (${washPct.toFixed(1)}%)`}
                  />
                </div>
              </div>
            );
          })}
        </div>
        <div className="mt-4 pt-3 border-t border-slate-800 text-[11px] text-slate-400 font-sans leading-relaxed">
          Only <span className="text-emerald-400 font-semibold">E3–E5 external</span>{" "}
          volume is admitted into economic calculations. E0–E2 wash settlements
          are excluded as non-economic noise per the protocol&apos;s forensic gate.
        </div>
      </div>
    </div>
  );
}
