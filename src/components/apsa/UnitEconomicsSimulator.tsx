'use client';

import React, { useState } from 'react';
import { ECONOMIC_SCENARIOS } from '@/lib/apsa/empirical-data';
import type { EconomicScenario } from '@/lib/apsa/types';
import { Calculator, Sliders, ShieldCheck, RotateCcw, Layers, TrendingUp, PieChart, Clock, Grid3x3, ScrollText } from 'lucide-react';
import { RevenueProjectionChart } from './revenue-projection-chart';
import { RevenueTimelineChart } from './revenue-timeline-chart';
import { RevenueBreakdownChart } from './revenue-breakdown-chart';
import { RevenueSensitivityChart } from './revenue-sensitivity-chart';
import { SubSectionNav, type SubSection } from './sub-section-nav';
import { useLocalStorage } from '@/hooks/use-local-storage';
import { toast } from 'sonner';

const ECON_SUBSECTIONS: SubSection[] = [
  { id: 'econ-scenarios', label: 'Scenarios', icon: Layers },
  { id: 'econ-simulator', label: 'Simulator', icon: Sliders },
  { id: 'econ-projection', label: 'Projection', icon: TrendingUp },
  { id: 'econ-breakdown', label: 'Cost Breakdown', icon: PieChart },
  { id: 'econ-sensitivity', label: 'Sensitivity', icon: Grid3x3 },
  { id: 'econ-timeline', label: 'Timeline', icon: Clock },
  { id: 'econ-audit', label: 'Audit', icon: ScrollText },
];

