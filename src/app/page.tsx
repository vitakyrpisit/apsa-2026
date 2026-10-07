"use client";

import { useCallback, useState } from "react";
import { Header } from "@/components/apsa/Header";
import { MetricCards } from "@/components/apsa/MetricCards";
import { LiveOnChainTracker } from "@/components/apsa/LiveOnChainTracker";
import { WashVolumeForensics } from "@/components/apsa/WashVolumeForensics";
import { CandidatesDirectory } from "@/components/apsa/CandidatesDirectory";
import { NovelConcepts } from "@/components/apsa/NovelConcepts";
import { TestnetWorkbench } from "@/components/apsa/TestnetWorkbench";
import { UnitEconomicsSimulator } from "@/components/apsa/UnitEconomicsSimulator";
import { AutonomousLoopAudit } from "@/components/apsa/AutonomousLoopAudit";
import { ExecutiveVerdictReport } from "@/components/apsa/ExecutiveVerdictReport";
import { RealRevenueHarness } from "@/components/apsa/RealRevenueHarness";
import type { OnChainWalletStatus } from "@/lib/apsa/base-rpc";
import {
  EVM_PAYOUT_ADDRESS,
  shortAddr,
  PROTOCOL_VERSION,
} from "@/lib/apsa/wallet-registry";
import {
  ShieldCheck,
  Layers,
  Terminal,
  Award,
  Calculator,
  Cpu,
  Activity,
  Sparkles,
  ExternalLink,
  Target,
  Github,
  Lock,
  Zap,
} from "lucide-react";

type ActiveTab =
  | "mission"
  | "verdict"
  | "forensics"
  | "candidates"
  | "novel"
  | "testnet"
  | "economics"
  | "autonomy"
  | "scanner";

type Network = "base-mainnet" | "base-sepolia";

interface TabDef {
  id: ActiveTab;
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  accent: string; // active classes
  hover: string;
}

const TABS: TabDef[] = [
  {
    id: "mission",
    label: "🎯 Real Revenue Mission (12-Test Suite)",
    icon: Target,
    accent: "bg-rose-600 text-white shadow-sm ring-1 ring-rose-400/50",
    hover: "text-rose-400 hover:text-rose-200 hover:bg-rose-950/40",
  },
  {
    id: "verdict",
    label: "1. Verdict & Report (Sec 18–21)",
    icon: Award,
    accent: "bg-emerald-600 text-white shadow-sm",
    hover: "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50",
  },
  {
    id: "forensics",
    label: "2. Wash Volume & E0–E5 (Sec 1–2)",
    icon: Layers,
    accent: "bg-emerald-600 text-white shadow-sm",
    hover: "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50",
  },
  {
    id: "candidates",
    label: "3. Top 10 Candidates (Sec 3–5)",
    icon: ShieldCheck,
    accent: "bg-emerald-600 text-white shadow-sm",
    hover: "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50",
  },
  {
    id: "novel",
    label: "4. Top 2 & 5 Ideas (Sec 6–7)",
    icon: Sparkles,
    accent: "bg-emerald-600 text-white shadow-sm",
    hover: "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50",
  },
  {
    id: "testnet",
    label: "5. Testnet & Mainnet Cycle (Sec 8–12)",
    icon: Terminal,
    accent: "bg-emerald-600 text-white shadow-sm",
    hover: "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50",
  },
  {
    id: "economics",
    label: "6. Unit Economics & Scenarios (Sec 13, 16–17)",
    icon: Calculator,
    accent: "bg-emerald-600 text-white shadow-sm",
    hover: "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50",
  },
  {
    id: "autonomy",
    label: "7. A4/A5 Autonomy & Manifest (Sec 14–15)",
    icon: Cpu,
    accent: "bg-emerald-600 text-white shadow-sm",
    hover: "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50",
  },
  {
    id: "scanner",
    label: "8. Live Base RPC Scanner",
    icon: Activity,
    accent: "bg-emerald-600 text-white shadow-sm",
    hover: "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50",
  },
];

