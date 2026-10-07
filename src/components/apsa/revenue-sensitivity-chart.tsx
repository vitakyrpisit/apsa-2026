"use client";

import { useMemo, useState } from "react";

interface RevenueSensitivityChartProps {
  ticketPrice: number;
  ordersPerDay: number;
  variableCostPerOrder: number;
  fixedMonthlyCost: number;
}

const PRICE_STEPS = [2, 4, 6, 8, 10, 12, 15, 20, 25];
const ORDERS_STEPS = [1, 3, 5, 10, 15, 25, 35, 50];

/**
 * RevenueSensitivityChart — a 2D heatmap of projected monthly net profit
 * across a grid of ticketPrice (rows) × ordersPerDay (columns). Each cell
 * is color-coded from rose (loss) → amber (thin) → emerald (strong). The
 * current slider position is highlighted with a ring.
 *
 * Helps the operator see the full sensitivity surface at a glance and
 * identify the "sweet spot" combinations.
 */
export function RevenueSensitivityChart({
  ticketPrice,
  ordersPerDay,
  variableCostPerOrder,
  fixedMonthlyCost,
}: RevenueSensitivityChartProps) {
  const [hover, setHover] = useState<{ r: number; c: number } | null>(null);

  const grid = useMemo(() => {
    const fixedDaily = fixedMonthlyCost / 30;
    return PRICE_STEPS.map((price) =>
      ORDERS_STEPS.map((orders) => {
        const grossDaily = price * orders;
        const varDaily = variableCostPerOrder * orders;
        const netDaily = grossDaily - varDaily - fixedDaily;
        const netMonthly = netDaily * 30;
        return Number(netMonthly.toFixed(2));
      }),
    );
  }, [variableCostPerOrder, fixedMonthlyCost]);

  // Color scale: find min/max for normalization.
  const flat = grid.flat();
  const min = Math.min(...flat, 0);
  const max = Math.max(...flat, 1);
  const range = max - min || 1;

  function colorFor(value: number): { bg: string; text: string } {
    if (value < 0) {
      // Loss: rose scale
      const intensity = Math.min(1, Math.abs(value) / Math.abs(min || 1));
      const opacity = 0.25 + intensity * 0.5;
      return { bg: `rgba(244, 63, 94, ${opacity})`, text: "#fecdd3" };
    }
    // Profit: amber → emerald scale based on intensity
    const intensity = (value - min) / range;
    if (intensity < 0.33) {
      const o = 0.2 + intensity * 0.6;
      return { bg: `rgba(245, 158, 11, ${o})`, text: "#fde68a" };
    }
    const o = 0.25 + (intensity - 0.33) * 0.7;
    return { bg: `rgba(16, 185, 129, ${o})`, text: "#a7f3d0" };
  }

  // Find the current-slider cell (closest step).
  const currentPriceIdx = PRICE_STEPS.reduce(
    (best, p, i) =>
      Math.abs(p - ticketPrice) < Math.abs(PRICE_STEPS[best] - ticketPrice)
        ? i
        : best,
    0,
  );
  const currentOrdersIdx = ORDERS_STEPS.reduce(
    (best, o, i) =>
      Math.abs(o - ordersPerDay) < Math.abs(ORDERS_STEPS[best] - ordersPerDay)
        ? i
        : best,
    0,
  );

  const hoverValue = hover ? grid[hover.r][hover.c] : null;
  const hoverPrice = hover ? PRICE_STEPS[hover.r] : null;
  const hoverOrders = hover ? ORDERS_STEPS[hover.c] : null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 mb-4 border-b border-slate-800">
        <div>
          <div className="text-xs font-mono text-emerald-400 uppercase tracking-wider mb-1">
            Profitability Sensitivity Surface
          </div>
          <h3 className="text-base font-bold text-white tracking-tight">
            Net Monthly Profit — Ticket Price × Orders/Day
          </h3>
        </div>
        <div className="flex items-center gap-3 text-[11px] font-mono">
          <span className="flex items-center gap-1.5 text-slate-400">
            <span className="w-3 h-3 rounded-sm" style={{ background: "rgba(244,63,94,0.55)" }} />
            Loss
          </span>
          <span className="flex items-center gap-1.5 text-slate-400">
            <span className="w-3 h-3 rounded-sm" style={{ background: "rgba(245,158,11,0.5)" }} />
            Thin
          </span>
          <span className="flex items-center gap-1.5 text-slate-400">
            <span className="w-3 h-3 rounded-sm" style={{ background: "rgba(16,185,129,0.6)" }} />
            Strong
          </span>
        </div>
      </div>

      {/* Heatmap grid */}
      <div className="overflow-x-auto pb-2">
        <div className="inline-block min-w-full">
          {/* Column headers (orders/day) */}
          <div
            className="grid gap-1 mb-1"
            style={{
              gridTemplateColumns: `60px repeat(${ORDERS_STEPS.length}, minmax(52px, 1fr))`,
            }}
          >
            <div className="text-[9px] font-mono text-slate-500 uppercase text-right pr-2 self-end">
              $/ord ↓ · ord/d →
            </div>
            {ORDERS_STEPS.map((o) => (
              <div
                key={o}
                className="text-[10px] font-mono text-slate-400 text-center py-1"
              >
                {o}
              </div>
            ))}
          </div>

          {/* Rows */}
          {PRICE_STEPS.map((price, r) => (
            <div
              key={price}
              className="grid gap-1 mb-1"
              style={{
                gridTemplateColumns: `60px repeat(${ORDERS_STEPS.length}, minmax(52px, 1fr))`,
              }}
            >
              <div className="text-[10px] font-mono text-slate-400 text-right pr-2 self-center">
                ${price}
              </div>
              {ORDERS_STEPS.map((orders, c) => {
                const value = grid[r][c];
                const { bg, text } = colorFor(value);
                const isCurrent =
                  r === currentPriceIdx && c === currentOrdersIdx;
                const isHover = hover && hover.r === r && hover.c === c;
                return (
                  <div
                    key={c}
                    onMouseEnter={() => setHover({ r, c })}
                    onMouseLeave={() => setHover(null)}
                    className={`h-10 rounded flex items-center justify-center text-[10px] font-mono font-semibold cursor-default transition-all ${
                      isCurrent
                        ? "ring-2 ring-emerald-300 ring-offset-1 ring-offset-slate-900"
                        : isHover
                          ? "ring-1 ring-slate-400"
                          : ""
                    }`}
                    style={{ background: bg, color: text }}
                    title={`$${price}/order × ${orders}/day = $${value.toLocaleString()}/mo`}
                  >
                    {value >= 1000
                      ? `$${(value / 1000).toFixed(1)}k`
                      : value >= 0
                        ? `$${value.toFixed(0)}`
                        : `-$${Math.abs(value).toFixed(0)}`}
                  </div>
                );
              })}
            </div>
          ))}
        </div>
      </div>

      {/* Hover / current readout */}
      <div className="mt-3 pt-3 border-t border-slate-800 flex flex-wrap items-center justify-between gap-3 text-[11px] font-mono">
        <div className="text-slate-400">
          {hover !== null && hoverValue !== null ? (
            <span>
              <span className="text-slate-300">${hoverPrice}</span>/order ×{" "}
              <span className="text-slate-300">{hoverOrders}</span>/day →{" "}
              <span
                className={`font-bold ${
                  hoverValue >= 0 ? "text-emerald-400" : "text-rose-400"
                }`}
              >
                ${hoverValue.toLocaleString()}/mo
              </span>
            </span>
          ) : (
            <span className="text-slate-500">
              Hover any cell for details · ring = current slider position
            </span>
          )}
        </div>
        <div className="text-slate-400">
          Current:{" "}
          <span className="text-emerald-400 font-bold">
            ${grid[currentPriceIdx][currentOrdersIdx].toLocaleString()}/mo
          </span>{" "}
          (${ticketPrice.toFixed(2)} × {ordersPerDay}/d)
        </div>
      </div>
    </div>
  );
}
