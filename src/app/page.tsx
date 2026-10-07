"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
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
import { LiveTicker } from "@/components/apsa/live-ticker";
import { CommandPalette, type CommandAction } from "@/components/apsa/command-palette";
import { HelpDrawer } from "@/components/apsa/help-drawer";
import { TAB_HELPS } from "@/lib/apsa/tab-helps";
import type { OnChainWalletStatus } from "@/lib/apsa/base-rpc";
import {
  EVM_PAYOUT_ADDRESS,
  shortAddr,
  PROTOCOL_VERSION,
} from "@/lib/apsa/wallet-registry";
import { toast } from "sonner";
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
  Command as CommandIcon,
  Download,
  HelpCircle,
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
  shortLabel: string;
  fullLabel: string;
  icon: React.ComponentType<{ className?: string }>;
  accent: string;
  hover: string;
}

const TABS: TabDef[] = [
  {
    id: "mission",
    shortLabel: "Mission",
    fullLabel: "🎯 Real Revenue Mission (12-Test Suite)",
    icon: Target,
    accent: "bg-rose-600 text-white shadow-sm ring-1 ring-rose-400/50",
    hover: "text-rose-400 hover:text-rose-200 hover:bg-rose-950/40",
  },
  {
    id: "verdict",
    shortLabel: "1. Verdict",
    fullLabel: "1. Verdict & Report (Sec 18–21)",
    icon: Award,
    accent: "bg-emerald-600 text-white shadow-sm",
    hover: "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50",
  },
  {
    id: "forensics",
    shortLabel: "2. Wash Volume",
    fullLabel: "2. Wash Volume & E0–E5 (Sec 1–2)",
    icon: Layers,
    accent: "bg-emerald-600 text-white shadow-sm",
    hover: "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50",
  },
  {
    id: "candidates",
    shortLabel: "3. Candidates",
    fullLabel: "3. Top 10 Candidates (Sec 3–5)",
    icon: ShieldCheck,
    accent: "bg-emerald-600 text-white shadow-sm",
    hover: "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50",
  },
  {
    id: "novel",
    shortLabel: "4. Novel Ideas",
    fullLabel: "4. Top 2 & 5 Ideas (Sec 6–7)",
    icon: Sparkles,
    accent: "bg-emerald-600 text-white shadow-sm",
    hover: "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50",
  },
  {
    id: "testnet",
    shortLabel: "5. Testnet",
    fullLabel: "5. Testnet & Mainnet Cycle (Sec 8–12)",
    icon: Terminal,
    accent: "bg-emerald-600 text-white shadow-sm",
    hover: "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50",
  },
  {
    id: "economics",
    shortLabel: "6. Economics",
    fullLabel: "6. Unit Economics & Scenarios (Sec 13, 16–17)",
    icon: Calculator,
    accent: "bg-emerald-600 text-white shadow-sm",
    hover: "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50",
  },
  {
    id: "autonomy",
    shortLabel: "7. Autonomy",
    fullLabel: "7. A4/A5 Autonomy & Manifest (Sec 14–15)",
    icon: Cpu,
    accent: "bg-emerald-600 text-white shadow-sm",
    hover: "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50",
  },
  {
    id: "scanner",
    shortLabel: "8. RPC Scanner",
    fullLabel: "8. Live Base RPC Scanner",
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
  const [testSuitePassed, setTestSuitePassed] = useState<boolean | null>(null);
  const [lastTestRunAt, setLastTestRunAt] = useState<number | null>(null);
  const [paletteOpen, setPaletteOpen] = useState(false);
  const [helpOpen, setHelpOpen] = useState(false);

  // Keyboard shortcuts: 1-9 jump to tabs, ? opens help, Cmd/Ctrl+K opens palette.
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement | null;
      const tag = target?.tagName;
      const isTyping =
        tag === "INPUT" ||
        tag === "TEXTAREA" ||
        tag === "SELECT" ||
        (target?.isContentEditable ?? false);
      // Allow Cmd/Ctrl+K even while typing.
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") return;
      if (isTyping) return;

      // ? (Shift+/) toggles help
      if (e.key === "?" || (e.shiftKey && e.key === "/")) {
        e.preventDefault();
        setHelpOpen((o) => !o);
        return;
      }
      // 1-9 jump to tabs (1 = first tab = mission, 2 = verdict, ...)
      const n = parseInt(e.key, 10);
      if (!isNaN(n) && n >= 1 && n <= TABS.length) {
        const tab = TABS[n - 1];
        if (tab) {
          setActiveTab(tab.id);
          window.scrollTo({ top: 360, behavior: "smooth" });
        }
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

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

  // Poll /api/onchain/status once on mount so the LiveTicker + MetricCards
  // have data even before the user visits the Scanner tab. Subsequent polling
  // is handled by the LiveOnChainTracker component itself.
  useEffect(() => {
    let cancelled = false;
    fetch("/api/onchain/status?network=base-mainnet")
      .then((r) => r.json())
      .then((s: OnChainWalletStatus) => {
        if (!cancelled) setWalletStatus(s);
      })
      .catch(() => {
        /* silent — Scanner tab will retry */
      });
    return () => {
      cancelled = true;
    };
  }, []);

  // Poll the test suite once on mount so the LiveTicker reflects the verdict
  // without forcing the user to the Mission tab. Initial state is already
  // `null` (= "RUNNING"), so we only set it after the fetch resolves.
  useEffect(() => {
    let cancelled = false;
    fetch("/api/test-suite", { method: "POST" })
      .then((r) => r.json())
      .then((d: { passed: boolean; count: number }) => {
        if (cancelled) return;
        setTestSuitePassed(d.passed);
        setLastTestRunAt(Date.now());
      })
      .catch(() => {
        if (!cancelled) setTestSuitePassed(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  // Build command palette actions.
  const commandActions = useMemo<CommandAction[]>(
    () => [
      ...TABS.map((t) => ({
        id: `goto-${t.id}`,
        label: `Go to: ${t.shortLabel}`,
        hint: t.fullLabel,
        group: "Navigate" as const,
        keywords: [t.id, t.shortLabel],
        run: () => {
          setActiveTab(t.id);
          window.scrollTo({ top: 360, behavior: "smooth" });
        },
      })),
      {
        id: "run-tests",
        label: "Re-run 12-Test Verification Suite",
        hint: "POST /api/test-suite",
        group: "Actions",
        keywords: ["test", "verify", "x402", "protocol"],
        run: () => {
          setActiveTab("mission");
          window.scrollTo({ top: 360, behavior: "smooth" });
          toast.info("Re-running 12-test suite…", {
            description: "Executing protocol verification on Base Mainnet.",
          });
        },
      },
      {
        id: "run-simulation",
        label: "Trigger x402 Protocol Cycle",
        hint: "Testnet workbench",
        group: "Actions",
        keywords: ["simulate", "402", "sentinel", "sarif"],
        run: () => {
          setActiveTab("testnet");
          window.scrollTo({ top: 360, behavior: "smooth" });
          toast.info("Opening x402 testnet workbench…");
        },
      },
      {
        id: "scan-wallet",
        label: "Scan receive-only wallet on Base",
        hint: "Live RPC",
        group: "Actions",
        keywords: ["rpc", "base", "usdc", "balance", "wallet"],
        run: () => {
          setActiveTab("scanner");
          window.scrollTo({ top: 360, behavior: "smooth" });
        },
      },
      {
        id: "download-bundle",
        label: "Download protocol archive (.zip)",
        hint: "158 KB",
        group: "Actions",
        keywords: ["zip", "archive", "bundle", "download"],
        run: () => {
          window.open("/api/download/bundle.zip", "_blank");
        },
      },
      {
        id: "toggle-network",
        label: "Toggle Base Mainnet / Sepolia",
        hint: "Switch network",
        group: "Actions",
        keywords: ["network", "sepolia", "mainnet"],
        run: () => {
          setActiveNetwork((n) =>
            n === "base-mainnet" ? "base-sepolia" : "base-mainnet",
          );
          toast.success(
            `Switched to ${
              activeNetwork === "base-mainnet" ? "Base Sepolia" : "Base Mainnet"
            }`,
          );
        },
      },
      {
        id: "health",
        label: "Open /api/health endpoint",
        hint: "Free probe",
        group: "External",
        keywords: ["uptime", "status", "api"],
        run: () => window.open("/api/health", "_blank"),
      },
      {
        id: "manifest",
        label: "Open x402 discovery manifest",
        hint: "/.well-known/x402-manifest.json",
        group: "External",
        keywords: ["manifest", "discovery", "agent", "mcp"],
        run: () => window.open("/.well-known/x402-manifest.json", "_blank"),
      },
      {
        id: "basescan",
        label: "View payout wallet on BaseScan",
        hint: "External",
        group: "External",
        keywords: ["explorer", "etherscan", "basescan", "wallet"],
        run: () =>
          window.open(
            `https://basescan.org/address/${EVM_PAYOUT_ADDRESS}`,
            "_blank",
          ),
      },
    ],
    // activeNetwork is intentionally a dep so the toggle-network action label
    // resolves correctly.
    [activeNetwork],
  );

  return (
    <div className="min-h-screen flex flex-col bg-[#0a0e15] text-slate-100 font-sans selection:bg-emerald-500/30 selection:text-white">
      <Header
        activeNetwork={activeNetwork}
        onNetworkChange={setActiveNetwork}
        onExportReport={handleExportReport}
        onOpenTestHarness={handleOpenTestHarness}
      />

      <LiveTicker
        walletStatus={walletStatus}
        testSuitePassed={testSuitePassed}
        lastTestRunAt={lastTestRunAt}
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
                  title={tab.fullLabel}
                  className={`px-3 py-2 rounded-lg font-medium transition-all flex items-center gap-2 whitespace-nowrap ${
                    isActive ? tab.accent : tab.hover
                  }`}
                >
                  <Icon className="w-3.5 h-3.5 flex-shrink-0" />
                  <span>{tab.shortLabel}</span>
                </button>
              );
            })}
            <button
              onClick={() => setHelpOpen(true)}
              title="What am I looking at? (Press ?)"
              className="px-2.5 py-2 rounded-lg text-slate-400 hover:text-emerald-300 hover:bg-slate-800/60 flex items-center gap-1.5 transition-colors flex-shrink-0"
            >
              <HelpCircle className="w-3.5 h-3.5" />
              <kbd className="hidden sm:inline text-[10px] text-slate-500 font-mono">
                ?
              </kbd>
            </button>
            <button
              onClick={() => setPaletteOpen(true)}
              title="Open command palette (Cmd+K)"
              className="px-2.5 py-2 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800/60 flex items-center gap-1.5 transition-colors flex-shrink-0"
            >
              <CommandIcon className="w-3.5 h-3.5" />
              <kbd className="hidden sm:inline text-[10px] text-slate-500 font-mono">
                ⌘K
              </kbd>
            </button>
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

        {/* Quick-action floating buttons (desktop only, subtle) */}
        <div className="hidden lg:flex fixed bottom-6 right-6 z-30 flex-col gap-2">
          <button
            onClick={() => setHelpOpen(true)}
            className="group w-11 h-11 rounded-full bg-slate-900 border border-slate-700 hover:border-emerald-500/50 hover:bg-slate-800 text-slate-300 hover:text-emerald-300 flex items-center justify-center shadow-lg shadow-black/40 transition-all"
            title="What am I looking at? (?)"
            aria-label="Open help drawer"
          >
            <HelpCircle className="w-4 h-4" />
          </button>
          <button
            onClick={() => setPaletteOpen(true)}
            className="group w-11 h-11 rounded-full bg-slate-900 border border-slate-700 hover:border-emerald-500/50 hover:bg-slate-800 text-slate-300 hover:text-emerald-300 flex items-center justify-center shadow-lg shadow-black/40 transition-all"
            title="Command palette (Cmd+K)"
            aria-label="Open command palette"
          >
            <CommandIcon className="w-4 h-4" />
          </button>
          <a
            href="/api/download/bundle.zip"
            download="APSA-2026-COMPLETE-AUTONOMOUS-MONEY-HUNTER.zip"
            className="group w-11 h-11 rounded-full bg-amber-600 hover:bg-amber-500 text-white flex items-center justify-center shadow-lg shadow-amber-950/40 transition-all"
            title="Download protocol archive"
            aria-label="Download protocol archive"
          >
            <Download className="w-4 h-4" />
          </a>
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

      <CommandPalette
        actions={commandActions}
        open={paletteOpen}
        onOpenChange={setPaletteOpen}
      />

      <HelpDrawer
        open={helpOpen}
        onOpenChange={setHelpOpen}
        helps={TAB_HELPS}
        activeTabId={activeTab}
        onNavigate={(id) => {
          setActiveTab(id as ActiveTab);
          window.scrollTo({ top: 360, behavior: "smooth" });
        }}
      />
    </div>
  );
}
