'use client';

import React from 'react';
import { DollarSign, ShieldAlert, TrendingUp, Cpu, Activity } from 'lucide-react';
import type { OnChainWalletStatus } from '@/lib/apsa/base-rpc';
import { AnimatedNumber } from './animated-number';
import { FadeIn } from './fade-in';

interface MetricCardsProps {
  walletStatus: OnChainWalletStatus | null;
  onOpenLiveScanner: () => void;
}

type Accent = 'emerald' | 'rose' | 'teal' | 'amber';

const ACCENT_STYLES: Record<
  Accent,
  {
    glow: string;
    border: string;
    iconWrap: string;
    valueText: string;
    spark: string[];
    sparkLine: string;
  }
> = {
  emerald: {
    glow: 'before:from-emerald-500/20',
    border: 'border-emerald-500/20 hover:border-emerald-400/40',
    iconWrap: 'bg-emerald-950/80 border-emerald-500/30 text-emerald-400',
    valueText: 'text-white',
    spark: ['#064e3b', '#065f46', '#047857', '#059669', '#10b981', '#34d399', '#6ee7b7'],
    sparkLine: '#34d399',
  },
  rose: {
    glow: 'before:from-rose-500/20',
    border: 'border-rose-500/20 hover:border-rose-400/40',
    iconWrap: 'bg-rose-950/80 border-rose-500/30 text-rose-400',
    valueText: 'text-rose-400',
    spark: ['#7f1d1d', '#9f1239', '#be123c', '#e11d48', '#f43f5e', '#fb7185', '#fda4af'],
    sparkLine: '#fb7185',
  },
  teal: {
    glow: 'before:from-teal-500/20',
    border: 'border-teal-500/20 hover:border-teal-400/40',
    iconWrap: 'bg-teal-950/80 border-teal-500/30 text-teal-400',
    valueText: 'text-teal-300',
    spark: ['#134e4a', '#0f3a36', '#115e59', '#0d9488', '#14b8a6', '#2dd4bf', '#5eead4'],
    sparkLine: '#2dd4bf',
  },
  amber: {
    glow: 'before:from-amber-500/20',
    border: 'border-amber-500/20 hover:border-amber-400/40',
    iconWrap: 'bg-amber-950/80 border-amber-500/30 text-amber-400',
    valueText: 'text-amber-300',
    spark: ['#451a03', '#78350f', '#92400e', '#b45309', '#d97706', '#f59e0b', '#fbbf24'],
    sparkLine: '#fbbf24',
  },
};

interface CardDef {
  kpi: string;
  icon: React.ReactNode;
  accent: Accent;
  value: React.ReactNode;
  sub: React.ReactNode;
  footerLabel: string;
  footerValue: React.ReactNode;
  footerTone?: 'emerald' | 'amber' | 'rose' | 'slate';
  sparkSeed: number;
}