export const UnitEconomicsSimulator: React.FC = () => {
  const [selectedPreset, setSelectedPreset] = useLocalStorage<'CONSERVATIVE' | 'BASE' | 'STRONG'>('apsa:econ:preset', 'BASE');
  const [ticketPrice, setTicketPrice] = useLocalStorage<number>('apsa:econ:ticketPrice', 8.25);
  const [ordersPerDay, setOrdersPerDay] = useLocalStorage<number>('apsa:econ:ordersPerDay', 10);
  const [variableCostPerOrder, setVariableCostPerOrder] = useLocalStorage<number>('apsa:econ:variableCost', 0.125);
  const [fixedMonthlyCost, setFixedMonthlyCost] = useLocalStorage<number>('apsa:econ:fixedMonthly', 10.00);
  // ephemeral UI state (not persisted)
  const [resetTick, setResetTick] = useState(0);

  // Calculated metrics
  const grossDaily = ticketPrice * ordersPerDay;
  const variableDaily = variableCostPerOrder * ordersPerDay;
  const fixedDaily = fixedMonthlyCost / 30;
  const netDaily = grossDaily - variableDaily - fixedDaily;
  const netMonthly = netDaily * 30;
  const netMarginPct = ((netDaily / (grossDaily || 1)) * 100);

  const applyPreset = (preset: 'CONSERVATIVE' | 'BASE' | 'STRONG') => {
    setSelectedPreset(preset);
    if (preset === 'CONSERVATIVE') {
      setTicketPrice(8.25);
      setOrdersPerDay(2);
      setVariableCostPerOrder(0.125);
      setFixedMonthlyCost(10.00);
    } else if (preset === 'BASE') {
      setTicketPrice(8.25);
      setOrdersPerDay(10);
      setVariableCostPerOrder(0.125);
      setFixedMonthlyCost(10.00);
    } else {
      setTicketPrice(8.25);
      setOrdersPerDay(35);
      setVariableCostPerOrder(0.125);
      setFixedMonthlyCost(15.00);
    }
  };

  const handleReset = () => {
    setSelectedPreset('BASE');
    setTicketPrice(8.25);
    setOrdersPerDay(10);
    setVariableCostPerOrder(0.125);
    setFixedMonthlyCost(10.00);
    setResetTick((t) => t + 1);
    toast.success('Economics reset to Base scenario defaults', {
      description: 'Saved slider values cleared from localStorage.',
    });
  };

  return (
    <div className="space-y-8">

      {/* Overview Banner */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
        <div className="flex items-center gap-2 text-xs text-emerald-400 font-mono uppercase tracking-wider mb-1">
          <Calculator className="w-4 h-4" />
          <span>Section 13, 16 &amp; 17: Financial Forensics &amp; Projections</span>
        </div>
        <h2 className="text-xl font-bold text-white tracking-tight">
          Unit Economics, Scenario Modeling &amp; Outcome Value Matrix
        </h2>
        <p className="text-xs text-slate-400 mt-1 max-w-3xl">
          Real net profit requires subtracting all infrastructure deductions (Inference, RPC, Hosting, Compute, Facilitator relay fees). All scenarios below are explicitly tagged: <span className="text-amber-400 font-mono font-semibold">[MODELLED ASSUMPTION]</span> vs <span className="text-emerald-400 font-mono font-semibold">[ON-CHAIN FACT]</span>.
        </p>
      </div>

      {/* Sub-section sticky nav for this long tab */}
      <SubSectionNav sections={ECON_SUBSECTIONS} title="Jump to" />

      {/* THREE SCENARIOS COMPARISON CARDS (SECTION 16) */}
      <div id="econ-scenarios" className="grid grid-cols-1 md:grid-cols-3 gap-4 scroll-mt-[150px]">
        {ECONOMIC_SCENARIOS.map((sc: EconomicScenario) => (
          <div
            key={sc.name}
            onClick={() => applyPreset(sc.name)}
            className={`p-4 rounded-xl border cursor-pointer transition-all ${
              selectedPreset === sc.name
                ? 'bg-slate-900 border-emerald-500 shadow-md ring-1 ring-emerald-500/20'
                : 'bg-slate-900/70 border-slate-800 hover:border-slate-700'
            }`}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800">
                {sc.name} SCENARIO
              </span>
              <span className="text-[10px] font-mono text-amber-400 font-bold">
                [{sc.nature}]
              </span>
            </div>

            <div className="my-3">
              <div className="text-[10px] font-mono text-slate-400 uppercase">Projected Net Monthly</div>
              <div className="text-2xl font-bold font-mono text-emerald-400">
                +${sc.netPerMonthUSD.toFixed(2)}
              </div>
              <div className="text-xs font-mono text-slate-300 mt-0.5">
                +${sc.netPerDayUSD.toFixed(2)} net / day ({sc.ordersPerDay} orders/day @ ${sc.averageTicketUSDC.toFixed(2)})
              </div>
            </div>

            <div className="pt-2 border-t border-slate-800 text-[11px] text-slate-400 font-sans leading-relaxed">
              {sc.notes}
            </div>
          </div>
        ))}
      </div>

      {/* INTERACTIVE DYNAMIC SIMULATOR SLIDERS */}
      <div id="econ-simulator" className="bg-slate-900 border border-slate-800 rounded-xl p-5 scroll-mt-[150px]">
        <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <Sliders className="w-4 h-4 text-emerald-400" />
            <h3 className="text-sm font-bold text-white uppercase tracking-wider font-mono">
              Dynamic Variable &amp; Fixed Economics Simulator
            </h3>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-xs text-emerald-400/80 font-mono flex items-center gap-1" title="Slider values are saved in your browser">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 apsa-live-dot" />
              auto-saved
            </span>
            <span className="text-xs text-slate-400 font-mono hidden sm:inline">
              Interactive Parametric Modeling
            </span>
            <button
              onClick={handleReset}
              key={resetTick}
              className="px-2.5 py-1 text-xs font-mono rounded-md bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white border border-slate-700 flex items-center gap-1.5 transition-colors"
              title="Reset to Base scenario defaults"
            >
              <RotateCcw className="w-3 h-3" />
              Reset
            </button>
          </div>
        </div>

        {/* Sliders Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">

          {/* Average Ticket */}
          <div className="space-y-2">
            <div className="flex justify-between text-xs font-mono">
              <span className="text-slate-400">Average Outcome Ticket:</span>
              <span className="text-white font-bold">${ticketPrice.toFixed(2)} USDC</span>
            </div>
            <input
              type="range"
              min="1.00"
              max="25.00"
              step="0.25"
              value={ticketPrice}
              onChange={(e) => setTicketPrice(parseFloat(e.target.value))}
              className="w-full accent-emerald-500 cursor-pointer"
            />
            <div className="flex justify-between text-[10px] font-mono text-slate-400">
              <span>$1.00 (Micro)</span>
              <span>$8.25 (Avg)</span>
              <span>$25.00 (Enterprise)</span>
            </div>
          </div>

          {/* Orders Per Day */}
          <div className="space-y-2">
            <div className="flex justify-between text-xs font-mono">
              <span className="text-slate-400">Paid External Orders / Day:</span>
              <span className="text-white font-bold">{ordersPerDay} orders</span>
            </div>
            <input
              type="range"
              min="1"
              max="50"
              step="1"
              value={ordersPerDay}
              onChange={(e) => setOrdersPerDay(parseInt(e.target.value))}
              className="w-full accent-emerald-500 cursor-pointer"
            />
            <div className="flex justify-between text-[10px] font-mono text-slate-400">
              <span>1 (Conservative)</span>
              <span>15 (Base)</span>
              <span>50 (Strong)</span>
            </div>
          </div>

          {/* Variable Cost per Order */}
          <div className="space-y-2">
            <div className="flex justify-between text-xs font-mono">
              <span className="text-slate-400">Variable Marginal Cost / Order:</span>
              <span className="text-rose-400 font-bold">${variableCostPerOrder.toFixed(3)}</span>
            </div>
            <input
              type="range"
              min="0.02"
              max="0.50"
              step="0.01"
              value={variableCostPerOrder}
              onChange={(e) => setVariableCostPerOrder(parseFloat(e.target.value))}
              className="w-full accent-emerald-500 cursor-pointer"
            />
            <div className="flex justify-between text-[10px] font-mono text-slate-400">
              <span>$0.02 (Fast)</span>
              <span>$0.125 (Deep)</span>
              <span>$0.50 (Heavy AST)</span>
            </div>
          </div>

        </div>

        {/* Live Simulation Results Strip */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-center font-mono">
          <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
            <div className="text-[10px] text-slate-400 uppercase">Gross Revenue / Day</div>
            <div className="text-lg font-bold text-white mt-1">${grossDaily.toFixed(2)}</div>
            <div className="text-[10px] text-slate-400">${(grossDaily * 30).toFixed(2)} / mo</div>
          </div>

          <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
            <div className="text-[10px] text-slate-400 uppercase">Total Costs / Day</div>
            <div className="text-lg font-bold text-rose-400 mt-1">-${(variableDaily + fixedDaily).toFixed(2)}</div>
            <div className="text-[10px] text-slate-400">Var: ${variableDaily.toFixed(2)} · Fix: ${fixedDaily.toFixed(2)}</div>
          </div>

          <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
            <div className="text-[10px] text-slate-400 uppercase">Net Realized / Day</div>
            <div className="text-lg font-bold text-emerald-400 mt-1">+${netDaily.toFixed(2)}</div>
            <div className="text-[10px] text-emerald-400 font-semibold">{netMarginPct.toFixed(1)}% margin</div>
          </div>

          <div className="p-3 rounded-lg bg-slate-950 border border-slate-800">
            <div className="text-[10px] text-slate-400 uppercase">Net Realized / Month</div>
            <div className="text-xl font-bold text-emerald-400 mt-1">+${netMonthly.toFixed(2)}</div>
            <div className="text-[10px] text-emerald-300">Sustainable Run-Rate</div>
          </div>
        </div>

      </div>

      {/* REVENUE PROJECTION CHART (live slider-driven + 3 empirical scenarios) */}
      <div id="econ-projection" className="scroll-mt-[150px]">
        <RevenueProjectionChart
          ticketPrice={ticketPrice}
          ordersPerDay={ordersPerDay}
          variableCostPerOrder={variableCostPerOrder}
          fixedMonthlyCost={fixedMonthlyCost}
        />
      </div>

      {/* REVENUE BREAKDOWN CHART (per-day cost structure) */}
      <div id="econ-breakdown" className="scroll-mt-[150px]">
        <RevenueBreakdownChart
          ticketPrice={ticketPrice}
          ordersPerDay={ordersPerDay}
          variableCostPerOrder={variableCostPerOrder}
          fixedMonthlyCost={fixedMonthlyCost}
        />
      </div>

      {/* REVENUE SENSITIVITY CHART (2D heatmap) */}
      <div id="econ-sensitivity" className="scroll-mt-[150px]">
        <RevenueSensitivityChart
          ticketPrice={ticketPrice}
          ordersPerDay={ordersPerDay}
          variableCostPerOrder={variableCostPerOrder}
          fixedMonthlyCost={fixedMonthlyCost}
        />
      </div>

      {/* REVENUE TIMELINE CHART (cumulative forward-looking projection) */}
      <div id="econ-timeline" className="scroll-mt-[150px]">
        <RevenueTimelineChart netDailyUSD={netDaily} />
      </div>

      {/* SECTION 17: OUTCOME VS TECHNOLOGY VERIFICATION MATRIX */}
      <div id="econ-audit" className="bg-slate-900 border border-slate-800 rounded-xl p-5 scroll-mt-[150px]">
        <div className="flex items-center gap-2 text-xs text-emerald-400 font-mono uppercase tracking-wider mb-1">
          <ShieldCheck className="w-4 h-4" />
          <span>Section 17: What Is the Customer Actually Buying?</span>
        </div>
        <h3 className="text-base font-bold text-white tracking-tight mb-2">
          De-commoditization Audit: Outcome vs. Raw Technical Pass-Through
        </h3>
        <p className="text-xs text-slate-400 mb-4 max-w-3xl">
          Autonomous buyer agents will not pay for what they can do themselves for free (e.g. querying a public RPC or pinging an API). They pay exclusively for <strong className="text-white">completed, risk-reducing, decision-ready outcomes</strong>.
        </p>

        <div className="overflow-x-auto border border-slate-800 rounded-lg text-xs font-mono">
          <table className="w-full text-left text-slate-300">
            <thead className="bg-slate-950 text-slate-400 uppercase text-[10px]">
              <tr>
                <th className="py-2.5 px-3">Service Domain</th>
                <th className="py-2.5 px-3 text-rose-400">NOT Buying (Raw Tech)</th>
                <th className="py-2.5 px-3 text-emerald-400">ACTUALLY Buying (Real Outcome)</th>
                <th className="py-2.5 px-3">Price Disparity</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              <tr>
                <td className="py-2.5 px-3 font-semibold text-white">Smart Contract Security</td>
                <td className="py-2.5 px-3 text-rose-300">"Raw Slither static analysis JSON dump"</td>
                <td className="py-2.5 px-3 text-emerald-300">"Validated blocking risk gate &amp; exploit remediation patch"</td>
                <td className="py-2.5 px-3 text-emerald-300">$0.001 vs $9.50 (9,500x)</td>
              </tr>
              <tr>
                <td className="py-2.5 px-3 font-semibold text-white">B2B Corporate Research</td>
                <td className="py-2.5 px-3 text-rose-300">"Web search or raw HTML scrape"</td>
                <td className="py-2.5 px-3 text-emerald-300">"Decision-ready diligence dossier with verified executive leads"</td>
                <td className="py-2.5 px-3 text-emerald-300">$0.0005 vs $7.00 (14,000x)</td>
              </tr>
              <tr>
                <td className="py-2.5 px-3 font-semibold text-white">DeFi Liquidity &amp; Yield</td>
                <td className="py-2.5 px-3 text-rose-300">"Token price or pool APR number"</td>
                <td className="py-2.5 px-3 text-emerald-300">"Toxic MEV flow &amp; impermanent loss risk attestation"</td>
                <td className="py-2.5 px-3 text-emerald-300">$0.0001 vs $5.50 (55,000x)</td>
              </tr>
              <tr>
                <td className="py-2.5 px-3 font-semibold text-white">Legal &amp; Compliance</td>
                <td className="py-2.5 px-3 text-rose-300">"Raw sanctions list text search"</td>
                <td className="py-2.5 px-3 text-emerald-300">"Cryptographically signed OFAC/AML taint clearance attestation"</td>
                <td className="py-2.5 px-3 text-emerald-300">$0.005 vs $4.00 (800x)</td>
              </tr>
            </tbody>
          </table>
        </div>

      </div>

    </div>
  );
};