export default function Home() {
  const [activeNetwork, setActiveNetwork] = useState<Network>("base-mainnet");
  const [activeTab, setActiveTab] = useState<ActiveTab>("mission");
  const [walletStatus, setWalletStatus] = useState<OnChainWalletStatus | null>(
    null,
  );

  const handleExportReport = useCallback(() => {
    setActiveTab("verdict");
    if (typeof window !== "undefined") {
      window.scrollTo({ top: 360, behavior: "smooth" });
    }
  }, []);

  const handleOpenTestHarness = useCallback(() => {
    setActiveTab("testnet");
    if (typeof window !== "undefined") {
      window.scrollTo({ top: 360, behavior: "smooth" });
    }
  }, []);

  const handleStatusUpdated = useCallback((status: OnChainWalletStatus) => {
    setWalletStatus(status);
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-[#0a0e15] text-slate-100 font-sans selection:bg-emerald-500/30 selection:text-white">
      <Header
        activeNetwork={activeNetwork}
        onNetworkChange={setActiveNetwork}
        onExportReport={handleExportReport}
        onOpenTestHarness={handleOpenTestHarness}
      />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <MetricCards
          walletStatus={walletStatus}
          onOpenLiveScanner={() => setActiveTab("scanner")}
        />

        {/* Primary Navigation Tabs */}
        <nav
          aria-label="APSA dashboard sections"
          className="mb-6 border-b border-slate-800 pb-3"
        >
          <div className="flex items-center gap-1.5 overflow-x-auto p-1 bg-slate-900/90 rounded-xl border border-slate-800/80 text-xs font-mono scrollbar-none">
            {TABS.map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  aria-current={isActive ? "page" : undefined}
                  className={`px-3 py-2 rounded-lg font-medium transition-all flex items-center gap-2 whitespace-nowrap ${
                    isActive ? tab.accent : tab.hover
                  }`}
                >
                  <Icon className="w-3.5 h-3.5 flex-shrink-0" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </div>
        </nav>

        {/* Dynamic Tab Panes */}
        <div className="transition-opacity duration-200">
          {activeTab === "mission" && <RealRevenueHarness />}
          {activeTab === "verdict" && (
            <ExecutiveVerdictReport
              walletStatus={walletStatus}
              onOpenTestHarness={handleOpenTestHarness}
            />
          )}
          {activeTab === "forensics" && <WashVolumeForensics />}
          {activeTab === "candidates" && <CandidatesDirectory />}
          {activeTab === "novel" && <NovelConcepts />}
          {activeTab === "testnet" && (
            <TestnetWorkbench network={activeNetwork} />
          )}
          {activeTab === "economics" && <UnitEconomicsSimulator />}
          {activeTab === "autonomy" && <AutonomousLoopAudit />}
          {activeTab === "scanner" && (
            <LiveOnChainTracker
              network={activeNetwork}
              onStatusUpdated={handleStatusUpdated}
            />
          )}
        </div>
      </main>

      {/* Sticky Footer */}
      <footer className="mt-auto border-t border-slate-800/80 bg-slate-950/95 backdrop-blur py-6">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs font-mono text-slate-400">
          <div className="flex flex-wrap items-center gap-2">
            <span className="flex items-center gap-1.5 text-slate-200 font-semibold">
              <span className="w-5 h-5 rounded bg-emerald-950 border border-emerald-500/40 text-emerald-400 flex items-center justify-center text-[10px] font-bold">
                402
              </span>
              {PROTOCOL_VERSION} · Autonomous Money Hunter
            </span>
            <span aria-hidden="true">·</span>
            <span>Base L2 USDC Protocol</span>
            <span aria-hidden="true">·</span>
            <span className="flex items-center gap-1">
              <Lock className="w-3 h-3 text-emerald-400" />
              Receive-Only: {shortAddr(EVM_PAYOUT_ADDRESS)}
            </span>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <span className="flex items-center gap-1 text-emerald-400">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 apsa-live-dot" />
              Active Audit
            </span>
            <span aria-hidden="true">·</span>
            <a
              href="/api/health"
              target="_blank"
              rel="noreferrer"
              className="text-emerald-400 hover:text-emerald-300 flex items-center gap-1"
            >
              <Zap className="w-3 h-3" />
              /api/health
            </a>
            <span aria-hidden="true">·</span>
            <a
              href={`https://basescan.org/address/${EVM_PAYOUT_ADDRESS}`}
              target="_blank"
              rel="noreferrer"
              className="text-emerald-400 hover:text-emerald-300 flex items-center gap-1"
            >
              BaseScan Explorer <ExternalLink className="w-3 h-3" />
            </a>
            <span aria-hidden="true">·</span>
            <span className="flex items-center gap-1 text-slate-500">
              <Github className="w-3 h-3" /> Zero Operator Keys Exposed
            </span>
          </div>
        </div>
      </footer>
    </div>
  );
}