/** Tiny deterministic sparkline using a seeded pseudo-random walk. */
function Sparkline({ colors, line, seed }: { colors: string[]; line: string; seed: number }) {
  const points = React.useMemo(() => {
    const pts: number[] = [];
    let v = 0.5;
    let s = seed;
    const rand = () => {
      s = (s * 9301 + 49297) % 233280;
      return s / 233280;
    };
    for (let i = 0; i < 12; i++) {
      v += (rand() - 0.45) * 0.18;
      v = Math.max(0.08, Math.min(0.92, v));
      pts.push(v);
    }
    return pts;
  }, [seed]);

  const w = 80;
  const h = 28;
  const step = w / (points.length - 1);
  const path = points
    .map((p, i) => `${i === 0 ? 'M' : 'L'} ${(i * step).toFixed(1)} ${(h - p * h).toFixed(1)}`)
    .join(' ');
  const area = `${path} L ${w} ${h} L 0 ${h} Z`;
  const gradId = `spark-${seed}`;

  return (
    <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`} className="opacity-80" aria-hidden="true">
      <defs>
        <linearGradient id={gradId} x1="0" y1="0" x2="0" y2="1">
          {colors.map((c, i) => (
            <stop key={i} offset={`${(i / (colors.length - 1)) * 100}%`} stopColor={c} stopOpacity={0.55 - i * 0.05} />
          ))}
        </linearGradient>
      </defs>
      <path d={area} fill={`url(#${gradId})`} />
      <path d={path} fill="none" stroke={line} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

function MetricCard({ card }: { card: CardDef }) {
  const s = ACCENT_STYLES[card.accent];
  return (
    <div
      className={`group relative p-4 rounded-xl bg-slate-900/80 border ${s.border} flex flex-col justify-between overflow-hidden transition-all duration-300 hover:-translate-y-0.5 hover:shadow-lg hover:shadow-black/40 before:absolute before:inset-0 before:bg-gradient-to-br ${s.glow} before:to-transparent before:opacity-0 hover:before:opacity-100 before:transition-opacity before:duration-300 before:pointer-events-none`}
    >
      <div className="relative flex items-center justify-between text-xs text-slate-400 mb-2">
        <span className="font-medium tracking-wide uppercase text-[11px]">
          {card.kpi}
        </span>
        <span className={`w-7 h-7 rounded-lg border flex items-center justify-center ${s.iconWrap}`}>
          {card.icon}
        </span>
      </div>

      <div className="relative">
        <div className="flex items-end justify-between gap-2">
          <div className="flex items-baseline gap-1.5">
            <span className={`text-2xl font-mono font-bold ${s.valueText}`}>
              {card.value}
            </span>
          </div>
          <div className="opacity-60 group-hover:opacity-100 transition-opacity">
            <Sparkline colors={s.spark} line={s.sparkLine} seed={card.sparkSeed} />
          </div>
        </div>
        <div className="text-[11px] text-slate-400 mt-1">{card.sub}</div>
      </div>

      <div className="relative mt-3 pt-2 border-t border-slate-800/80 text-[11px] text-slate-400 flex items-center justify-between">
        <span>{card.footerLabel}</span>
        <span
          className={`font-mono font-semibold ${
            card.footerTone === 'emerald'
              ? 'text-emerald-400'
              : card.footerTone === 'amber'
                ? 'text-amber-400'
                : card.footerTone === 'rose'
                  ? 'text-rose-400'
                  : 'text-slate-300'
          }`}
        >
          {card.footerValue}
        </span>
      </div>
    </div>
  );
}

export const MetricCards: React.FC<MetricCardsProps> = ({ walletStatus, onOpenLiveScanner }) => {
  const balanceNum = walletStatus ? parseFloat(walletStatus.usdcBalance) || 0 : 0;
  const inboundTransfers = walletStatus ? walletStatus.recentTransfers.length : 0;

  const cards: CardDef[] = [
    {
      kpi: 'Primary KPI',
      icon: <DollarSign className="w-4 h-4" />,
      accent: 'emerald',
      value: (
        <>
          <AnimatedNumber value={balanceNum} decimals={2} prefix="$" durationMs={900} />
          <span className="text-xs font-mono text-slate-400 ml-1.5">USDC</span>
        </>
      ),
      sub: (
        <div className="flex items-center justify-between">
          <span>Live on-chain payout wallet</span>
          <button
            onClick={onOpenLiveScanner}
            className="text-emerald-400 hover:text-emerald-300 font-mono text-[10px] underline underline-offset-2"
          >
            Scan →
          </button>
        </div>
      ),
      footerLabel: 'Target Address Inbound:',
      footerValue: `${inboundTransfers} ${inboundTransfers === 1 ? 'tx' : 'txs'}`,
      footerTone: inboundTransfers > 0 ? 'emerald' : 'amber',
      sparkSeed: 17,
    },
    {
      kpi: 'Forensic Filter',
      icon: <ShieldAlert className="w-4 h-4" />,
      accent: 'rose',
      value: (
        <>
          <AnimatedNumber value={71.4} decimals={1} suffix="%" durationMs={1100} />
          <span className="text-xs font-mono text-slate-400 ml-1.5">Wash/Sybil</span>
        </>
      ),
      sub: <span>Settlements excluded under E0–E2 circular funding rules.</span>,
      footerLabel: 'Counted in Economics:',
      footerValue: 'Only E3–E5',
      footerTone: 'emerald',
      sparkSeed: 41,
    },
    {
      kpi: 'Proven Unit Ticket',
      icon: <TrendingUp className="w-4 h-4" />,
      accent: 'emerald',
      value: (
        <>
          <span className="text-white">$6.50</span>
          <span className="text-sm text-slate-500 mx-1">–</span>
          <span className="text-white">$12</span>
          <span className="text-xs font-mono text-slate-400 ml-1.5">/outcome</span>
        </>
      ),
      sub: <span>Decision-ready reports outperform $0.001 raw feeds by 5,000×.</span>,
      footerLabel: 'Priority Bracket:',
      footerValue: '$1–$10 & $10–$50',
      footerTone: 'slate',
      sparkSeed: 73,
    },
    {
      kpi: 'Variable Economics',
      icon: <Activity className="w-4 h-4" />,
      accent: 'teal',
      value: (
        <>
          <AnimatedNumber value={96.8} decimals={1} suffix="%" durationMs={1000} />
          <span className="text-xs font-mono text-slate-400 ml-1.5">Net Margin</span>
        </>
      ),
      sub: <span>Variable inference &amp; RPC: ~$0.14–$0.28 per delivery.</span>,
      footerLabel: 'Net Profit / Order:',
      footerValue: '+$6.27 to +$11.72',
      footerTone: 'emerald',
      sparkSeed: 91,
    },
    {
      kpi: 'Autonomy Index',
      icon: <Cpu className="w-4 h-4" />,
      accent: 'amber',
      value: <span className="text-amber-300">A4 Feasible</span>,
      sub: <span>Full 402 loop automated; human only for initial wallet &amp; legal setup.</span>,
      footerLabel: 'Start Capital:',
      footerValue: '~$0.00 (Zero)',
      footerTone: 'emerald',
      sparkSeed: 113,
    },
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3.5 mb-6">
      {cards.map((c, i) => (
        <FadeIn key={i} delay={i * 0.06} duration={0.4} y={14}>
          <MetricCard card={c} />
        </FadeIn>
      ))}
    </div>
  );
};
