"use client";

import { useEffect, useState } from "react";
import { Box, Coins, Activity, Clock, Wifi } from "lucide-react";
import type { OnChainWalletStatus } from "@/lib/apsa/base-rpc";
import { shortAddr } from "@/lib/apsa/wallet-registry";

interface LiveTickerProps {
  walletStatus: OnChainWalletStatus | null;
  testSuitePassed: boolean | null;
  lastTestRunAt: number | null;
}

/**
 * LiveTicker — a slim sticky sub-header strip that surfaces the most
 * critical live signals at all times: latest Base block, on-chain USDC
 * balance of the receive-only payout wallet, test-suite verdict, and
 * time since last sync. Sits directly below the main Header.
 */
export function LiveTicker({
  walletStatus,
  testSuitePassed,
  lastTestRunAt,
}: LiveTickerProps) {
  const [now, setNow] = useState(() => Date.now());

  useEffect(() => {
    const id = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(id);
  }, []);

  const block = walletStatus?.blockNumber ?? null;
  const balance = walletStatus?.usdcBalance ?? null;
  const isRealRpc = walletStatus?.isRealRpc ?? false;
  const syncedAgo = lastTestRunAt
    ? Math.max(0, Math.floor((now - lastTestRunAt) / 1000))
    : null;

  return (
    <div className="sticky top-[57px] z-30 border-b border-slate-800/80 bg-slate-950/85 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-x-5 gap-y-1.5 overflow-x-auto py-2 text-[11px] font-mono scrollbar-none">
          {/* Block height */}
          <TickerChip
            icon={<Box className="w-3 h-3" />}
            label="BLOCK"
            value={block !== null ? `#${block.toLocaleString()}` : "—"}
            tone="slate"
          />

          {/* USDC balance */}
          <TickerChip
            icon={<Coins className="w-3 h-3" />}
            label="USDC"
            value={balance !== null ? `${balance}` : "—"}
            tone={Number(balance) > 0 ? "emerald" : "slate"}
          />

          {/* Test suite verdict */}
          <TickerChip
            icon={<Activity className="w-3 h-3" />}
            label="12-TEST"
            value={
              testSuitePassed === null
                ? "RUNNING"
                : testSuitePassed
                  ? "ALL PASS"
                  : "FAIL"
            }
            tone={
              testSuitePassed === null
                ? "amber"
                : testSuitePassed
                  ? "emerald"
                  : "rose"
            }
          />

          {/* Last sync */}
          {syncedAgo !== null && (
            <TickerChip
              icon={<Clock className="w-3 h-3" />}
              label="SYNC"
              value={
                syncedAgo < 60
                  ? `${syncedAgo}s ago`
                  : `${Math.floor(syncedAgo / 60)}m ago`
              }
              tone="slate"
            />
          )}

          {/* RPC mode */}
          <TickerChip
            icon={<Wifi className="w-3 h-3" />}
            label="RPC"
            value={isRealRpc ? "LIVE" : "FALLBACK"}
            tone={isRealRpc ? "emerald" : "amber"}
          />

          {/* Wallet short address (push to right) */}
          <div className="ml-auto flex items-center gap-2 text-slate-500 whitespace-nowrap">
            <span className="hidden sm:inline">RECEIVE-ONLY</span>
            <span className="text-slate-300">
              {shortAddr(
                walletStatus?.address ??
                  "0x829f877daAb94D766BB2b8511ad486C40f2C2BDA",
                6,
                4,
              )}
            </span>
            <span
              className={`inline-block w-1.5 h-1.5 rounded-full ${
                isRealRpc
                  ? "bg-emerald-400 apsa-live-dot"
                  : "bg-amber-400 apsa-live-dot"
              }`}
              aria-hidden="true"
            />
          </div>
        </div>
      </div>
    </div>
  );
}

type Tone = "slate" | "emerald" | "amber" | "rose";

const TONE_MAP: Record<Tone, { text: string; icon: string; dot?: string }> = {
  slate: { text: "text-slate-300", icon: "text-slate-400" },
  emerald: { text: "text-emerald-300", icon: "text-emerald-400" },
  amber: { text: "text-amber-300", icon: "text-amber-400" },
  rose: { text: "text-rose-300", icon: "text-rose-400" },
};

function TickerChip({
  icon,
  label,
  value,
  tone,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
  tone: Tone;
}) {
  const t = TONE_MAP[tone];
  return (
    <div className="flex items-center gap-1.5 whitespace-nowrap">
      <span className={t.icon}>{icon}</span>
      <span className="text-slate-500 tracking-wider">{label}</span>
      <span className={`font-semibold ${t.text}`}>{value}</span>
    </div>
  );
}
